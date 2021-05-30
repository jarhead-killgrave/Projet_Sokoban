import copy
import os
import sys
import time
from typing import Union
from pytube import Y
import pygame
from pygame import Surface
from pygame.event import Event
from pygame.surface import SurfaceType

import solver
from level import Level
from multimedia import Audio
from multimedia import Image

# # # # # # # # # # # # # # # # # # # # Initialisation des evenements utilisateur # # # # # # # # # # # # # # # # # # #

JOUER = pygame.USEREVENT + 1  # Lancer le jeu
GO_MENU = pygame.USEREVENT + 2  # Aller au menu 
NIVEAUX = pygame.USEREVENT + 3  # Aller à la selection des niveaux
ECRAN_FIN = pygame.USEREVENT + 4  # Fin de la resolution de tous les niveaux
RUN_SOLUTION = pygame.USEREVENT + 5  # Lancer la recherche de solution de l'IA
AUTOMATIQUE = pygame.USEREVENT + 6  # Lancer le solveur

# # # # # # # # # # # # # # # # # # # # Initialisation des polices d ecriture # # # # # # # # # # # # # # # # # # # # #

title_font = pygame.font.SysFont("comicsansms", 46)
font = pygame.font.SysFont("comicsansms", 36)
tip_font = pygame.font.SysFont("gotham", 26)
text = title_font.render("A Sokoban Adventure", True, (255, 255, 255))


class Couche:
    def __init__(self, screen: Union[Surface, SurfaceType]):
        """
        Constructeur d'une couche de jeu

        Une couche de jeu est un élément qui permet de modeliser l'état
        :param screen:
        """
        self.screen = screen
        self.width, self.height = screen.get_size()
        self.son = Audio()

    def react_to(self, event: Event) -> None:
        if event.type == pygame.QUIT:
            sys.exit()
        else:
            self.son.play(event)

    def draw(self):
        self.screen.fill((153, 204, 255))


#################################### Ecran du menu principal ####################################

class Menu(Couche):

    def __init__(self, screen: Union[Surface, SurfaceType]):
        """ Constructeur de la frame gerant le menu

        A l'initialisation recuperer l'ecran, initialiser et dessiner
        les rectangles qui definissent les boutons
        """
        Couche.__init__(self, screen)
        self.bouton_token = 0
        self.rect_B1 = pygame.Rect(self.width / 10, self.height / 2 - 120, 160, 60)
        self.rect_B2 = pygame.Rect(self.width / 10, self.height / 2, 160, 60)
        self.rect_B3 = pygame.Rect(self.width / 10, self.height / 2 + 120, 160, 60)
        self.deco = pygame.image.load("graphiques/caisse.png").convert()

        # liste des rectangles
        self.liste_rect = [self.rect_B1, self.rect_B2, self.rect_B3]

    def react_to(self, event):
        """ Methode qui permet de gerer les evenements qui sont captes """
        Couche.react_to(self, event)
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.bouton_token = (self.bouton_token - 1) % len(self.liste_rect)
            elif event.key == pygame.K_DOWN:
                self.bouton_token = (self.bouton_token + 1) % len(self.liste_rect)
            elif event.key == pygame.K_SPACE or event.key == pygame.K_RETURN:
                if self.liste_rect[self.bouton_token] == self.rect_B1:
                    pygame.event.post(pygame.event.Event(JOUER))
                elif self.liste_rect[self.bouton_token] == self.rect_B2:
                    pygame.event.post(pygame.event.Event(NIVEAUX))
                elif self.liste_rect[self.bouton_token] == self.rect_B3:
                    sys.exit()

    def draw(self):
        """ Methode permettant de dessiner sur l'ecran de jeu """
        Couche.draw(self)

        self.screen.blit(text, (400 - text.get_width() // 2, 30))
        self.screen.blit(self.deco, (320, 125))

        couleur_principale = [(0, 204, 0), (255, 128, 0), (128, 0, 255)]
        couleur_secondaire = [(38, 77, 0), (77, 38, 0), (57, 0, 77)]

        pygame.draw.rect(self.screen, couleur_secondaire[self.bouton_token], self.liste_rect[self.bouton_token])

        for i in range(len(self.liste_rect)):
            if i != self.bouton_token:
                pygame.draw.rect(self.screen, couleur_principale[i], self.liste_rect[i])

        text_B1 = font.render('Jouer', True, (255, 255, 255))
        self.screen.blit(text_B1, (self.width / 10 + 30, self.height / 2 - 120))

        text_B2 = font.render('Niveaux', True, (255, 255, 255))
        self.screen.blit(text_B2, (self.width / 10 + 12, self.height / 2))

        text_B3 = font.render('Quitter', True, (255, 255, 255))
        self.screen.blit(text_B3, (self.width / 10 + 14, self.height / 2 + 120))


#################################### Ecran de jeu ####################################

class Jouer(Couche):
    def __init__(self, screen: Union[Surface, SurfaceType], lvl: int = 0):
        """ Constructeur de la frame gerant une partie de jeu

        A l'initialisation recuperer l'ecran,
        initialiser le fichier qui permettra la construction graphique,
        recuperer le niveau a dessiner
        """
        Couche.__init__(self, screen)
        self.niveau = lvl
        self.construct = Level(file="level/level{}.sok".format(self.niveau))
        self.conversion = Image()
        self.score = 0
        self.nombre_coups = 0
        self.nombre_coups_total = 0
        self.touche = {pygame.K_RIGHT: "d",
                       pygame.K_d: "d",
                       pygame.K_LEFT: "g",
                       pygame.K_q: "g",
                       pygame.K_UP: "h",
                       pygame.K_z: "h",
                       pygame.K_DOWN: "b",
                       pygame.K_s: "b"
                       }

    def react_to(self, event):
        """ Methode qui permet de gerer les evenements qui sont captes """
        Couche.react_to(self, event)
        if event.type == pygame.KEYDOWN:
            if event.key in self.touche:
                self.construct.mouvement_du_personnage(self.touche[event.key])
                self.nombre_coups += 1
                self.nombre_coups_total += 1

            elif event.key == pygame.K_ESCAPE:
                pygame.event.post(pygame.event.Event(GO_MENU))
                self.nombre_coups_total = 0

            elif event.key == pygame.K_r:
                self.construct.reset()
            elif event.key == pygame.K_u:
                self.construct.dernier_plateau()
                self.nombre_coups += 1
                self.nombre_coups_total += 1

            elif event.key == pygame.K_p:
                pygame.event.post(pygame.event.Event(RUN_SOLUTION))

        if self.construct.victoire():
            self.niveau += 1
            self.score += 1
            self.nombre_coups = 0
            if "level{}.sok".format(self.niveau) in os.listdir("level"):
                self.construct = Level(file="level/level{}.sok".format(self.niveau))
            else:
                self.niveau = 0
                pygame.event.post(pygame.event.Event(ECRAN_FIN))

    def draw(self):
        """ Methode permettant de dessiner sur l'ecran de jeu """
        Couche.draw(self)
        self.conversion.affichage(self.construct.plateau, self.screen)

        score = tip_font.render("Score : " + str(self.score) + " niveau(x) complétés", True, (142, 142, 142))
        coups = tip_font.render("Nombre de coups : " + str(self.nombre_coups), True, (142, 142, 142))
        coupsTotal = tip_font.render("Nombre de coups total : " + str(self.nombre_coups_total), True, (142, 142, 142))
        tip1 = tip_font.render("Appuyez sur ECHAP pour retourner au menu", True, (138, 101, 56))
        tip2 = tip_font.render("Appuyez sur R pour recommencer le niveau", True, (138, 101, 56))
        tip3 = tip_font.render("Appuyez sur U pour revenir au coups précédent", True, (138, 101, 56))
        self.screen.blit(score, (self.width / 2 + 100, self.height / 2 + 150))
        self.screen.blit(tip1, (self.width / 25, self.height / 2 + 150))
        self.screen.blit(tip2, (self.width / 25, self.height / 2 + 200))
        self.screen.blit(tip3, (self.width / 25, self.height / 2 + 250))
        self.screen.blit(coups, (self.width / 2 + 100, self.height / 2 + 200))
        self.screen.blit(coupsTotal, (self.width / 2 + 100, self.height / 2 + 250))


#################################### Ecran du solveur automatique ####################################

class Resolution(Couche):

    def __init__(self, screen: Union[Surface, SurfaceType], lvl: int = 0):
        """ Initialisation de la frame gerant la resolution des niveaux """
        Couche.__init__(self, screen)
        self.niveau = lvl
        self.construct = Level(file="level/level{}.sok".format(self.niveau))
        self.solution = solver.aStarSearch(solver.transferToGameState(copy.deepcopy(self.construct.plateau)))
        self.dico_solutions = {
            4: ["g", "b", "b", "g", "d", "d", "b", "g", "g", "g", "d", "h", "g", "d", "d", "h", "h", "g", "g", "b", "b",
                "h", "h", "g", "g", "b", "b", "h", "d", "h", "d", "d", "b", "d", "b", "g", "h", "g", "g", "h", "g",
                "b"],
            5: ["b", "g", "g", "g", "g", "d", "d", "d", "b", "d", "d", "d", "b", "g", "g", "b", "g", "g", "g", "g", "g",
                "g", "g", "h", "d", "d", "d", "h", "h", "g", "g", "g"],
            6: ['g', 'b', 'b', 'd', 'h', 'd', 'g', 'h', 'g', 'h', 'd', 'd', 'd', 'd', 'd', 'd', 'd', 'h', 'd', 'b', 'g',
                'b', 'd', 'h', 'd', 'b', 'g', 'b', 'd', 'd', 'g', 'g', 'b', 'g', 'g', 'g', 'g', 'g', 'g', 'h', 'd', 'g',
                'h', 'g', 'h', 'd', 'd', 'd', 'd', 'd', 'd', 'h', 'd', 'b', 'g', 'b', 'd', 'h', 'd', 'b', 'g', 'b', 'd',
                'g', 'b', 'g', 'g', 'g', 'g', 'h', 'g', 'h', 'g', 'h', 'd', 'd', 'd', 'd', 'd', 'h', 'd', 'b', 'g', 'b',
                'd', 'd', 'd', 'g', 'g', 'b', 'b', 'g', 'g', 'g', 'g', 'h', 'h', 'g', 'h', 'd', 'd', 'd', 'd', 'h', 'd',
                'b', 'g', 'b', 'd', 'd'],
            7: ['g', 'g', 'b', 'g', 'g', 'g', 'g', 'g', 'g', 'g', 'h', 'g', 'h', 'h', 'd', 'd', 'd', 'd', 'd', 'd', 'd',
                'h', 'd', 'b', 'g', 'b', 'd', 'h', 'd', 'b', 'g', 'b', 'd', 'd', 'g', 'g', 'b', 'g', 'g', 'g', 'g', 'g',
                'g', 'g', 'h', 'd', 'g', 'h', 'g', 'h', 'd', 'd', 'd', 'd', 'd', 'd', 'd', 'h', 'd', 'b', 'g', 'b', 'd',
                'h', 'd', 'b', 'g', 'b', 'd', 'g', 'b', 'g', 'g', 'g', 'g', 'g', 'g', 'h', 'h', 'g', 'h', 'd', 'd', 'd',
                'd', 'd', 'd', 'h', 'd', 'b', 'g', 'b', 'd', 'd', 'd', 'g', 'g', 'b', 'b', 'g', 'g', 'g', 'g', 'h', 'g',
                'b', 'g', 'h', 'h', 'g', 'h', 'd', 'd', 'd', 'd', 'd', 'd', 'h', 'd', 'b', 'g', 'b', 'd', 'd', 'g', 'b',
                'b', 'g', 'g', 'g', 'g', 'g', 'h', 'h', 'g', 'h', 'd', 'd', 'd', 'd', 'd', 'h', 'd', 'b', 'g', 'b', 'd',
                'h', 'd', 'b', 'g', 'b', 'b', 'g', 'g', 'g', 'g', 'h', 'h', 'g', 'h', 'd', 'd', 'd', 'd', 'h', 'd', 'b',
                'g', 'b', 'd'],
            8: ['b', 'g', 'g', 'g', 'g', 'g', 'b', 'g', 'g', 'h', 'd', 'd', 'd', 'd', 'd', 'd', 'd', 'h', 'd', 'b', 'g',
                'b', 'd', 'h', 'd', 'b', 'g', 'b', 'd', 'd', 'g', 'g', 'b', 'g', 'g', 'g', 'g', 'h', 'g', 'h', 'g', 'h',
                'd', 'd', 'd', 'd', 'd', 'h', 'd', 'b', 'g', 'b', 'd', 'd', 'd', 'g', 'g', 'b', 'b', 'g', 'g', 'g', 'g',
                'h', 'h', 'g', 'h', 'd', 'd', 'd', 'd', 'b', 'd', 'd', 'h', 'g', 'b', 'g', 'h', 'g', 'g', 'g', 'g', 'g',
                'g', 'g', 'b', 'b', 'b', 'd', 'h', 'h', 'g', 'h', 'd', 'd', 'd', 'd', 'd', 'd', 'd', 'b', 'd', 'h', 'g',
                'g', 'g', 'g', 'g', 'g', 'g', 'b', 'b', 'd', 'b', 'd', 'd', 'd', 'd', 'd', 'g', 'g', 'g', 'g', 'h', 'h',
                'g', 'h', 'd', 'd', 'd', 'd', 'd', 'd'],
            9: ['d', 'd', 'd', 'd', 'h', 'd', 'b', 'g', 'b', 'd', 'h', 'd', 'b', 'g', 'b', 'd', 'd', 'g', 'g', 'h', 'h',
                'g', 'g', 'g', 'g', 'g', 'g', 'b', 'g', 'g', 'h', 'd', 'd', 'd', 'd', 'd', 'd', 'd', 'h', 'd', 'b', 'g',
                'b', 'd', 'h', 'd', 'b', 'g', 'b', 'd', 'g', 'h', 'h', 'g', 'g', 'g', 'g', 'g', 'g', 'g', 'g', 'b', 'b',
                'b', 'd', 'h', 'h', 'g', 'h', 'd', 'd', 'd', 'd', 'd', 'd', 'd', 'h', 'd', 'b', 'g', 'b', 'd', 'd', 'd',
                'g', 'g', 'g', 'h', 'g', 'g', 'g', 'g', 'g', 'g', 'b', 'b', 'b', 'd', 'h', 'h', 'g', 'h', 'd', 'd', 'd',
                'd', 'd', 'd', 'h', 'd', 'b', 'g', 'b', 'd', 'd', 'g', 'g', 'h', 'g', 'g', 'g', 'b', 'g', 'h', 'g', 'g',
                'b', 'b', 'd', 'h', 'g', 'h', 'd', 'd', 'd', 'd', 'd', 'd', 'b', 'd', 'd', 'h', 'g', 'b', 'g', 'h', 'g',
                'g', 'g', 'g', 'g', 'b', 'b', 'b', 'd', 'h', 'h', 'g', 'h', 'd', 'd', 'd', 'd', 'd', 'b', 'd', 'h', 'g',
                'g', 'g', 'g', 'g', 'b', 'b', 'b', 'd', 'h', 'h', 'g', 'h', 'd', 'd', 'd', 'd', 'd']
        }
        # si la solution est une chaine de caractere alors convertir on la transforme en liste
        if self.solution:
            self.solution = list(self.solution.lower())

        # si la solution vaut le booleen False on recupere une solution du dico de solution
        else:
            self.solution = self.dico_solutions[lvl]
        self.conversion = Image()
        self.indice = 0
        self.encours = False

    def react_to(self, event):
        """ Methode qui permet de gerer les evenements qui sont captes """
        Couche.react_to(self, event)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if not self.encours:
                    self.encours = True
                    pygame.event.post(pygame.event.Event(AUTOMATIQUE))
            elif event.key == pygame.K_RETURN:
                pygame.event.post(pygame.event.Event(JOUER))
            elif event.key == pygame.K_ESCAPE:
                pygame.event.post(pygame.event.Event(GO_MENU))

        elif event.type == AUTOMATIQUE:
            self.construct.mouvement_du_personnage(self.solution[self.indice])
            self.indice += 1
            if self.construct.victoire():
                pygame.event.post(pygame.event.Event(JOUER))
            else:
                pygame.event.post(pygame.event.Event(AUTOMATIQUE))
            time.sleep(0.3)

    def draw(self):
        """ Methode permettant de dessiner sur l'ecran de jeu """
        Couche.draw(self)
        self.conversion.affichage(self.construct.plateau, self.screen)
        tip1 = tip_font.render("Appuyez sur ESPACE pour lancer le solveur", True, (216, 77, 28))
        tip2 = tip_font.render("Appuyez sur ECHAP pour retourner au menu", True, (216, 77, 28))
        tip3 = tip_font.render("Appuyer sur ENTREE pour pour jouer", True,
                               (216, 77, 28))
        self.screen.blit(tip1, (self.width / 25, self.height / 2 + 150))
        self.screen.blit(tip2, (self.width / 25, self.height / 2 + 200))
        self.screen.blit(tip3, (self.width / 25, self.height / 2 + 250))


#################################### Ecran de selection des niveaux ####################################

class Niveaux(Couche):

    def __init__(self, screen: Union[Surface, SurfaceType]):
        """ Initialisation de la frame permettant la selection des niveaux """
        Couche.__init__(self, screen)
        self.bouton_token = 0
        self.niveau = 0
        ############################ Initialisation des rectangles du jeu######################
        self.rect_B0 = pygame.Rect(self.width / 10 + 70, self.height / 2 - 120, 120, 40)
        self.rect_B1 = pygame.Rect(self.width / 10 + 70, self.height / 2 - 60, 120, 40)
        self.rect_B2 = pygame.Rect(self.width / 10 + 70, self.height / 2, 120, 40)
        self.rect_B3 = pygame.Rect(self.width / 10 + 70, self.height / 2 + 60, 120, 40)
        self.rect_B4 = pygame.Rect(self.width / 10 + 70, self.height / 2 + 120, 120, 40)
        self.rect_B5 = pygame.Rect(self.width / 10 + 70, self.height / 2 + 180, 120, 40)
        self.rect_B6 = pygame.Rect(self.width / 10 + 320, self.height / 2 - 120, 120, 40)
        self.rect_B7 = pygame.Rect(self.width / 10 + 320, self.height / 2 - 60, 120, 40)
        self.rect_B8 = pygame.Rect(self.width / 10 + 320, self.height / 2, 120, 40)
        self.rect_B9 = pygame.Rect(self.width / 10 + 320, self.height / 2 + 60, 120, 40)
        self.rect_B10 = pygame.Rect(self.width / 10 + 320, self.height / 2 + 120, 120, 40)

        # liste des rectangles
        self.liste_rect = [self.rect_B0, self.rect_B1, self.rect_B2, self.rect_B3, self.rect_B4, self.rect_B5,
                           self.rect_B6, self.rect_B7, self.rect_B8, self.rect_B9,
                           self.rect_B10]

        ##############################Representation des rectangles sur l'écran ####################

    def react_to(self, event):
        """ Methode qui permet de gerer les evenements qui sont captes """
        Couche.react_to(self, event)
        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_UP:
                self.bouton_token = (self.bouton_token - 1) % len(self.liste_rect)

            elif event.key == pygame.K_DOWN:
                self.bouton_token = (self.bouton_token + 1) % len(self.liste_rect)

            elif event.key == pygame.K_SPACE or event.key == pygame.K_RETURN:
                pygame.event.post(pygame.event.Event(JOUER))

            elif event.key == pygame.K_ESCAPE:
                pygame.event.post(pygame.event.Event(GO_MENU))

        self.niveau = self.bouton_token

    def draw(self):
        """ Methode permettant de dessiner sur l'ecran de jeu """
        Couche.draw(self)
        self.screen.blit(text,
                         (400 - text.get_width() // 2, 30))  # representation sur la surface de l'ecran du nom du jeu

        choix = pygame.font.SysFont("gotham", 40).render("Choisissez un niveau", True, (255, 0, 0))
        self.screen.blit(choix, (190, 130))

        ########################## Modification des couleurs des rectangles liees à la position du bouton ou est l'utilisateur ######################

        # Mettre le rectangle en noir pour signifier la presence de l'utilisateur
        pygame.draw.rect(self.screen, (0, 0, 0), self.liste_rect[self.bouton_token])

        # Mettre le reste des rectangles en rouge
        for i in range(len(self.liste_rect)):
            if self.liste_rect[i] != self.liste_rect[self.bouton_token]:
                pygame.draw.rect(self.screen, (255, 0, 0), self.liste_rect[i])

        ########################### Texte sur les niveaux et representation sur la surface ####################################

        text_b0 = font.render('Niv 0', True, (255, 255, 255))
        self.screen.blit(text_b0, (self.width / 10 + 76, self.height / 2 - 126))

        text_b1 = font.render('Niv 1', True, (255, 255, 255))
        self.screen.blit(text_b1, (self.width / 10 + 76, self.height / 2 - 66))

        text_b2 = font.render('Niv 2', True, (255, 255, 255))
        self.screen.blit(text_b2, (self.width / 10 + 76, self.height / 2 - 6))

        text_b3 = font.render('Niv 3', True, (255, 255, 255))
        self.screen.blit(text_b3, (self.width / 10 + 76, self.height / 2 + 54))

        text_b4 = font.render('Niv 4', True, (255, 255, 255))
        self.screen.blit(text_b4, (self.width / 10 + 76, self.height / 2 + 114))

        text_b5 = font.render('Niv 5', True, (255, 255, 255))
        self.screen.blit(text_b5, (self.width / 10 + 76, self.height / 2 + 174))

        text_b6 = font.render('Niv 6', True, (255, 255, 255))
        self.screen.blit(text_b6, (self.width / 10 + 326, self.height / 2 - 126))

        text_b7 = font.render('Niv 7', True, (255, 255, 255))
        self.screen.blit(text_b7, (self.width / 10 + 326, self.height / 2 - 66))

        text_b8 = font.render('Niv 8', True, (255, 255, 255))
        self.screen.blit(text_b8, (self.width / 10 + 326, self.height / 2 - 6))

        text_b9 = font.render('Niv 9', True, (255, 255, 255))
        self.screen.blit(text_b9, (self.width / 10 + 326, self.height / 2 + 54))

        text_b10 = font.render('Niv 10', True, (255, 255, 255))
        self.screen.blit(text_b10, (self.width / 10 + 326, self.height / 2 + 114))


#################################### Ecran de fin ####################################

class Fin(Couche):

    def __init__(self, screen: Union[Surface, SurfaceType], nb_de_coups):
        """ Initialisation de la frame gerant l'ecran de fin """
        Couche.__init__(self, screen)
        self.bouton_token = 0
        self.nombre_coups_total = nb_de_coups
        self.rect_B1 = pygame.Rect(self.width / 2 - 300, self.height / 2 + 120, 200, 60)
        self.rect_B2 = pygame.Rect(self.width / 2 - 100, self.height / 2 + 120, 200, 60)
        self.rect_B3 = pygame.Rect(self.width / 2 + 100, self.height / 2 + 120, 200, 60)
        self.liste_rect = [self.rect_B1, self.rect_B2, self.rect_B3]

    def react_to(self, event):
        """ Methode qui permet de gerer les evenements qui sont captes """
        Couche.react_to(self, event)
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                self.bouton_token = (self.bouton_token - 1) % 3
            elif event.key == pygame.K_RIGHT:
                self.bouton_token = (self.bouton_token + 1) % 3
            elif event.key == pygame.K_SPACE or event.key == pygame.K_RETURN:
                if self.liste_rect[self.bouton_token] == self.rect_B1:
                    pygame.event.post(pygame.event.Event(JOUER))
                elif self.liste_rect[self.bouton_token] == self.rect_B2:
                    pygame.event.post(pygame.event.Event(GO_MENU))
                elif self.liste_rect[self.bouton_token] == self.rect_B3:
                    sys.exit()

    def draw(self):
        """ Methode permettant de dessiner sur l'ecran de jeu """
        Couche.draw(self)
        text_v = font.render('Bravo, vous avez gagné !', True, (138, 101, 56))
        self.screen.blit(text_v, (self.width / 2 - text.get_width() / 2 - 20, 30))

        text_stats = font.render("Vous avez fait : {} coups!".format(self.nombre_coups_total), True, (142, 142, 142))
        self.screen.blit(text_stats, (self.width / 2 - text.get_width() / 2 - 30, 105))

        couleur_principale = [(0, 204, 0), (255, 128, 0), (128, 0, 255)]
        couleur_secondaire = [(38, 77, 0), (77, 38, 0), (57, 0, 77)]

        pygame.draw.rect(self.screen, couleur_secondaire[self.bouton_token], self.liste_rect[self.bouton_token])

        for i in range(len(self.liste_rect)):
            if i != self.bouton_token:
                pygame.draw.rect(self.screen, couleur_principale[i], self.liste_rect[i])

        text_b1 = font.render('Rejouer', True, (255, 255, 255))
        self.screen.blit(text_b1, (self.width / 2 - 265, self.height / 2 + 120))

        text_b2 = font.render('Menu', True, (255, 255, 255))
        self.screen.blit(text_b2, (self.width / 2 - 47, self.height / 2 + 120))

        text_b3 = font.render('Quitter', True, (255, 255, 255))
        self.screen.blit(text_b3, (self.width / 2 + 135, self.height / 2 + 120))