from typing import Union


class Grille:

    def __init__(self,
                 lig: int = 11,
                 col: int = 19,
                 init: Union[int, str] = 0,
                 taille_case: int = 64,
                 taille_marge: int = 10) -> None:
        """
        Constructeur d'une grille de 2D

        Un element de classe Grille est un plateau 2D de dimensions (lig, col) assimilable a une une liste d'une
        liste contenant des caracteres et dont chaque case pouvant être modeliser graphiquement à travers une taille
        de case en pixels en imposant une marge (taille_marge)

        :param lig: le nombre de ligne du plateau
        :param col: le nombre de colonne du plateau
        :param init: le caractere initiale à placer dans toute les cases
        :param taille_case: la taille en pixel d'une case graphiquement
        :param taille_marge: la taille en pixel de la marge que doit posseder une represetation graphique

        """
        self.plateau = [[init] * col for _ in range(lig)]  # --> creaGrille
        self.nb_col = col  # Recuperation du nombre de colonnes
        self.nb_lig = lig  # Recuperation du nombre de lignes
        self.taille = lig * col  # Recuperation de la dimension du plateau a partir des lignes et des colonnes
        self.taille_case = taille_case  # Definie la taille d'une pixel en pixel
        self.taille_marge = taille_marge  # Definie la taille de la marge en pixel

    def dimensions(self) -> tuple:
        """
            Renvoie la taille (longueur et largeur) de la grille

            :return les dimensions du plateau

        """
        return self.nb_lig, self.nb_col

    def diagonale(self) -> list:
        """
            Recupere la diagonale du plateau

            :return: diagonales du plateau

        """
        dim = min(self.dimensions())
        return [self.plateau[i][i] for i in range(dim)]

    def anti_diagonale(self):
        """
            Recupere l'antidiagonale du plateau

            :return: l'antidiagonale du plateau
            :rtype: list

        """
        dim = min(self.dimensions())
        return [self.plateau[i][self.nb_col - i - 1] for i in range(dim)]

    def dimensions_egales(self) -> bool:
        """
            Verifie que le plateau est carré, c'est à dire le nombre de ligne = nombre de colonne

            :return:

        """
        return self.nb_lig == self.nb_col

    def identite_generale(self, val: Union[int or str]) -> bool:
        """
            Verifie si tous les éléments du plateau contiennent une même valeur

            :param val: la valeur à verfier
            :return: un booleen

        """
        return all([all([i == val for i in ligne]) for ligne in self.plateau])

    def affiche(self) -> None:
        """Affiche proprement la grille"""
        for ligne in self.plateau:
            print('|\t', '\t'.join([str(val) for val in ligne]), '\t|')

    def affiche_level(self) -> None:
        """Affiche proprement un niveau"""
        for ligne in self.plateau:
            print(''.join([str(val) for val in ligne]))

    def compteur_de_valeur(self, val: Union[int, str]) -> int:
        """
            Compte le nombre d'occurence d'une valeur dans la grille

            :param val: le valeur qui doit être compté
            :return: le nombre de fois que la valeur apparait dans le plateau


        """
        return sum(ligne.count(val) for ligne in self.plateau)

    # # # # # # # # # # # # # # # methodes geres par les numeros de ligne et/ou colonne # # # # # # # # # # # # # # #

    def ligne(self, x: int) -> list:
        """
            Recupere la ligne selectionnee

            :param x: numero de la ligne
            :return: ligne x du plateau

        """
        return self.plateau[x]

    def colonne(self, x: int) -> list:
        """
            Recupere la colonne selectionnee

            :param x: numero de la colonne
            :return: colonne y du plateau

        """
        return [ligne[x] for ligne in self.plateau]

    def coordonnees_suivantes(self, x: int, y: int, direction: int = 0) -> tuple:
        """
        Renvoie les coordonnees de la case suivante en fonction de la orientation donnee.

        En entrant les coordonnées de la pixel de départ et une orientation, on calcule
        les nouvelles coordonnées par rapport à la orientation si cela est possible
        et on les récupère.

        orientation possible:
            -vers le haut: O

            -vers la droite: 1

            -vers le bas: 2

            -vers la gauche: 3

        :param x: numero de la ligne initiale
        :param y: numero de la colonne initiale
        :param direction: la orientation choisie
        :return: les nouvelles ligne et colonne

        """
        if direction == 0 and x > 0:
            return x - 1, y  # Vers le haut
        if direction == 1 and y < self.nb_col:
            return x, y + 1  # Vers la droite
        if direction == 2 and x < self.nb_lig:
            return x + 1, y  # Vers le bas
        if direction == 3 and y > 0:
            return x, y - 1  # Vers la gauche
        return x, y

    def place(self, x: int, y: int, symbole: Union[str, int]) -> None:
        """
            Place un symbole dans la grille aux coordonnees voulues

            :param x: numero de la ligne où placé le caractere
            :param y: numero de la colonne où placé le caractere
            :param symbole: le caractere à placé

        """
        self.plateau[x][y] = symbole

    def coordonnees_graphiques(self, x: int, y: int, pixel=None) -> tuple:
        """
            Retourne les coordonnees en pixel d'une pixel  a partir de ses coordonnees (x, y)

            :param x: numero de la ligne de la pixel
            :param y: numero de la colonne
            :param pixel: la taille en pixel que l'on utilise
            :return: coordonnées graphiques en pixels

        """
        if pixel is None:
            pixel = self.taille_case
        return self.taille_marge + y * pixel, self.taille_marge + x * pixel

    def retourne_symbole(self, x: int, y: int) -> Union[int, str]:
        """
            Determiner la valeur aux coordonnees (x, y) de la grille

            :param x: le numero de la ligne
            :param y: le numero de la colonne
            :return: le symbole(nombre ou caractere)

        """
        return self.plateau[x][y]

    def numero_case(self, x: int, y: int) -> int:
        """
            Retourne le numero de la case

            Formule de calcul: numero_de_la_ligne * nombre_maximal_de_colonne + numero_de_la_colonne

            :param x: le numero de la ligne
            :param y: le numero de la colonne
            :return: le numero de la case correspondante

        """
        return x * self.nb_col + y

    # # # # # # # # # # # # # # # # # # # methodes geres par le numero de la case # # # # # # # # # # # # # # # # # # #

    def case_suivante(self, case: int, direction: int = 0) -> int:
        """
        Renvoie la pixel suivante en fonction de la orientation donnee.

        En entrant le numero de la pixel de départ et une orientation,
        on determine la nouvelle pixel par rapport à la orientation si
        cela est possible et on la récupère. La détermination de
        la nouvelle pixel passe par l'utilisation des méthodes
        coordonnees_suivantes et et numero_case

        orientation possible:
            -vers le haut: O

            -vers la droite: 1

            -vers le bas: 2

            -vers le haut: 3

        :param case: le numero de la pixel initiale
        :param direction: la orientation choisie
        :return: le numero de la pixel suivante

        """
        lig, col = self.convertir_case(case)
        ligne_suivante, colonne_suivante = self.coordonnees_suivantes(lig, col, direction)
        return self.numero_case(ligne_suivante, colonne_suivante)

    def place_dans_la_case(self, case: int, symbole: Union[int, str]) -> None:
        """
            Place un symbole dans la grille aux coordonnees voulues

            :param case: le numero de la pixel
            :param symbole: le caractere à placer

            """
        lig, col = self.convertir_case(case)
        self.plateau[lig][col] = symbole

    def trouve_ligne(self, case: int) -> list:
        """
            Extrait la ligne de la pixel

            :param case: le numero de la case
            :return: la ligne correspondant à la case

        """
        return self.plateau[self.convertir_case(case)[0]]

    def trouve_colonne(self, case: int) -> list:
        """
            Extrait la colonne de la pixel

            :param case: le numero de la case
            :return: la colonne correspondant à la case

        """
        col = self.convertir_case(case)[1]
        return [ligne[col] for ligne in self.plateau]

    def convertir_case(self, case: int) -> tuple:
        """
        Convertit le numero de pixel vers des coordonnees (ligne,colonne)

        :param case: le numero de la case
        :return: les coordonnees(x, y) associés à cette case

        """
        return case // self.nb_col, case % self.nb_col

    def valeur_case(self, case: int) -> Union[int, str]:
        """
            Retourne le symbole se trouvant dans une case donnee

            :param case: le numero de pixel
            :return: le caractere contenu dans la case

        """
        ligne, colonne = self.convertir_case(case)
        return self.plateau[ligne][colonne]

    def identite(self, case: int, val: Union[int, str]) -> bool:
        """
            Renvoie vrai si la valeur de la case correspond a la valeur prise en parametre

            :param case: le numero de la pixel
            :param val: le caractere à tester
            :return: un booleen

        """
        return self.valeur_case(case) == val

    def trouve_symbole(self, symbole: Union[int, str]) -> list:
        """
            Retourne une liste des numeros de case possedant le meme element

            :param symbole: le caractere à trouver
            :return: une liste des cases contenant le caractere

        """
        return [case for case in range(self.taille) if self.identite(case, symbole)]

    def coordonnees_graphique(self, case: int, pixel=None) -> tuple:
        """
            Retourne les coordonnees en pixel d'une pixel a partir de son numero de pixel

            :param case: le numero de case
            :param pixel: la taille en pixel que l'on utilise
            :return: les coordonnes graphiques de la pixel

        """
        lig, col = self.convertir_case(case)
        return self.coordonnees_graphiques(lig, col, pixel)
