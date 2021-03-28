import pygame
import numpy as np
from numba import jit

from moverand import *

from settings import *

@jit
def _MapToColor(value, maxValue, colorA, colorB):
    return [
        int(colorA[0] + (value/maxValue)*(colorB[0] - colorA[0])),
        int(colorA[1] + (value/maxValue)*(colorB[1] - colorA[1])),
        int(colorA[2] + (value/maxValue)*(colorB[2] - colorA[2]))
    ]

@jit
def _ColorToInteger(color):
    return ( color[0] << 0 ) | ( color[1] << 8 ) | ( color[2] << 16 )

@jit
def _MapToVisual(trails, xSlimes, ySlimes):
    colored = np.empty_like(trails)

    if DRAW_TRAIL:
        for i in range(WIDTH*HEIGHT):
            colored[i] = _ColorToInteger( _MapToColor( trails[i], 100, BACKGROUND, TRAIL_COLOR ) )

    for i in range(SLIMES):
        colored[ xSlimes[i] + ySlimes[i]*WIDTH ] = _ColorToInteger( SLIME_COLOR )


    return colored

# Initialize graghics
def InitializeGraghics():
    pygame.init()
    return pygame.display.set_mode([CANVAS_WIDTH, CANVAS_WIDTH]), pygame.Surface([WIDTH, HEIGHT])


# Main loop
def MainGraghicsLoop():
    # Main loop
    running = True
    screen, smallSurface = InitializeGraghics()

    xSlime=np.array([START_X for _ in range(SLIMES)])
    ySlime=np.array([START_Y for _ in range(SLIMES)])
    direction=np.array([random.uniform(0, math.pi*2) for _ in range(SLIMES)])
    trail=np.array([0 for _ in range(WIDTH*HEIGHT)])

    while running:

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False


        # Todo: Integrate with Nicks Code
        xSlime, ySlime, direction, trail = Update(xSlime, ySlime, direction, trail)

        visual = _MapToVisual(trail, xSlime, ySlime)

        # Draw the pixel array
        pygame.pixelcopy.array_to_surface(
            smallSurface,
            visual.reshape(WIDTH, HEIGHT)
        )

        frame = pygame.transform.scale(smallSurface, (CANVAS_WIDTH, CANVAS_WIDTH))


        screen.blit(frame, frame.get_rect())

        # Update the screen
        pygame.display.flip()

def TestGraghics():
    MainGraghicsLoop()


TestGraghics()
