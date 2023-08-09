## Contributing Guidelines

1. See [Contributing Guidelines](https://github.com/pygame-community/pygame_geometry/blob/main/CONTRIBUTING.md) for general contributing guidelines.
2. Use this boilerplate to get started

```python
"""

This serves as a boilerplate for pygame_geometry.
You must use this boilerplate in order to create
any official pygame_geometry examples.

@authors: andrewhong@myyahoo.com

"""

import pygame
import pygame_geometry

### == Configuration

DISPLAY_NAME = "pygame_geometry examples boilerplate"
PREFERRED_FPS = 60
WIDTH = 800
HEIGHT = 800

### == Game

pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption(DISPLAY_NAME)

running = True
while running:
  for event in pygame.event.get():
      if event.type == pygame.QUIT:
          running = False

    screen.fill((0, 0, 0))

    pygame.display.flip()
    delta_time = clock.tick(PREFERRED_FPS) / 1000 / PREFERRED_FPS

pygame.quit()

```
