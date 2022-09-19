import random
import sys

import geometry
import pygame as pg

FPS = 60
RES = WIDTH, HEIGHT = 640, 480
DARK_GREY = (10, 10, 10)
SIDES = [3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
COLORS = {
    3: (255, 0, 0),
    4: (0, 255, 0),
    5: (0, 0, 255),
    6: (255, 255, 0),
    7: (0, 255, 255),
    8: (255, 0, 255),
    9: (255, 255, 255),
    10: (255, 127, 0),
    11: (127, 0, 255),
    12: (0, 255, 127),
}


class Game:
    def __init__(self):
        pg.init()
        # pg.mouse.set_visible(False)
        self.display = pg.display
        self.screen = self.display.set_mode(RES)
        self.clock = pg.time.Clock()
        self.colors = COLORS
        self.radius = 64
        self.toggle_mouse_button = False
        self.polygons = []

    def events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                print("\nQuitting program...")
                pg.quit()
                sys.exit()
            if pg.mouse.get_pressed()[0]:
                if self.toggle_mouse_button:
                    self.toggle_mouse_button = False
                else:
                    self.toggle_mouse_button = True

    def draw(self, num_sides=3, color=(255, 255, 255)):
        box_side = 2 * self.radius
        box = pg.Surface((box_side, box_side))
        box.fill(DARK_GREY)

        box_x, box_y = pg.mouse.get_pos()

        polygon_radius = box_side // 2
        polygon_center = (box_side // 2, box_side // 2)

        polygon = geometry.Polygon.normal_polygon(num_sides, polygon_center, polygon_radius, 30)

        self.screen.fill(DARK_GREY)
        pg.draw.polygon(box, color, polygon.vertices)
        self.screen.blit(box, (box_x - box_side // 2, box_y - box_side // 2))

    def update(self):
        self.display.update()

    def run(self):
        while True:
            self.clock.tick(FPS)
            self.display.set_caption(f"Regular Polygons - FPS {self.clock.get_fps():.1f}")

            self.events()

            if self.toggle_mouse_button:
                num_sides = SIDES[random.randint(0, len(self.colors) - 1)]
                color = self.colors[num_sides]
                self.draw(num_sides=num_sides, color=color)

            self.update()


def main():
    game = Game()
    game.run()


if __name__ == "__main__":
    main()
