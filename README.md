# flashcard3
# Générateur de cartes recto/verso imprimables (PDF A4)

Application Streamlit permettant de générer des cartes rapidement **recto/verso** multi-usages à partir d’un fichier **CSV** (et d’un ZIP d’images optionnel), puis d’exporter un **PDF A4 composé de 9 cartes au format portrait**.

## Fonctionnalités
- Import d’un fichier **CSV** (contenu des cartes)
- Import optionnel d’un **ZIP d’images** (PNG/JPG) pour illustrer recto/verso
- Génération d’un PDF A4 avec cartes **recto/verso** prêtes à imprimer
- Couleur du **recto** définie par carte : nom de couleur prédéfinie ou code hexadécimal

## Format attendu du CSV

Le CSV contient **au maximum 9 lignes**.
Chaque ligne décrit une carte, avec **2 à 4 colonnes** séparées par des points-virgules `;` :

1. **Question** (peut contenir une couleur entre parenthèses)
2. **Réponse**
3. *(optionnel)* **Image recto** (nom de fichier)
4. *(optionnel)* **Image verso** (nom de fichier)

### Exemples

**Sans images**
1. ma question1 (bleu) ; ma réponse1     -> uniquement du texte sur le recto et le verso. Le recto est de couleur bleu 
2. ; mon texte_verso                     -> recto vierge de couleur grise (couleur par défaut) et du texte sur  le verso 
3. ;;                                    -> recto vierge de couleur grise (couleur par défaut) et verso vierge de couleur blanche  

**Avec images**
1. ma question1 (#FF00FF) ; ma réponse1 ; mon_image_recto.png ; mon_image_verso.png     -> recto : texte et image avec une couleur recto (#FF00FF) et verso : texte et image sur fond blanc  
2. ma question2 (vert);; photo_recto.jpg ; photo_photo_verso.jpg                        -> recto : texte et image avec une couleur recto vert et verso : image centrée
3. ;;; mon_illustration_verso.png                                                       -> recto : fond vierge de couleur grise et verso : image centrée             

**Cas particulier**
Si une illustration **du recto** possède un nom de fichier commençant par pc_ (exemple pc_mon_image_recto.png) alors elle est destinée à remplir le recto entier et il ne doit pas y avoir de texte prévu pour le reco 
;mon_texte_verso;pc_mon_image_recto.png

### Couleur du recto
La couleur du recto est indiquée dans la **colonne 1**, entre parenthèses :

- Couleurs acceptées : `bleu`, `rouge`, `rose`, `vert`, `jaune`, `blanc`
- Ou un code hexadécimal : `#FF00FF`, `#F00`, etc. (cf. https://htmlcolorcodes.com/fr/ pour définir la couleur désirée)
- Si aucune couleur n’est indiquée (ex. `ma question ; ma réponse`), la couleur par défaut du recto est **gris**.

## Images (ZIP optionnel)
Fournir un fichier ZIP d’images :
- Les images doivent être au format **PNG** ou **JPG**
- la transparence du format **PNG** est pris en charge
- Le nom indiqué en **colonne 3 (recto)** et **colonne 4 (verso)** doit correspondre **exactement** à un nom de fichier présent dans le ZIP (respect des majuscules/minuscules inclus).

### Dimensions conseillées (300 dpi)
Pour **remplir complètement l’intérieur du cadre (mode "Cadre 4 mm")**, utiliser des images au format portrait avec les dimensions suivantes :
- **Largeur : ~626 px**
- **Hauteur : ~969 px**

Ces valeurs correspondent à la zone utile de la carte (A4, marges, espacements, cadre 4 mm) à **300 dpi**.

## Utilisation
1. Ouvrir l’application Streamlit
2. Téléverser ton fichier CSV
3. Optionnel : téléverser une archive ZIP contenant les images
4. Générer et télécharger le PDF
5. Imprimer et massicoter ;-)

## Limites connues
- Nombre maximal de cartes : **9**
- Les séparateurs attendus dans le CSV sont des `;`
- Le texte ne doit pas contenir plus de 50 signes si une illustration est associée.



## Auteur
Fabrice Legros fablegros(at)gmail.com
