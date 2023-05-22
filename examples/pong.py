import geometry
from random import randint
import pygame

pygame.font.init()

W, H = 800, 600

screen = pygame.display.set_mode((W, H))
clock = pygame.time.Clock()

running = True

paddle_a = pygame.Rect(20, H / 2 - 100 / 2, 20, 100)
paddle_b = pygame.Rect(W - 20 - 20, H / 2 - 100 / 2, 20, 100)

ball = geometry.Circle(W / 2, H / 2, 7)
vel = pygame.Vector2(5, -5)

a_points = 0
b_points = 0

font = pygame.font.Font(None, 50)

while running:
    screen.fill((0, 0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()

    if keys[pygame.K_w]:
        paddle_a.y -= 5
    elif keys[pygame.K_s]:
        paddle_a.y += 5

    if keys[pygame.K_UP]:
        paddle_b.y -= 5
    elif keys[pygame.K_DOWN]:
        paddle_b.y += 5

    if paddle_a.y <= 0:
        paddle_a.y = 0
    elif paddle_a.y + paddle_a.h >= H:
        paddle_a.y = H - paddle_a.h

    if paddle_b.y <= 0:
        paddle_b.y = 0
    elif paddle_b.y + paddle_b.h >= H:
        paddle_b.y = H - paddle_b.h

    ball.center += vel

    if ball.y - ball.r <= 0:
        vel.y *= -1
    if ball.y + ball.r >= H:
        vel.y *= -1

    if ball.x - ball.r <= 0:
        a_points += 1
        ball.center = W / 2, H / 2
        vel.x *= -1
    if ball.x + ball.r >= W:
        b_points += 1
        ball.center = W / 2, H / 2
        vel.x *= -1

    if ball.colliderect(paddle_a):
        vel.x *= -1
        ball.x += vel.x * 0.85

    if ball.colliderect(paddle_b):
        vel.x *= -1
        ball.x += vel.x * 0.85

    pygame.draw.rect(screen, "white", paddle_a)
    pygame.draw.rect(screen, "white", paddle_b)

    pygame.draw.circle(screen, "white", ball.center, ball.r)

    label = font.render(f"{a_points} | {b_points}", 1, "white")

    screen.blit(label, (W / 2 - label.get_width() / 2, 10))

    pygame.display.update()
    clock.tick(60)

pygame.quit()
