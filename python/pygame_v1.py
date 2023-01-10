import pygame
import sys

width = 800
height = 500
radius = 5
target_fps = 60
screen_bcg = "black"

# Initialization
pygame.init()
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Circles')
fps = pygame.time.Clock()
paused = False

# Ball setup
ball_pos1 = [50, 50]
ball_pos2 = [50, 240]
ball_pos3 = [50, 430]


def update():
    ball_pos1[0] += 5
    ball_pos2[0] += 3
    ball_pos3[0] += 1


def render():
    screen.fill(screen_bcg)

    pygame.draw.circle(screen, "red", ball_pos1, radius, 0)
    pygame.draw.circle(screen, "white", ball_pos2, radius, 0)
    pygame.draw.circle(screen, "green", ball_pos3, radius, 0)

    pygame.display.update()
    fps.tick(target_fps)


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_SPACE:
                paused = not paused
    if not paused:
        update()
        render()
