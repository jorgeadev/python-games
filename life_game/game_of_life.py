import pygame
import numpy as np
import time

pygame.init()

width, height = 1000, 1000
screen = pygame.display.set_mode((height, width))

bg = 25, 25, 25
screen.fill(bg)

nxC, nyC = 50, 50
dimCW = width / nxC
dimCH = height / nyC

# Estado de la celdas. Vivas = 1, Muertas = 0;
game_satate = np.zeros((nxC, nyC))

# Autómata palo.
#game_satate[5, 3] = 1
#game_satate[5, 4] = 1
#game_satate[5, 5] = 1

# autómata movil.
game_satate[21, 21] = 1
game_satate[21, 22] = 1
game_satate[21, 23] = 1
game_satate[22, 23] = 1
game_satate[20, 23] = 1

# control de la ejecució del juego.
pause_except = False

# Bucle de ejecución
while True:
    new_game_state = np.copy(game_satate)
    screen.fill(bg)
    time.sleep(0.2)

    # Registrar eventos de teclado y ratón.
    ev = pygame.event.get()
    for event in ev:
        if event.type == pygame.KEYDOWN:
            pause_except = not pause_except

        mouse_click = pygame.mouse.get_pressed()
        if sum(mouse_click) > 0:
            posX, posY = pygame.mouse.get_pos()
            celX, celY = int(np.floor(posX / dimCW)), int(np.floor(posY / dimCH))
            new_game_state[celX, celY] = not mouse_click[2]

    for  y in range(0, nxC):
        for x in range(0, nyC):

            if not pause_except:
                # Calculamos el número de ecinos cercanos.
                n_neigh = game_satate[(x - 1) % nxC, (y - 1) % nyC] + \
                          game_satate[(x)     % nxC, (y - 1) % nyC] + \
                          game_satate[(x + 1) % nxC, (y - 1) % nyC] + \
                          game_satate[(x - 1) % nxC, (y) %     nyC] + \
                          game_satate[(x + 1) % nxC, (y) %     nyC] + \
                          game_satate[(x - 1) % nxC, (y + 1) % nyC] + \
                          game_satate[(x)     % nxC, (y + 1) % nyC] + \
                          game_satate[(x + 1) % nxC, (y + 1) % nyC]

                # Rule 1: Una célula muerta con exactamente 3 vecinas vivas, "revive".
                if game_satate[x, y] == 0 and n_neigh == 3:
                    new_game_state[x, y ] = 1

                # Rule 2: Una célula viva con menos de 2 o más de 3 vecinas vivas, "muere".
                elif game_satate[x, y] == 1 and (n_neigh < 2 or n_neigh > 3):
                    new_game_state[x, y] = 0

            # Creamos los polígoos de cada una de las celdas a dibujar.
            poly = [((x)     * dimCW, y        * dimCH),
                    ((x + 1) * dimCW, y        * dimCH),
                    ((x + 1) * dimCW, (y + 1)  * dimCH),
                    ((x)     * dimCW, (y + 1) * dimCH)]

            # Dibujamos la celda para cada par x, y.
            if new_game_state[x, y] == 0:
                pygame.draw.polygon(screen, (128, 128, 128), poly, 1)
            else:
                pygame.draw.polygon(screen, (255, 255, 255), poly, 0)

    # Actualizamos el estado del juego.
    game_satate = np.copy(new_game_state)

    # Actualizamos la pantalla.
    pygame.display.flip()