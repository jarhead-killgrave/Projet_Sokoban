from typing import Union
import pygame
from pygame import Surface
from pygame.surface import SurfaceType

import level

import grille

pygame.init()


class Image:
    def __init__(self, theme="defaut"):
        """constructeur de la classe gerant les images du jeu"""
        super().__init__()
        self.representation = {
            "@": pygame.image.load("graphiques/themes/{}/images/player.png".format(theme)),
            "+": pygame.image.load("graphiques/themes/{}/images/player.png".format(theme)),
            " ": pygame.image.load("graphiques/themes/{}/images/space.png".format(theme)),
            ".": pygame.image.load("graphiques/themes/{}/images/target.png".format(theme)),
            "$": pygame.image.load("graphiques/themes/{}/images/box.png".format(theme)),
            "*": pygame.image.load("graphiques/themes/{}/images/box_on_target.png".format(theme)),
            "#": pygame.image.load("graphiques/themes/{}/images/wall.png".format(theme)),
        }
        self.taille = self.representation["@"].get_width()

    def dessiner_grille(self, plateau: list, ecran: Union[Surface, SurfaceType]):
        """
            methode permetant de dessiner un tableau 2D sur un ecran par parcours de ligne et colonne

            :param plateau: une liste de liste à dessiner
            :param ecran: surface surlaquelle il faut afficher les carracteres graphiques
        """
        for i in range(len(plateau)):
            for j in range(len(plateau[i])):
                val = plateau[i][j]
                if val in self.representation:
                    ecran.blit(self.representation[val], (j * self.taille, i * self.taille))

    def dessiner_level(self, niveau: Union[level.Level, grille.Grille], ecran: Union[Surface, SurfaceType]) -> None:
        """
            methode permetant de dessiner une grille(Grille) ou un niveau(Level) par numero de case

            :param niveau: un objet Level ou Grille à dessiner
            :param ecran: surface surlaquelle il faut afficher les carracteres graphiques
        """
        for numero_case in range(niveau.taille):
            val = niveau.valeur_case(numero_case)
            if val in self.representation:
                ecran.blit(self.representation[val], niveau.coordonnees_graphique(numero_case, self.taille))

    def affichage(self, plateau: Union[level.Level, grille.Grille, list], ecran: Union[Surface, SurfaceType]):
        """
            methode gerant la methode pour dessiner un niveau

            Choisi un methode(dessiner_grille ou dessiner_level) pour dessiner un plateau à partir de son type initiale

            :param plateau: un tableau 2D, un grille(Grille) ou un niveau(Level)
            :param ecran: surface surlaquelle il faut afficher les carracteres graphiques
        """
        if type(plateau) == list:
            self.dessiner_grille(plateau, ecran)
        elif type(plateau) == level.Level or grille.Grille:
            self.dessiner_level(plateau, ecran)


class Audio:

    def __init__(self):
        """Constructeur de la classe gérant les sons du jeu"""
        self.sons = {
            "lancer_jeu": pygame.mixer.Sound("Audio/debut_partie.wav"),
            "appuie_touche": pygame.mixer.Sound("Audio/keypress.wav"),
        }
        self.son_on = True
        for son in self.sons:
            self.sons[son].set_volume(0.15)

    def play(self, event):

        if self.son_on:
            if event.type == pygame.KEYDOWN:
                pygame.mixer.Sound.play(self.sons["appuie_touche"])
            elif event.type == pygame.USEREVENT + 1: # Evenement utilisateur correspondant a JOUER
                pygame.mixer.Sound.play(self.sons["lancer_jeu"])

        if event.type == pygame.KEYUP and event.key == pygame.K_m:
            if self.son_on:
                self.son_on = False
            else:
                self.son_on = True
