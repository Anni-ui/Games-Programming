import pygame
import random
pygame.init()
screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()
x, y = 400, 300
color = (255, 107, 53)
red = [60, 110, 155]
green = [155, 60, 107]
blue = [107, 155, 60]

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:  x -= 5
    if keys[pygame.K_RIGHT]: x += 5
    if keys[pygame.K_UP]:    y -= 5
    if keys[pygame.K_DOWN]:  y += 5
    if keys[pygame.K_SPACE]: color = (random.choice(red), random.choice(green), random.choice(blue))

    screen.fill((11, 13, 16))
    pygame.draw.rect(screen, (color), (x, y, 40, 40))
    pygame.display.flip()
    clock.tick(60)

pygame.quit()