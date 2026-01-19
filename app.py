# cell_id: 9961351c - Mis à jour le 2024-05-18 17:12 (Paris)
import os, re, csv, io, zipfile
import tempfile
from typing import List, Dict, Tuple, Optional
import streamlit as st

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm, mm
from reportlab.lib import colors
from reportlab.platypus import Frame, Paragraph, KeepInFrame
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.utils import ImageReader
from PIL import Image

# ----------------------------
# Réglages
# ----------------------------
OUTPUT_PDF = "cartes_recto_verso.pdf"
# NB_CARTES, COLS, ROWS set to portrait layout (3x3 cards)
NB_CARTES = 9
COLS, ROWS = 3, 3

MARGIN = 1.0 * cm
GAP = 0.35 * cm              # espace entre cartes (découpe)
BORDER_WIDTH = 1
ELEMENT_SPACING = 0.8 * cm   # Espace entre les éléments (texte, image) et les bords de la carte
RECTO_FRAME_WIDTH = 4 * mm   # Largeur du cadre pour l'option recto "cadre"

# Couleurs (recto)
DEFAULT_BACK_COLOR_NAME = "gris"
DEFAULT_BACK_COLOR = colors.HexColor("#B3B3B3")
COLOR_MAP = {
    "bleu": colors.HexColor("#2D6CDF"),
    "rouge": colors.HexColor("#D64541"),
    "rose": colors.HexColor("#E85D9E"),
    "vert": colors.HexColor("#2ECC71"),
    "jaune": colors.HexColor("#F1C40F"),
    "blanc": colors.white, # Ajout du blanc
    "gris": DEFAULT_BACK_COLOR
}

def pick_color_from_filename(filename: str) -> Tuple[str, colors.Color]:
    return DEFAULT_BACK_COLOR_NAME, DEFAULT_BACK_COLOR

def parse_color_string(color_str: str, default_color: colors.Color) -> colors.Color:
    if not color_str:
        return default_color

    # Try to match predefined color names
    if color_str.lower() in COLOR_MAP:
        return COLOR_MAP[color_str.lower()]

    # Try to match hexadecimal color codes (3 or 6 digits)
    hex_match = re.match(r'^#?([0-9a-fA-F]{3}(?:[0-9a-fA-F]{3})?)$', color_str.strip())
    if hex_match:
        # Ensure it's a 6-digit hex code for ReportLab
        hex_code_val = hex_match.group(1)
        if len(hex_code_val) == 3:
            hex_code_val = ''.join([c*2 for c in hex_code_val]) # Expand 3-digit to 6-digit
        hex_code = "#" + hex_code_val
        try:
            return colors.HexColor(hex_code)
        except Exception:
            # Fallback if HexColor parsing fails
            pass

    # If neither, return default color
    return default_color

def is_dark(c: colors.Color) -> bool:
    r, g, b = c.red, c.green, c.blue
    # For white, we need to explicitly return false for dark to ensure black text
    if c == colors.white:
        return False
    lum = 0.2126*r + 0.7152*g + 0.0722*b
    return lum < 0.55

def sniff_dialect(data: str) -> csv.Dialect:
    # Priority to semicolon if it seems like the primary delimiter
    if ';' in data:
        try:
            # Check if semicolon works as a reasonable delimiter (e.g., more than one field)
            # and if it appears consistently enough to be the primary delimiter
            f_test = io.StringIO(data)
            test_reader = csv.reader(f_test, delimiter=';')
            # Look at first few lines to guess consistency
            sample_lines = data.splitlines()[:5]
            if any(len(row) > 1 for row in csv.reader(io.StringIO(sample_lines[0]), delimiter=';')) or all(';' in line for line in sample_lines if line.strip()):
                class SemicolonDialect(csv.excel):
                    delimiter = ';'
                return SemicolonDialect()
        except Exception:
            pass # Fall through to other options

    # Then try to sniff more generally
    sniffer = csv.Sniffer()
    try:
        # Sniff using common delimiters, excluding semicolon since we handled it
        dialect = sniffer.sniff(data[:4096], delimiters=',\t')
        return dialect
    except csv.Error:
        # If sniffing fails (e.g., single column data or unusual format),
        # return excel dialect as a robust default (usually comma-delimited)
        return csv.get_dialect('excel')

def normalize_header(h: str) -> str:
    return re.sub(r"\s+", "", (h or "").strip().lower())

def read_cards_from_csv(csv_file_content: str) -> List[Dict[str, str]]:
    """
    CSV attendu (souple) :
    - question : colonne 'question' (ou 1re colonne si pas d'en-tête)
    - texte verso : colonne 'texte' / 'reponse' / 'réponse' / 'answer' (ou 2e/3e colonne selon présence d'en-tête)
    - image recto : colonne 'image_recto' / 'imagerecto' (ou 3e colonne si pas d'en-tête)
    - image verso : colonne 'image_verso' / 'imageverso' (ou 4e colonne si pas d'en-tête)
    """
    # Use io.StringIO to treat the string content as a file
    f = io.StringIO(csv_file_content)

    dialect = sniff_dialect(csv_file_content)
    reader = csv.reader(f, dialect)
    rows = list(reader)
    if not rows:
        return []

    first = rows[0]
    norm_first = [normalize_header(x) for x in first]
    has_header = any(x in ("question","q","texte","text","reponse","réponse","answer","reponseverso","verso", "image_recto", "imagerecto", "image_verso", "imageverso") for x in norm_first)

    def get_field(d: Dict[str,str], keys: List[str], fallback: str="") -> str:
        for k in keys:
            nk = normalize_header(k)
            for kk, vv in d.items():
                if normalize_header(kk) == nk:
                    return (vv or "").strip()
        return fallback

    out = []
    if has_header:
        headers = norm_first
        for r in rows[1:]:
            if not any(str(x).strip() for x in r):
                continue
            d = {headers[i]: (r[i].strip() if i < len(r) else "") for i in range(len(headers))}
            q_raw = get_field(d, ["question","q"])
            card_color_string = None
            question_text = q_raw # Default to raw question

            # Try to find (color_name_or_hex) at the BEGINNING of the string, case-insensitive
            match_beginning = re.match(r'^\s*\(([^)]+)\)\s*(.*)$', q_raw, re.IGNORECASE)
            if match_beginning:
                card_color_string = match_beginning.group(1).strip()
                question_text = match_beginning.group(2).strip()
            else:
                # If not at the beginning, try to find (color_name_or_hex) at the END of the string
                match_end = re.search(r'\s*\(([^)]+)\)\s*$', q_raw, re.IGNORECASE)
                if match_end:
                    card_color_string = match_end.group(1).strip()
                    question_text = re.sub(r'\s*\(([^)]+)\)\s*$', '', q_raw, flags=re.IGNORECASE).strip()

            txt = get_field(d, ["texte","text","reponse","réponse","answer","verso","reponseverso"])
            card_image_recto = get_field(d, ["image_recto", "imagerecto"])
            card_image_verso = get_field(d, ["image_verso", "imageverso"])
            out.append({"question": question_text, "texte": txt, "card_color_key": card_color_string, "image_recto": card_image_recto, "image_verso": card_image_verso})
    else:
        # Sans en-tête : col1=question, col2=texte, col3=image_recto, col4=image_verso
        for r in rows:
            if not any(str(x).strip() for x in r):
                continue
            q_raw = (r[0].strip() if len(r) > 0 else "")
            card_color_string = None
            question_text = q_raw

            match_beginning = re.match(r'^\s*\(([^)]+)\)\s*(.*)$', q_raw, re.IGNORECASE)
            if match_beginning:
                card_color_string = match_beginning.group(1).strip()
                question_text = match_beginning.group(2).strip()
            else:
                match_end = re.search(r'\s*\(([^)]+)\)\s*$', q_raw, re.IGNORECASE)
                if match_end:
                    card_color_string = match_end.group(1).strip()
                    question_text = re.sub(r'\s*\(([^)]+)\)\s*$', '', q_raw, flags=re.IGNORECASE).strip()

            txt = (r[1].strip() if len(r) > 1 else "") # Second column for verso text
            card_image_recto = (r[2].strip() if len(r) > 2 else "") # Third column for recto image
            card_image_verso = (r[3].strip() if len(r) > 3 else "") # Fourth column for verso image
            out.append({"question": question_text, "texte": txt, "card_color_key": card_color_string, "image_recto": card_image_recto, "image_verso": card_image_verso})

    return out

# ----------------------------
# Mise en page
# ----------------------------
class Grid:
    def __init__(self, page_w, page_h, card_w, card_h, x0, y0):
        self.page_w = page_w
        self.page_h = page_h
        self.card_w = card_w
        self.card_h = card_h
        self.x0 = x0
        self.y0 = y0

def compute_grid() -> Grid:
    # COLS, ROWS, NB_CARTES are now global variables, updated by Streamlit UI
    page_w, page_h = A4
    usable_w = page_w - 2*MARGIN - (COLS-1)*GAP
    usable_h = page_h - 2*MARGIN - (ROWS-1)*GAP
    card_w = usable_w / COLS
    card_h = usable_h / ROWS
    return Grid(page_w, page_h, card_w, card_h, MARGIN, MARGIN)

def card_xy(grid: Grid, col: int, row: int) -> Tuple[float,float]:
    # row 0 en haut
    x = grid.x0 + col*(grid.card_w + GAP)
    y_top = grid.page_h - grid.y0 - row*(grid.card_h + GAP)
    y = y_top - grid.card_h
    return x, y

def draw_card_border(c: canvas.Canvas, x: float, y: float, w: float, h: float, stroke_color=colors.lightgrey):
    c.setLineWidth(BORDER_WIDTH)
    c.setStrokeColor(stroke_color)
    c.rect(x, y, w, h, stroke=1, fill=0)

def draw_centered_text_in_box(c: canvas.Canvas, x: float, y: float, w: float, h: float, text: str, style: ParagraphStyle):
    pad = 6 # Internal padding for the text within the card

    # Calculate the inner dimensions for the text area
    inner_x = x + pad
    inner_y = y + pad
    inner_w = w - 2 * pad
    inner_h = h - 2 * pad

    # Replace semicolons and newlines with line breaks for display
    formatted_text = (text or "").replace(";", "<br/>").replace("\n","<br/>")
    p = Paragraph(formatted_text if formatted_text.strip() else "&nbsp;", style)

    # Get the actual height the paragraph would take if wrapped within inner_w
    # We pass a temporary canvas and a very large height to allow it to compute its natural height
    text_width, text_height = p.wrapOn(c, inner_w, inner_h * 100)

    # Ensure text_height does not exceed inner_h, and shrink if necessary
    if text_height > inner_h:
        text_height = inner_h

    # Calculate vertical offset to center the text
    y_offset = (inner_h - text_height) / 2

    # Draw the paragraph
    # The y-coordinate for drawOn is the bottom-left corner of the paragraph.
    # We want to place the bottom of the paragraph at (inner_y + y_offset).
    p.drawOn(c, inner_x, inner_y + y_offset)

def draw_cut_marks(c: canvas.Canvas, grid: Grid):
    c.setLineWidth(0.2) # Thinner lines for cut marks
    c.setStrokeColor(colors.black)
    page_w, page_h = A4

    # Vertical grid lines: at left and right of each card block
    for j in range(COLS):
        x_left_card = grid.x0 + j * (grid.card_w + GAP)
        x_right_card = x_left_card + grid.card_w
        c.line(x_left_card, 0, x_left_card, page_h) # Left edge of card, extends full page
        c.line(x_right_card, 0, x_right_card, page_h) # Right edge of card, extends full page

    # Horizontal grid lines: at bottom and top of each card block
    for i in range(ROWS):
        y_bottom_card = grid.y0 + i * (grid.card_h + GAP)
        y_top_card = y_bottom_card + grid.card_h
        c.line(0, y_bottom_card, page_w, y_bottom_card) # Bottom edge of card, extends full page
        c.line(0, y_top_card, page_w, y_top_card) # Top edge of card, extends full page

def build_pdf(
    cards: List[Dict[str,str]],
    default_back_color: colors.Color,
    output_buffer: io.BytesIO,
    uploaded_recto_images: Dict[str, Image.Image] = None,
    recto_color_style: str = "Remplissage (couleur pleine)"
):
    # Retrieve current COLS, ROWS, NB_CARTES from global scope
    global COLS, ROWS, NB_CARTES
    grid = compute_grid()

    base_font = "Helvetica"
    style_verso = ParagraphStyle(
        "Verso", fontName=base_font, fontSize=12.5, leading=14.5,
        alignment=TA_CENTER, textColor=colors.black
    )

    cards_to_process = (cards[:NB_CARTES] + [{"question":"","texte":""}] * NB_CARTES)[:NB_CARTES]

    c = canvas.Canvas(output_buffer, pagesize=A4)

    temp_image_files_to_clean = [] # List to keep track of temporary files for cleanup

    # -------- Recto --------
    for i in range(NB_CARTES):
        row = i // COLS
        col = i % COLS
        x, y = card_xy(grid, col, row)

        # Determine the background color for the current card
        card_specific_color_string = cards_to_process[i].get("card_color_key")
        current_back_color = parse_color_string(card_specific_color_string, default_back_color)

        use_frame_style = recto_color_style == "Cadre 4 mm"
        recto_fill_color = current_back_color
        recto_image_background_color = current_back_color
        content_x, content_y = x, y
        content_w, content_h = grid.card_w, grid.card_h

        if use_frame_style:
            recto_fill_color = colors.white
            recto_image_background_color = colors.white
            content_x = x + RECTO_FRAME_WIDTH
            content_y = y + RECTO_FRAME_WIDTH
            content_w = grid.card_w - (2 * RECTO_FRAME_WIDTH)
            content_h = grid.card_h - (2 * RECTO_FRAME_WIDTH)

        Recto text style: color adapted to background (depends on current_back_color)
        recto_text_color = colors.black if use_frame_style else (colors.white if is_dark(current_back_color) else colors.black)
        style_recto = ParagraphStyle(
            "Recto", fontName=base_font, fontSize=16, leading=18,
            alignment=TA_CENTER, textColor=recto_text_color
        )

        # Fill recto with background color
        c.setFillColor(recto_fill_color)
        c.rect(x, y, grid.card_w, grid.card_h, stroke=0, fill=1)
        if use_frame_style:
            c.setLineWidth(RECTO_FRAME_WIDTH)
            c.setStrokeColor(current_back_color)
            c.rect(
                x + RECTO_FRAME_WIDTH / 2,
                y + RECTO_FRAME_WIDTH / 2,
                grid.card_w - RECTO_FRAME_WIDTH,
                grid.card_h - RECTO_FRAME_WIDTH,
                stroke=1,
                fill=0
            )

        question_text_for_card = cards_to_process[i].get("question", "").strip()
        card_recto_image_filename = cards_to_process[i].get("image_recto", "").strip()

        current_recto_pil_image = None
        if card_recto_image_filename and uploaded_recto_images and card_recto_image_filename in uploaded_recto_images:
             current_recto_pil_image = uploaded_recto_images[card_recto_image_filename]

        image_to_draw_path = None
        if current_recto_pil_image:
            try:
                r = recto_image_background_color.red
                g = recto_image_background_color.green
                b = recto_image_background_color.blue
                bg_color_tuple = (int(r * 255), int(g * 255), int(b * 255))

                # Create a new RGB image with the desired background color
                alpha_composite_img = Image.new('RGB', current_recto_pil_image.size, bg_color_tuple)
                alpha_composite_img.paste(current_recto_pil_image, (0, 0), current_recto_pil_image) # The original_pil_image is used as the mask for pasting

                # Save the composited RGB image to a temporary file on disk
                with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as temp_png_file:
                    image_to_draw_path = temp_png_file.name
                    alpha_composite_img.save(temp_png_file, format='PNG')
                temp_image_files_to_clean.append(image_to_draw_path) # Add to cleanup list

            except Exception as e:
                st.error(f"Erreur lors du compositing de l'image de recto pour la carte {i}: {e}")
                image_to_draw_path = None


        if image_to_draw_path:
            if not question_text_for_card:
                # No text, image takes up 90% of card width, centered
                try:
                    # Get original dimensions using PIL to calculate aspect ratio
                    pil_img = Image.open(image_to_draw_path)
                    original_w, original_h = pil_img.size
                    pil_img.close() # Close the image file

                    # Desired width is 90% of the card's width
                    img_w = 0.9 * content_w

                    # Calculate proportional height
                    if original_w == 0:
                        raise ValueError("Image has zero width")
                    img_h = (original_h / original_w) * img_w

                    # Now, check if this calculated height exceeds 90% of the card's height
                    max_allowed_h = 0.9 * content_h

                    if img_h > max_allowed_h:
                        # If scaling by width makes it too tall, scale by height instead.
                        img_h = max_allowed_h
                        if original_h == 0: # Prevent division by zero if original_h is also 0
                            raise ValueError("Image has zero height after width check")
                        img_w = (original_w / original_h) * img_h # Recalculate width based on new height

                    # Calculate positions for centering the *final* sized image
                    img_x = content_x + (content_w - img_w) / 2
                    img_y = content_y + (content_h - img_h) / 2

                    c.drawImage(image_to_draw_path, img_x, img_y,
                                width=img_w, height=img_h, preserveAspectRatio=True)
                except Exception as e:
                    st.error(f"Erreur lors du dessin de l'image (90% largeur, sans texte) : {e}")
                    # If image drawing fails, draw empty text centrally as a fallback
                    draw_centered_text_in_box(c, content_x, content_y, content_w, content_h, "", style_recto)
            else:
                # Text is present, use original image/text layout with safe sizing
                available_h = max(content_h - (3 * ELEMENT_SPACING), 0)
                min_text_box_h = 1.0 * cm
                if available_h <= min_text_box_h:
                    img_h = max(available_h * 0.4, 0)
                else:
                    img_h = min(content_h / 2, max(available_h - min_text_box_h, 0))

                # Text is present, use original image/text layout
                img_h = content_h / 2
                img_w = img_h

                img_x = content_x + (content_w - img_w) / 2
                img_y = content_y + ELEMENT_SPACING

                text_box_h = max(available_h - img_h, 1)
                text_box_h = content_h - (3 * ELEMENT_SPACING + img_h)

                text_box_x = content_x
                text_box_y = img_y + img_h + ELEMENT_SPACING
                text_box_w = content_w

                try:
                    c.drawImage(image_to_draw_path, img_x, img_y,
                                width=img_w, height=img_h, preserveAspectRatio=True)
                except Exception as e:
                    st.error(f"Erreur lors du dessin de l'image (avec texte) : {e}")
                    # Fallback: draw text in full card area if image drawing still fails
                    draw_centered_text_in_box(c, content_x, content_y, content_w, content_h, question_text_for_card, style_recto)
                    continue

                draw_centered_text_in_box(c, text_box_x, text_box_y, text_box_w, text_box_h, question_text_for_card, style_recto)
        else:
            # No image or image processing failed, draw text in the full card area
            draw_centered_text_in_box(c, content_x, content_y, content_w, content_h, question_text_for_card, style_recto)

    draw_cut_marks(c, grid)
    c.showPage()

    # -------- Verso --------
    for i in range(NB_CARTES):
        row = i // COLS
        col = i % COLS
        back_col = (COLS - 1 - col) # inversion colonnes pour impression recto/verso
        x, y = card_xy(grid, back_col, row)

        # --- Image Verso --- #
        card_verso_image_filename = cards_to_process[i].get("image_verso", "").strip()
        current_verso_pil_image = None
        if card_verso_image_filename and uploaded_recto_images and card_verso_image_filename in uploaded_recto_images:
            current_verso_pil_image = uploaded_recto_images[card_verso_image_filename] # Assuming uploaded_recto_images can also contain verso images

        image_to_draw_verso_path = None
        if current_verso_pil_image:
            try:
                # For verso, assume white background for compositing if original is RGBA
                bg_color_tuple_verso = (255, 255, 255) # White background

                # Create a new RGB image with the desired background color
                alpha_composite_img_verso = Image.new('RGB', current_verso_pil_image.size, bg_color_tuple_verso)
                alpha_composite_img_verso.paste(current_verso_pil_image, (0, 0), current_verso_pil_image)

                with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as temp_png_file_verso:
                    image_to_draw_verso_path = temp_png_file_verso.name
                    alpha_composite_img_verso.save(temp_png_file_verso, format='PNG')
                temp_image_files_to_clean.append(image_to_draw_verso_path)
            except Exception as e:
                st.error(f"Erreur lors du compositing de l'image de verso pour la carte {i}: {e}")
                image_to_draw_verso_path = None

        verso_text_for_card = cards_to_process[i].get("texte", "").strip()

        if image_to_draw_verso_path:
            if not verso_text_for_card:
                # No text, image takes up 90% of card width, centered
                try:
                    pil_img_verso = Image.open(image_to_draw_verso_path)
                    original_w_verso, original_h_verso = pil_img_verso.size
                    pil_img_verso.close()

                    img_w_verso = 0.9 * grid.card_w
                    if original_w_verso == 0:
                        raise ValueError("Verso image has zero width")
                    img_h_verso = (original_h_verso / original_w_verso) * img_w_verso

                    max_allowed_h_verso = 0.9 * grid.card_h

                    if img_h_verso > max_allowed_h_verso:
                        img_h_verso = max_allowed_h_verso
                        if original_h_verso == 0:
                            raise ValueError("Verso image has zero height after width check")
                        img_w_verso = (original_w_verso / original_h_verso) * img_h_verso

                    # Calculate positions for centering the *final* sized image
                    img_x_verso = x + (grid.card_w - img_w_verso) / 2
                    img_y_verso = y + (grid.card_h - img_h_verso) / 2

                    c.drawImage(image_to_draw_verso_path, img_x_verso, img_y_verso,
                                width=img_w_verso, height=img_h_verso, preserveAspectRatio=True)
                except Exception as e:
                    st.error(f"Erreur lors du dessin de l'image de verso (90% largeur, sans texte) : {e}")
                    draw_centered_text_in_box(c, x, y, grid.card_w, grid.card_h, "", style_verso)
            else:
                # Text is present, use original image/text layout
                img_h_verso = grid.card_h / 2
                img_w_verso = img_h_verso

                img_x_verso = x + (grid.card_w - img_w_verso) / 2
                img_y_verso = y + ELEMENT_SPACING

                text_box_h_verso = grid.card_h - (3 * ELEMENT_SPACING + img_h_verso)

                text_box_x_verso = x
                text_box_y_verso = img_y_verso + img_h_verso + ELEMENT_SPACING
                text_box_w_verso = grid.card_w

                try:
                    c.drawImage(image_to_draw_verso_path, img_x_verso, img_y_verso,
                                width=img_w_verso, height=img_h_verso, preserveAspectRatio=True)
                except Exception as e:
                    st.error(f"Erreur lors du dessin de l'image de verso (avec texte) : {e}")
                    draw_centered_text_in_box(c, x, y, grid.card_w, grid.card_h, verso_text_for_card, style_verso)
                    continue
                draw_centered_text_in_box(c, text_box_x_verso, text_box_y_verso, text_box_w_verso, text_box_h_verso, verso_text_for_card, style_verso)
        else:
            # No image or image processing failed, draw text in the full card area
            draw_centered_text_in_box(c, x, y, grid.card_w, grid.card_h, verso_text_for_card, style_verso)

    # Removed draw_cut_marks for verso page as requested.
    c.save()

    # Cleanup temporary files created during image processing
    for temp_file in temp_image_files_to_clean:
        try:
            os.remove(temp_file)
        except OSError as e:
            st.warning(f"Erreur lors de la suppression du fichier temporaire {temp_file}: {e}")


# ----------------------------
# Streamlit Application Logic
# ----------------------------
st.title("Générateur de cartes recto/verso imprimables multi-usages")

st.write("Uploadez votre fichier CSV et une archive ZIP contenant les illustrations (facultatif) pour générer 9 cartes recto/verso sur une feuille A4 en pdf.")
st.text("Le contenu du fichier CSV est constitué au maximum de 9 lignes correspondant au nombre de cartes")
st.write(" le format attendu du CSV est le suivant :") 
st.text("ma question1 (couleur_ou_#CODEHEX) ; ma réponse1 ; mon_image_recto.png ; mon_image_verso.png")
st.text("ma question2 (couleur_ou_#CODEHEX) ; ma réponse2")
st.text("etc.")
st.write("(couleur_ou_#CODEHEX) est la couleur du recto de la carte - choix possibles : bleu, rouge, rose, vert, jaune, blanc, gris ou un code hexadécimal de la forme #FF00FF ou #F00.")
st.write("Si aucune couleur n'est indiquée (maquestion1 ; maréponse1) alors la couleur par défaut du recto est le gris (#B3B3B3).")
st.write("Vous pouvez choisir un remplissage complet du recto ou un cadre de 4 mm via l'option ci-dessous.")
st.write("La couleur de fond du verso reste blanche.") 
st.write("Le nom du fichier image dans la 3e colonne du CSV (recto) et 4e colonne (verso) doit correspondre exactement au nom d'un fichier PNG/JPG dans l'archive ZIP.")
st.write("")

st.subheader("Disposition des cartes")
st.info(f"Format portrait (3x3 cartes). Nombre de cartes par page : {NB_CARTES}.")

# Option for recto color style
recto_color_style = st.radio(
    "Style du recto :",
    ("Remplissage (couleur pleine)", "Cadre 4 mm"),
    index=0
)

# CSV Upload
uploaded_csv_file = st.file_uploader("Uploader le fichier CSV", type=["csv"])

# Image Upload for Recto (multiple images via ZIP)
uploaded_recto_images_zip = st.file_uploader("Uploader un fichier ZIP d'images PNG/JPG (facultatif) pour les rectos et versos", type=["zip"])

recto_images_dict = {}
if uploaded_recto_images_zip:
    st.info("Décompression des images...")
    with tempfile.TemporaryDirectory() as tempdir:
        with zipfile.ZipFile(uploaded_recto_images_zip, 'r') as zip_ref:
            zip_ref.extractall(tempdir)
        for filename in os.listdir(tempdir):
            if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
                filepath = os.path.join(tempdir, filename)
                try:
                    img = Image.open(filepath).convert('RGBA') # Convert to RGBA for consistent handling
                    recto_images_dict[filename] = img
                except Exception as e:
                    st.warning(f"Impossible de charger l'image {filename}: {e}")
    if recto_images_dict:
        st.success(f"{len(recto_images_dict)} images chargées depuis le fichier ZIP.")
    else:
        st.warning("Aucune image valide trouvée dans le fichier ZIP.")


if uploaded_csv_file is None:
    st.warning("Veuillez uploader un fichier CSV pour commencer.")
elif uploaded_csv_file is not None:
    # Read CSV content from the uploaded file
    csv_content = uploaded_csv_file.getvalue().decode("utf-8")
    csv_name = uploaded_csv_file.name

    color_name, default_back_color = pick_color_from_filename(csv_name)
    st.info(f"Couleur par défaut : {color_name} (#B3B3B3)")

    cards = read_cards_from_csv(csv_content)
    st.info(f"Lignes lues : {len(cards)} (on utilise les {NB_CARTES} premières)")

    if st.button("Générer le PDF"):
        if cards:
            output_buffer = io.BytesIO()
            # Pass the dictionary of recto and verso images to build_pdf
            build_pdf(
                cards,
                default_back_color,
                output_buffer,
                uploaded_recto_images=recto_images_dict,
                recto_color_style=recto_color_style
            )

            st.success(f"PDF généré : {OUTPUT_PDF}")
            st.download_button(
                label="Télécharger le PDF",
                data=output_buffer.getvalue(),
                file_name=OUTPUT_PDF,
                mime="application/pdf"
            )
        else:
            st.error("Aucune carte n'a pu être lue depuis le fichier CSV. La génération du PDF est annulée.")
st.markdown("---")
st.caption("ℹ️ Documentation et format du fichier CSV : https://github.com/fablegros-ux/flashcard3#readme")
