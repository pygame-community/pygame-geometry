"""
This is an example script implementing
the method normal_polygon() from the class Polygon
for the Pygame community.

Author: @newpaxonian
"""

import random
import sys

import pygame as pg
import geometry

DARK_GREY = (10, 10, 10)
SIDES = [3, 4, 5, 6, 7, 8, 9, 10, 11, 12]


class Game:
    """
    Class Game: contains the main game loop and the methods
    """

    def __init__(self):
        pg.init()
        self.display = pg.display
        self.screen = self.display.set_mode((640, 480))
        self.clock = pg.time.Clock()
        self.radius = 64
        self.toggle_mouse_button = False
        self.polygons = []

    def events(self):
        """
        Method events: handles the events
        """
        for event in pg.event.get():
            if event.type == pg.QUIT or (
                    event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE
            ):
                print("\nQuitting program...")
                pg.quit()
                sys.exit()
            if pg.MOUSEBUTTONDOWN and any(pg.mouse.get_pressed()):
                self.toggle_mouse_button = not self.toggle_mouse_button

    def draw(self, num_sides=3, color=(255, 255, 255)):
        """
        Method draw: draws a regular polygon
        """
        box_side = 2 * self.radius
        box = pg.Surface((box_side, box_side))
        box.fill(DARK_GREY)
        box_x, box_y = pg.mouse.get_pos()
        polygon_radius = box_side // 2
        polygon_center = (box_side // 2, box_side // 2)
        polygon = geometry.Polygon.normal_polygon(
            num_sides, polygon_center, polygon_radius, 30
        )

        self.screen.fill(DARK_GREY)
        pg.draw.polygon(box, color, polygon.vertices)
        self.screen.blit(box, (box_x - box_side // 2, box_y - box_side // 2))

    def run(self):
        """
        Main game loop
        """
        while True:
            self.clock.tick(60)
            self.display.set_caption(
                f"Regular Polygons - FPS {self.clock.get_fps():.1f}"
            )

            self.events()

            if self.toggle_mouse_button:
                num_sides = random.choice(SIDES)
                color = (
                    random.randint(0, 255),
                    random.randint(0, 255),
                    random.randint(0, 255),
                )
                self.draw(num_sides=num_sides, color=color)

            self.display.update()


def main():
    """
    Main function
    """
    game = Game()
    game.run()


if __name__ == "__main__":
    main()
