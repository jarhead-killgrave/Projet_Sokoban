from grille import Grille
from level import Level


if __name__ == "__main__":
    ####### Test du module grille #######
    g = Grille(10, 10)
    print(g.plateau)
    print(g.nb_col)
    print(g.nb_lig)
    print(g.taille)
    print(g.ligne(1))
    print(g.colonne(1))
    print(g.dimensions())
    print(g.diagonale())
    print(g.anti_diagonale())
    print(g.dimensions_egales())
    g.place(5, 5, 'A')
    g.place_dans_la_case(25, 'A')
    g.affiche()
    print(g.compteur_de_valeur('A'))
    print(g.coordonnees_suivantes(5, 4, 0))
    print(g.coordonnees_suivantes(5, 4, 1))
    print(g.coordonnees_suivantes(5, 4, 2))
    print(g.coordonnees_suivantes(5, 4, 3))
    print(g.retourne_symbole(5, 5))
    print(g.identite_generale(0))
    print(g.trouve_ligne(25))
    print(g.trouve_colonne(25))
    print(g.convertir_case(25))
    print(g.valeur_case(25))
    print(g.trouve_symbole('A'))
    print(g.identite(25, 'A'))
    print(g.case_suivante(25, 3))
    print(g.coordonnees_graphiques(0, 0))


    ###################### Test du module level ########################


    # Importer le niveau par defaut et l'afficher :
    level0 = Level()
    level0.affiche_level()
    print(level0.plateau)  # affiche la liste imbriquee du niveau par defaut
    Grille.affiche(level0)  # affiche le niveau par defaut pas joliment
    Grille.affiche_level(level0)  # afficher proprement le niveau par defaut

    # Importer le niveau 1 et l'afficher :
    level1 = Level(file="level/level1.sok")
    print(level1.plateau)  # affiche la liste imbriquee du niveau par defaut
    Grille.affiche(level1)  # affiche le niveau 1 pas joliment
    Grille.affiche_level(level1)  # afficher proprement le niveau 1

    # Tests des fonctions
    print(level1.est_un_joueur(17))  # la case 17 correspond au joueur
    print(level1.est_un_joueur(25))  # la case 25 n'est pas un joueur
    print(level1.est_un_mur(16))  # la case 16 est un mur
    print(level1.est_un_mur(30))  # la case 30 n'est pas un mur
    print(level1.est_une_boite(19))  # la case 19 est une caisse
    print(level1.est_une_boite(4))  # la case 4 n'est pas une caisse
    print(level1.est_une_case_vide(18))  # la case 18 est libre
    print(level1.est_une_case_vide(19))  # la case 19 est occupee
    print(level1.est_un_objectif(34))  # la case 34 est un emplacement de caisse
    print(level1.nombre_de_boites())  # affiche le nombre de caisses de level

    ###################Test de la resolution d'un niveau en console############################
    while True:
        level1.affiche_level()
        direction = input("Quelle mouvement voulait vous faire(h,b,d,g) ? 1 pour arreter, 'u' pour retourner en "
                          "arriere : ")
        if direction == "1":
            break
        elif direction == "u":
            level1.dernier_plateau()

        elif direction == "r":
            level1.reset()

        else:
            level1.mouvement_du_personnage(direction)
            if level1.victoire():
                print("vous avez gagné")
                break
            

