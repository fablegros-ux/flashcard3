# flashcard3  
### Générateur de cartes recto/verso imprimables (PDF A4)  
**Printable double-sided flashcard generator (A4 PDF)**

---

## Fonctionnalités  
**Features**

- Import d’un fichier **CSV** (contenu des cartes)  
  *Upload a **CSV file** (card content)*

- Import optionnel d’un **ZIP d’images** (PNG/JPG) pour illustrer recto/verso  
  *Optional **ZIP file** of images (PNG/JPG) for front/back illustration*

- Génération d’un PDF A4 avec cartes **recto/verso** prêtes à imprimer  
  *A4 PDF generation with double-sided cards ready to print*

- Couleur du **recto** définie par carte : nom de couleur prédéfinie ou code hexadécimal  
  *Front color defined per card: predefined color name or hexadecimal code*

---

## Format attendu du CSV  
**Expected CSV format**

Le CSV contient **au maximum 9 lignes**.  
Chaque ligne décrit une carte, avec **2 à 4 colonnes**, séparées par des points-virgules `;` :

1. **Question** (peut contenir une couleur entre parenthèses)  
2. **Réponse**  
3. *(optionnel)* **Image recto** (nom de fichier)  
4. *(optionnel)* **Image verso** (nom de fichier)

---

**The CSV may contain up to 9 lines.**  
Each line defines a card with **2 to 4 columns**, separated by semicolons `;`:

1. **Question** (may include a color in parentheses)  
2. **Answer**  
3. *(optional)* **Front image** (filename)  
4. *(optional)* **Back image** (filename)

---

### Exemples / Examples

#### Sans images / Without images

```csv
ma question1 (bleu); ma réponse1
; mon texte_verso
;;
