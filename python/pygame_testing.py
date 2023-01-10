import pygame
pygame.init()


active = True
target_fps = 60
width = 800
height = 500
radius = 20
# Set the initial speed of the ball
x_speed = 2
y_speed = 3


screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Moving Ball")
clock = pygame.time.Clock()


# -------- Main Program Loop -----------
while active:
    # --- Main event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            active = False

    # --- Game logic should go here

    # Move the ball
    x += x_speed
    y += y_speed

    # Check for collision with the edges of the screen
    if x > size[0] - radius or x < radius:
        x_speed = -x_speed
    if y > size[1] - radius or y < radius:
        y_speed = -y_speed

    # --- Drawing code should go here
    # Clear the screen to white
    screen.fill((255, 255, 255))

    # Draw the ball
    pygame.draw.circle(screen, "red", (x, y), radius, 0)

    # --- Go ahead and update the screen with what we've drawn.
    pygame.display.flip()

    # --- Limit to 60 frames per second
    clock.tick(target_fps)

# Close the window and quit.
pygame.quit()
