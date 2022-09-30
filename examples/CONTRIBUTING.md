## Contributing Guidelines

1. See [Contributing Guidelines](https://github.com/novialriptide/pygame_geometry/blob/main/CONTRIBUTING.md) for general contributing guidelines.
2. Use this boilerplate to get started

```python
"""
This serves as a boilerplate for pygame_geometry.
@authors: andrewhong@myyahoo.com
"""

import pygame
import pygame_geometry

### == Configuration

DISPLAY_NAME = "pygame_geometry examples boilerplate"
WIDTH = 800
HEIGHT = 800

### == Game

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption(DISPLAY_NAME)

running = True
while running:
  for event in pygame.event.get():
      if event.type == pygame.QUIT:
          running = False

    screen.fill((0, 0, 0))

    pygame.display.flip()

pygame.quit()

```
