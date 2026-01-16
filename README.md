# flashcard3
Générateur de cartes recto/verso imprimables (multi-usages)

Importez :

un fichier CSV (obligatoire)

un fichier ZIP d’images (facultatif)

L’application génère un PDF A4 de cartes recto/verso, en orientation portrait ou paysage, avec 9 ou 10 cartes par page selon votre choix.

Format du fichier CSV

Chaque ligne correspond à une carte (jusqu’au nombre sélectionné).
Format d’une ligne :

question (couleur) ; réponse ; image_recto ; image_verso

Exemples :

Ma question (rouge) ; Ma réponse ; recto1.png ; verso1.png

Ma question ; Ma réponse

Ma question (#FF00FF) ; Ma réponse ; recto2.jpg ; verso2.png

Couleur du recto

La couleur se met entre parenthèses après la question :

Couleurs autorisées : bleu, rouge, rose, vert, jaune, blanc

Ou un code hexadécimal : #FF00FF ou #F00

Si aucune couleur n’est indiquée, le recto est bleu par défaut.

Images (optionnel)

Si vous fournissez un ZIP d’images :

les colonnes 3 (recto) et 4 (verso) peuvent contenir le nom exact d’un fichier image présent dans le ZIP

formats acceptés : PNG et JPG/JPEG

le nom doit correspondre au caractère près (majuscules/minuscules comprises)

Conseil : enregistrez le CSV en UTF-8 et utilisez le point-virgule ; comme séparateur.

Auteur Fabrice Legros fablegros@aol.com
