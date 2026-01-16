# flashcard3
# Générateur de cartes recto/verso imprimables (PDF A4)

Application Streamlit permettant de générer des cartes **recto/verso** multi-usages à partir d’un fichier **CSV** (et d’un ZIP d’images optionnel), puis d’exporter un **PDF A4 avec des cartes au format portait ou paysage**.

## Fonctionnalités
- Import d’un fichier **CSV** (contenu des cartes)
- Import optionnel d’un **ZIP d’images** (PNG/JPG) pour illustrer recto/verso
- Génération d’un PDF A4 avec cartes **recto/verso** prêtes à imprimer
- Couleur du **recto** par carte : nom de couleur ou code hexadécimal

## Format attendu du CSV

Le CSV contient **au maximum 9 à 10 lignes** (selon le format choisi dans l’application).
Chaque ligne décrit une carte, avec **2 à 4 colonnes** séparées par des points-virgules `;` :

1. **Question** (peut contenir une couleur entre parenthèses)
2. **Réponse**
3. *(optionnel)* **Image recto** (nom de fichier)
4. *(optionnel)* **Image verso** (nom de fichier)

### Exemples

**Sans images**
ma question1 (bleu) ; ma réponse1  
ma question2 ; ma réponse2  

**Avec images**
ma question1 (#FF00FF) ; ma réponse1 ; mon_image_recto.png ; mon_image_verso.png  
ma question2 (vert) ; ma réponse2 ; photo1.jpg ; photo2.jpg  

### Couleur du recto
La couleur est indiquée dans la **colonne 1**, entre parenthèses :

- Couleurs acceptées : `bleu`, `rouge`, `rose`, `vert`, `jaune`, `blanc`
- Ou un code hexadécimal : `#FF00FF`, `#F00`, etc.
- Si aucune couleur n’est indiquée (ex. `ma question ; ma réponse`), la couleur par défaut du recto est **bleu**.

## Images (ZIP optionnel)
Si tu fournis un fichier ZIP d’images :
- Les images doivent être au format **PNG** ou **JPG**
- Le nom indiqué en **colonne 3 (recto)** et **colonne 4 (verso)** doit correspondre **exactement** à un nom de fichier présent dans le ZIP (respect des majuscules/minuscules inclus).

## Utilisation
1. Ouvre l’application Streamlit
2. Uploade ton fichier CSV
3. (Optionnel) Uploade un ZIP d’images
4. Choisis le format (horizontal/vertical)
5. Génère et télécharge le PDF

## Limites connues
- Nombre maximal de cartes : **9 à 10** (selon le format sélectionné)
- Les séparateurs attendus dans le CSV sont des `;`



## Auteur
Fabrice Legros fablegros(at)gmail.com

