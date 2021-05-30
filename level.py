from grille import Grille
import copy


class Level(Grille):

    def __init__(self, taille_case=64, taille_marge=10, file="level/level0.sok"):
        """
        Constructeur d'un niveau de sokoban
        Ouvre un fichier 'file'
        Recupere le nombre de lignes et de colonnes de la grille
        Converti le fichier ouvert en une liste imbriquee
        """
        with open(file, "r") as f:
            # Conversion du fichier en tableau :
            lines = f.readlines()
        # Recuperer les dimensions du plateau (1ere ligne du fichier .sok) pour les utiliser en parametre de la grille :
        col, lig = lines[0].split()
        # Initialisation de la grille vide avec les dimensiosn du fichier :
        Grille.__init__(self, int(lig), int(col), " ", taille_case, taille_marge)
        # Conversion de chaque ligne du fichier au format tab en lignes de la grille de jeu :
        self.plateau = [list(line.replace("\n", "")) for line in lines[1:]]
        self.plateau_initiale = copy.deepcopy(self.plateau)
        self.historique = []
        self.plateau_initiale = copy.deepcopy(self.plateau)

    def dernier_plateau(self) -> None:
        """
            Garde le precedent plateau de jeu en memoire afin de pouvoir y retourner
        """
        if len(self.historique) > 0:
            self.plateau = self.historique.pop()

    def ajout_historique(self, plateau: list) -> None:
        """
            Enregistre l'ensemble des plateaux de jeux precedents

            :param plateau: une liste

        """
        self.historique.append(copy.deepcopy(plateau))

    def reset(self) -> None:
        """
            Reinitialise le niveau par defaut
        """
        self.plateau = copy.deepcopy(self.plateau_initiale)
        del self.historique[:]

    def est_un_joueur(self, case: int) -> bool:
        """
            Teste si la case selectionnee correspond au joueur

            "+" =  joueur sur un emplacement de caisse,
            "@" = joueur pas sur un emplacement de caisse

            :param case: le numero de la case à tester
            :return: un booléen
        """
        return self.identite(case, "@") or self.identite(case, "+")

    def est_un_mur(self, case: int) -> bool:
        """
            Teste si la case selectionnee correspond a un mur

            "#" = un mur

            :param case: le numero de la case à tester
            :return: un booléen

        """
        return self.identite(case, "#")

    def est_une_boite(self, case: int) -> bool:
        """
            Renvoie vrai si la pixel selectionnee correspond a une caisse

            "*" = caisse sur un emplacement de caisse,
            "$" = caisse pas sur un emplacement de caisse

            :param case: le numero de la case à tester
            :return: un booléen

        """
        return self.identite(case, "$") or self.identite(case, "*")

    def est_une_case_vide(self, case: int) -> bool:
        """
            Renvoie vrai si la pixel selectionnee est vide

            " " = vide

            :param case: le numero de la case à tester
            :return: un booléen
        """
        return self.identite(case, " ")

    def est_un_objectif(self, case: int) -> bool:
        """
            Renvoie vrai si la pixel selectionnee correspond a un emplacement de caisse

            "." = objectif

            :param case: le numero de la case à tester
            :return: un booléen

        """
        return self.identite(case, ".")

    def sont_active(self) -> int:
        """
            Renvoie le nombre de caisses sur un emplacement de caisse

            :return: le nombre de caisse sur un emplacement

        """
        return self.compteur_de_valeur("*")

    def position_joueur(self) -> int:
        """
            Trouve la position du joueur

            :return: le numero de la case du joueur

        """

        if self.compteur_de_valeur("@") == 1:
            return self.trouve_symbole("@")[0]
        elif self.compteur_de_valeur("+") == 1:
            return self.trouve_symbole("+")[0]

    def nombre_de_boites(self) -> int:
        """
            Renvoie le nombre total de caisses
            
            :return: le nombre de caisse contenu dans le plateau
        """
        return self.compteur_de_valeur("*") + self.compteur_de_valeur("$")

    def victoire(self) -> bool:
        """
            Renvoie vrai si nombre total de caisses = nombre de caisses sur emplacement de caisse
            
            :return booleen 
        """
        return self.nombre_de_boites() == self.sont_active()

    def mouvement_vers_case_vide(self, orientation: int) -> None:
        """
            Deplace le joueur en fonction d'une orientation donnee, a condition que la case d'arrivee soit vide
        """
        case_player = self.position_joueur()
        case_suivante = self.case_suivante(case_player, orientation)

        # Si la case est vide
        if self.est_une_case_vide(case_suivante):
            self.place_dans_la_case(case_suivante, "@")

            if self.identite(case_player, "@"):
                self.place_dans_la_case(case_player, " ")

            elif self.identite(case_player, "+"):
                self.place_dans_la_case(case_player, ".")

        # Si la case est un objectif
        elif self.est_un_objectif(case_suivante):
            self.place_dans_la_case(case_suivante, "+")
            if self.identite(case_player, "@"):
                self.place_dans_la_case(case_player, " ")

            elif self.identite(case_player, "+"):
                self.place_dans_la_case(case_player, ".")

    def mouvement_boite(self, orientation: int) -> None:
        """
            Deplace le personnage et une caise dans une orientation donnee
        """
        case_player = self.position_joueur()
        case_suivante = self.case_suivante(case_player, orientation)
        case_suivante_box = self.case_suivante(case_suivante, orientation)

        if self.est_une_case_vide(case_suivante_box) or self.est_un_objectif(case_suivante_box):

            if self.est_une_case_vide(case_suivante_box):
                self.place_dans_la_case(case_suivante_box, "$")

            elif self.est_un_objectif(case_suivante_box):
                self.place_dans_la_case(case_suivante_box, "*")

            if self.identite(case_suivante, "*"):
                self.place_dans_la_case(case_suivante, "+")

            elif self.identite(case_suivante, "$"):
                self.place_dans_la_case(case_suivante, "@")

            if self.identite(case_player, "@"):
                self.place_dans_la_case(case_player, " ")

            elif self.identite(case_player, "+"):
                self.place_dans_la_case(case_player, ".")

    def mouvement_du_personnage(self, orientation: str) -> None:
        """
        Deplace le joueur (et les caisses)
        Si la case d'arrivee est vide --> deplace le joueur dans la case
        Si la case d'arrivee est une caisse --> pousse la caisse et deplace le joueur dans la case
        (sauf si la case apres la caisse est un mur ou une autre caisse)
        """
        case_player = self.position_joueur()
        self.ajout_historique(self.plateau)
        deplacements = {"h": 0, "d": 1, "b": 2, "g": 3}
        if orientation in deplacements:
            case_suivante = self.case_suivante(case_player, deplacements[orientation])
            # si la case est vide ou un objectif :
            if self.est_une_case_vide(case_suivante) or self.est_un_objectif(case_suivante):
                self.mouvement_vers_case_vide(deplacements[orientation])

            # si la case est une boite :
            elif self.est_une_boite(case_suivante):
                self.mouvement_boite(deplacements[orientation])
