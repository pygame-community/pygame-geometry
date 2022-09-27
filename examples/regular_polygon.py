"""
This is an example script implementing
the method normal_polygon() from the class Polygon
for the Pygame community.

Author: @newpaxonian
"""

import math
import random
import sys

import geometry
import pygame as pg

GRAY_BACKGROUND = (47, 52, 63)


class Game:
    """
    Class Game: contains the main game loop and the methods
    """

    def __init__(self):
        pg.init()
        self.display = pg.display
        self.screen = self.display.set_mode((640, 480))
        self.clock = pg.time.Clock()
        self.radius = 16
        self.sides = 3
        self.mouse_left = False
        self.mouse_right = False
        self.mouse_wheel = False
        self.font = pg.font.SysFont("Consolas", 14, True)
        self.text_timer = 20
        self.text_alpha = 255
        self.polygon_names = {3: "triangle", 4: "square", 5: "pentagon",
                              6: "hexagon", 7: "heptagon", 8: "octagon",
                              9: "enneagon", 10: "decagon"}
        self.polygon_text_pos = (600, 466)

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
            if event.type == pg.MOUSEBUTTONDOWN:
                if pg.mouse.get_pressed() == (1, 0, 0):
                    self.mouse_left = not self.mouse_left
                elif pg.mouse.get_pressed() == (0, 0, 1):
                    self.mouse_right = True
            if event.type == pg.MOUSEBUTTONUP:
                if pg.mouse.get_pressed() == (0, 0, 0):
                    self.mouse_left = False
                    self.mouse_right = False
            if event.type == pg.MOUSEWHEEL:
                self.mouse_wheel = True
                if event.y > 0:
                    self.sides = self.sides + 1 if self.sides < 10 else 10
                elif event.y < 0:
                    self.sides = self.sides - 1 if self.sides > 3 else 3

    def draw_polygon(self, num_sides=3, center=(0.0, 0.0),
                     radius=1.0, angle=0.0, color=(255, 255, 255)):
        """
        Method draw_polygon: draws a regular polygon
        """
        box_side = 2 * radius
        box_x, box_y = center[0] - box_side // 2, center[1] - box_side // 2
        box = pg.surface.Surface((box_side, box_side)).convert_alpha()
        box.fill([0, 0, 0, 0])
        polygon = geometry.regular_polygon(
            num_sides, (box_side // 2, box_side // 2), radius, angle
        )

        pg.draw.polygon(box, color, polygon.vertices)
        self.screen.blit(box, (box_x, box_y))

    def draw_text(self, text, color, pos):
        """
        Method draw_text: draws text
        """
        text_surface = self.font.render(text, True, color)
        text_rect = text_surface.get_rect(center=pos)
        text_rect.center = pos
        text_bg = pg.surface.Surface((80, text_surface.get_height() + 5))
        text_bg_size = text_bg.get_size()
        text_bg_rect = text_bg.get_rect(center=pos)
        # pos - (text_bg_size // 2)
        text_bg_rect.center = tuple(
            (p - tbg // 2) for p, tbg in zip(pos, text_bg_size)
        )
        text_bg.fill(GRAY_BACKGROUND)
        self.screen.blit(text_bg, text_bg_rect.center)
        self.screen.blit(text_surface, text_rect)

    def draw(self):
        """
        Method draw: draws scene
        """
        # Mouse events
        if self.mouse_left:
            angle = math.tau * random.uniform(0.0, 1.0)
            x = pg.mouse.get_pos()[0] \
                + round(math.cos(angle) * self.radius * 0.5)
            y = pg.mouse.get_pos()[1] \
                + round(math.sin(angle) * self.radius * 0.5)
            color = (
                random.randint(0, 255),
                random.randint(0, 255),
                random.randint(0, 255),
            )
            self.draw_polygon(
                num_sides=self.sides, center=(x, y),
                radius=self.radius, angle=33.33333, color=color
            )
        elif self.mouse_right:
            self.screen.fill(GRAY_BACKGROUND)
        elif self.mouse_wheel:
            self.draw_text(
                f"{self.polygon_names[self.sides]}",
                "white", self.polygon_text_pos
            )
            self.mouse_wheel = False

        # Screen Title
        title = self.font.render(
            "Mouse: left = draw | right = reset | wheel = change polygon",
            True, "white"
        )
        title_background = pg.surface.Surface((640, title.get_height() + 5))
        title_background.set_alpha(180)
        title_pos = title.get_rect(center=(640 / 2, title.get_height() * 0.75))

        self.screen.blit(title_background, (0, 0))
        self.screen.blit(title, title_pos)

        self.draw_text(
            f"{self.polygon_names[self.sides]}", "white", self.polygon_text_pos
        )
        pg.time.wait(50)

    def run(self):
        """
        Main game loop
        """
        self.screen.fill(GRAY_BACKGROUND)
        while True:
            self.clock.tick(60)
            self.display.set_caption("Regular Polygons")
            self.events()
            self.draw()
            self.display.update()


def main():
    """
    Main function
    """
    game = Game()
    game.run()


if __name__ == "__main__":
    main()
