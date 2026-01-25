---

# flashcard3 🎴


---

## Français

### Générateur de cartes recto/verso imprimables (PDF A4)

Application Streamlit permettant de générer des cartes rapidement **recto/verso** multi-usages à partir d’un fichier **CSV** (et d’un ZIP d’images optionnel), puis d’exporter un **PDF A4 composé de 9 cartes au format portrait**.

### 🚀 Fonctionnalités

* Import d’un fichier **CSV** (contenu des cartes)
* Import optionnel d’un **ZIP d’images** (PNG/JPG) pour illustrer recto/verso
* Génération d’un PDF A4 avec cartes **recto/verso** prêtes à imprimer
* Couleur du **recto** définie par carte : nom de couleur prédéfinie ou code hexadécimal

### 📊 Format attendu du CSV

Le CSV contient **au maximum 9 lignes**. Chaque ligne décrit une carte, avec **2 à 4 colonnes** séparées par des points-virgules `;` :

1. **Question** (peut contenir une couleur entre parenthèses)
2. **Réponse**
3. *(optionnel)* **Image recto** (nom de fichier)
4. *(optionnel)* **Image verso** (nom de fichier)

#### Exemples

* **Sans images :** `ma question1 (bleu) ; ma réponse1` (Recto bleu, texte seulement).
* **Avec images :** `ma question1 (#FF00FF) ; ma réponse1 ; img_r.png ; img_v.png`
* **Cas "Pleine Carte" :** Si le nom de l'image recto commence par `pc_` (ex: `pc_image.png`), elle remplit toute la carte. Ne pas mettre de texte au recto dans ce cas.

#### Couleur du recto

Indiquée en colonne 1 entre parenthèses :

* **Noms :** bleu, rouge, rose, vert, jaune, blanc.
* **Hex :** `#FF00FF`, `#F00`, etc.
* Par défaut : **gris**.

### 🖼️ Images (ZIP optionnel)

* Formats : **PNG** (transparence gérée) ou **JPG**.
* **Dimensions conseillées (300 dpi) :** Largeur **~626 px** / Hauteur **~969 px** pour remplir le cadre (4 mm).

### 🛠️ Utilisation

1. Ouvrir l’application Streamlit.
2. Téléverser le fichier **CSV**.
3. *Optionnel :* Téléverser l'archive **ZIP** d'images.
4. Générer et télécharger le PDF.
5. Imprimer (A4) et massicoter !

---

## English

### Printable Double-Sided Flashcard Generator (A4 PDF)

A Streamlit application designed to quickly generate multi-purpose **double-sided** cards from a **CSV** file (and an optional image ZIP). It exports a ready-to-print **A4 PDF containing 9 portrait-format cards**.

### 🚀 Features

* **CSV** file import (card content)
* Optional **Image ZIP** import (PNG/JPG) for front and back illustrations
* A4 PDF generation with **double-sided** cards ready for printing
* Customizable **front color** per card: predefined names or hex codes

### 📊 Expected CSV Format

The CSV must contain **at most 9 lines**. Each line represents one card, with **2 to 4 columns** separated by semicolons `;`:

1. **Question** (can include a color in parentheses)
2. **Answer**
3. *(optional)* **Front Image** (filename)
4. *(optional)* **Back Image** (filename)

#### Examples

* **Text only:** `my question1 (blue) ; my answer1` (Blue front, text on both sides).
* **With images:** `my question1 (#FF00FF) ; my answer1 ; front_img.png ; back_img.png`
* **"Full Card" case:** If the front image filename starts with `pc_` (e.g., `pc_photo.png`), it will fill the entire front side. No text should be provided for the front in this case.

#### Front Side Color

Specified in Column 1 within parentheses:

* **Accepted names:** bleu (blue), rouge (red), rose (pink), vert (green), jaune (yellow), blanc (white).
* **Hex codes:** `#FF00FF`, `#F00`, etc.
* Default color: **grey**.

### 🖼️ Images (Optional ZIP)

* Formats: **PNG** (transparency supported) or **JPG**.
* **Recommended dimensions (300 dpi):** Width **~626 px** / Height **~969 px** to perfectly fit the 4 mm frame.

### 🛠️ How to use

1. Open the Streamlit app.
2. Upload your **CSV** file.
3. *Optional:* Upload the **ZIP** archive containing your images.
4. Generate and download the PDF.
5. Print (A4) and cut!

---

## ⚠️ Limites / Limitations

* **Max cards:** 9.
* **Separator:** Semicolon (`;`).
* **Text length:** Max 50 characters if an illustration is used.

**Auteur / Author:** [Votre Nom/Pseudo]

---

Souhaitez-vous que j'ajoute une section technique sur la manière d'installer l'application localement (pip install, etc.) ?
