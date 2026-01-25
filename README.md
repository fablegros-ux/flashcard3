flashcard3

Français | English
Français
Générateur de cartes recto/verso imprimables (PDF A4)

Application Streamlit permettant de générer des cartes rapidement recto/verso multi-usages à partir d’un fichier CSV (et d’un ZIP d’images optionnel), puis d’exporter un PDF A4 composé de 9 cartes au format portrait.
🚀 Fonctionnalités

    Import d’un fichier CSV (contenu des cartes)

    Import optionnel d’un ZIP d’images (PNG/JPG) pour illustrer recto/verso

    Génération d’un PDF A4 avec cartes recto/verso prêtes à imprimer

    Couleur du recto définie par carte : nom de couleur prédéfinie ou code hexadécimal

📊 Format attendu du CSV

Le CSV contient au maximum 9 lignes. Chaque ligne décrit une carte, avec 2 à 4 colonnes séparées par des points-virgules (;) :

    Question (peut contenir une couleur entre parenthèses)

    Réponse

    (optionnel) Image recto (nom de fichier)

    (optionnel) Image verso (nom de fichier)

Exemples

Sans images :

    ma question1 (bleu) ; ma réponse1 -> Texte recto/verso. Recto de couleur bleu.

    ; mon texte_verso -> Recto gris (défaut) et texte au verso.

    ;; -> Recto gris et verso blanc, les deux vierges.

Avec images :

    ma question1 (#FF00FF) ; ma réponse1 ; image_r.png ; image_v.png -> Texte + image sur les deux faces.

    ma question2 (vert);; photo_r.jpg ; photo_v.jpg -> Recto : texte + image. Verso : image centrée.

Cas particulier (Plein Cadre) : Si le nom de l'image recto commence par pc_ (ex: pc_image.png), elle remplit tout le recto. Il ne doit pas y avoir de texte associé au recto. ; texte_verso ; pc_image_recto.png
🎨 Couleur du recto

Indiquée en colonne 1 entre parenthèses :

    Noms acceptés : bleu, rouge, rose, vert, jaune, blanc.

    Hexadécimal : #FF00FF, #F00, etc.

    Par défaut : Gris.

🖼️ Images (ZIP optionnel)

    Formats : PNG ou JPG (transparence PNG supportée).

    Le nom dans le CSV doit correspondre exactement au fichier dans le ZIP.

    Dimensions conseillées (300 dpi) : Pour le mode "Cadre 4 mm", utiliser 626 x 969 px (portrait).

English
Printable Double-Sided Flashcard Generator (A4 PDF)

A Streamlit application to quickly generate multi-purpose double-sided cards from a CSV file (and an optional image ZIP), exporting a ready-to-print A4 PDF with 9 portrait cards.
🚀 Features

    CSV file import (card content)

    Optional Image ZIP import (PNG/JPG) for front/back illustrations

    A4 PDF generation with double-sided layout

    Customizable front color per card: predefined names or hex codes

📊 CSV Format

The CSV must contain a maximum of 9 rows. Each row uses 2 to 4 columns separated by semicolons (;):

    Question (can include a color in parentheses)

    Answer

    (optional) Front Image (filename)

    (optional) Back Image (filename)

Examples

Without images:

    question1 (blue) ; answer1 -> Text on both sides. Front is blue.

    ; back_text -> Blank grey front (default) and text on the back.

With images:

    q1 (#FF00FF) ; a1 ; img_f.png ; img_b.png -> Text + image on both sides.

    ;;; back_illustration.png -> Grey front and centered image on the back.

Special Case (Full Frame): If the front image filename starts with pc_ (e.g., pc_photo.png), it will fill the entire front side. No front text should be provided. ; back_text ; pc_front_image.png
🎨 Front Color

Specified in column 1 within parentheses:

    Accepted names: bleu, rouge, rose, vert, jaune, blanc (French names).

    Hex code: #FF00FF, #F00, etc.

    Default: Grey.

🖼️ Images (Optional ZIP)

    Formats: PNG or JPG (PNG transparency supported).

    Filenames in the CSV must exactly match those in the ZIP (case-sensitive).

    Recommended Dimensions (300 dpi): For the "4mm Frame" mode, use 626 x 969 px (portrait).

🛠️ Utilisation / Usage

    Ouvrir l’application / Open the app.

    Téléverser le CSV / Upload your CSV.

    (Optionnel) Téléverser le ZIP d'images / (Optional) Upload the image ZIP.

    Générer et télécharger le PDF / Generate and download the PDF.

    Imprimer et massicoter ! / Print and cut!

⚠️ Limites / Limitations

    Max 9 cartes / cards.

    Séparateur CSV : ;

    Max 50 signes (caractères) si une image est présente / 50 characters max if an image is included.

👤 Auteur / Author

[Ton Nom / Your Name]
