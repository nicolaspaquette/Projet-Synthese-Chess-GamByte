# Projet Synthèse: Chess GamByte

### Sommaire
Chess GamByte est une plateforme de jeu d'échec développée en python. 
2 modes de jeu sont disponibles:
- Humain contre Humain
- Humain contre Ordinateur

Avant de commencer, l'utilisateur doit choisir sa couleur de pièce ou peut décider de faire une sélection aléatoire. 

Tous les coups légaux sont intégrés dans le jeu:
- En passant
- Castling
- Promotion des pions

Des informations à propos du tour du joueur et des mises en échecs sont disponibles en haut de l'échiquier.

Il est possible de visualiser les coups précédemment joués dans la partie en utilisant le menu de droite lors d'une partie.

Une base de données est intégrée au projet afin de pouvoir observer toutes les parties terminées.

### Installation
Le téléchargement de Python sur l'ordinateur est nécessaire 
https://www.python.org/

MongoDB doit être installé afin d'enregistrer localement les informations des parties jouées.
https://www.mongodb.com/
Dans l'installation, comprendre le logiciel MongoDB Compass qui permet la visualisation des données locales

Dans un éditeur de code, comme Visual Studio Code
Installation des libraries nécessaires au bon fonctionnement dans l'invite de commande avec pip:
- **pip install pygame**
- **pip install pymongo**

Pygame: librarie d'affichage graphique pour programmation de jeu
PyMongo: utilisation de la base de données Mongo

Il faut exécuter le fichier **main** dans le dossier **Dev** pour lancer la fenêtre de jeu .

### Utilisation

À partir du menu principal, il y a 3 boutons:
- **Play vs Human**
- **Play vs AI**
- **Game History**

Pour les 2 premiers boutons qui lance une partie, 3 autres boutons vont apparaître pour la sélection de couleur:
- **White**
- **Random**
- **Black**

Après que le choix est fait, le partie va débuter avec le joueur ayant les pièces **blanches**.

**Pour jouer:**
*La couleur du joueur ayant son tour actuellement sera indiqué en haut du jeu*

Lorsque l'on fait un clic gauche de souris sur une pièce que le joueur actuel possède,
des **petits ronds verts** vont apparaître aux cases disponibles de cette pièce

Il suffit d'effectuer un autre clic gauche sur une des cases ayant un cercle vert pour effectuer le mouvement.

Si il y a un échec ou échec et mat, l'information va être indiqué dans le côté droit en haut de l'échiquier.

**Visualisation des coups joués:**
Le dernier coup joué s'affichera en bas à gauche de l'écran et la liste de tous les coups joués est présente
dans le grand carré noir vers la droite.

Il est possible de naviguer dans la liste et de voir tous les coups avec les 4 boutons:
- **<<** : Revenir au premier coup de la partie
- **<** : Reculer d'un seul coup
- **>** : Avancer d'un seul coup
- **>>**: Revenir à la position actuelle de la partie

**Fin de partie et retour**
Lors d'un échec et mat ou d'un abandon grâce au bouton vers la droite en bas, **Forfeit Game**, 
le bouton **Main Menu** apparaîtra pour revenir au menu principal.

À ce moment, la partie sera sauvegardée dans la base de donnée automatiquement

**Game History, visualisation des anciennes parties**:
Avec le bouton **Game History** du menu princiapl, vous aurez accès aux informations des parties précédantes:
- Date
- Résultat
- Couleur du gagnant
- Nombre de coups joués
- Bouton permettant de visualiser la partie spécifiquement

Après avoir faire un clic gauche sur le bouton de la partie, vous verrez le premier coup de la partie.
Il est ensuite possible d'utiliser les 4 boutons pour naviguer parmis toutes les positions.

Le bouton **Main Menu** permet de revenir au menu principal.

### Références
- Pour l'utilisation de 'heat maps' donnant aux pièces des cases spécifiques étant généralement bénéfiques
https://www.chessprogramming.org/Simplified_Evaluation_Function

- Chaîne Youtube de Sebastian Lague: explication de l'algorithme minimax et de bonnes pratiques en programmation de jeu d'échec
https://www.youtube.com/watch?v=U4ogK0MIzqk&list=LL&index=36&t=557s
https://www.youtube.com/watch?v=l-hh51ncgDI&list=LL&index=35

### Remerciements
J'aimerais remercier M. Monty pour sa gentillesse et son ouverture en m'aidant à trouver certains problèmes cryptiques au cours du développement.

Merci aussi à M. Demers pour son intérêt envers mon projet et à sa passion de l'enseignement de l'informatique, qui se transmet à ses étudiants.

### Licence

Copyright <2021> <Nicolas Paquette>

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.