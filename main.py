from frame import *
import pygame

FPS = 30

if __name__ == "__main__":
    pygame.init()
    niveau = 0
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("A Sokoban Adventure")
    my_frame = Menu(screen)
    nb_de_coups = 0
    score = 0
    horloge = pygame.time.Clock()
    while True:
        time = horloge.tick(FPS)
        for event in pygame.event.get():

            my_frame.react_to(event)

            if event.type == JOUER:
                my_frame = Jouer(screen, niveau)
                my_frame.nombre_coups_total = nb_de_coups
                my_frame.score =score


            elif event.type == NIVEAUX:
                my_frame = Niveaux(screen)

            elif event.type == GO_MENU:
                my_frame = Menu(screen)
                nb_de_coups = 0
                score = 0

            elif event.type == ECRAN_FIN:
                my_frame = Fin(screen, nb_de_coups)
                nb_de_coups = 0
                score = 0
            elif event.type == RUN_SOLUTION:
                my_frame = Resolution(screen, niveau)

        if type(my_frame) == Niveaux or type(my_frame) == Jouer:
            niveau = my_frame.niveau
        if type(my_frame) == Jouer:
            nb_de_coups = my_frame.nombre_coups_total
            score = my_frame.score

        my_frame.draw()
        pygame.display.flip()
