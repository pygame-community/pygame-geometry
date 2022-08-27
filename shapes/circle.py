from __future__ import annotations

from typing import Sequence, Tuple

import pygame

from shapes.shape import Shape

__all__ = ("Circle",)


def radius_values(r: float) -> Tuple[float, float, float]:
    """takes the r value as input and returns a tuple containing (in order):
    (r: float, d: float, r_sqr: float)
    """
    return r, 2 * r, r * r
    # dunder methods


class Circle(Shape):
    __slots__ = ("x", "y", "r", "d", "r_sqr")

    def __init__(self, x: float, y: float, r: float) -> None:
        self.x, self.y = x, y
        # d and r_sqr are
        # convenient attributes for saving calculations
        self.r, self.d, self.r_sqr = radius_values(r)

    def copy(self) -> Circle:
        """Returns a new Circle object that's a copy of the original"""
        return Circle(self.x, self.y, self.r)

    # Movement, scale and position functions
    def update(self, x: float, y: float, r: float) -> None:
        """Updates the x and y position and r in place"""
        self.x = x
        self.y = y
        self.r = r
        self.r_sqr = r * r

    def move(self, x: float, y: float) -> Circle:
        """Returns a new Circle that's moved by the x and y offsets and
        has the same r as the original
        """
        return Circle(self.x + x, self.y + y, self.r)

    def move_ip(self, x: float, y: float) -> None:
        """Moves the circle's position by the x and y offsets in place"""
        self.x += x
        self.y += y

    def move_to(self, x: float, y: float) -> Circle:
        """Returns a new Circle with x and y as position and
        same r as self
        """
        return Circle(x, y, self.r)

    def move_to_ip(self, x: float, y: float) -> None:
        """Set the circle's x and y positions to the new position in place"""
        self.x = x
        self.y = y

    def scale_by(self, amount: float) -> Circle:
        """Returns a new Circle with same position as self and updated r"""
        r = self.r
        if r * amount <= 0:
            r = 1

        return Circle(self.x, self.y, r * amount)

    def scale_by_ip(self, amount: float) -> None:
        """Scales the Circle to the new r in place"""

        self.r *= amount

        if self.r <= 1:
            self.r = 1

        self.r, self.d, self.r_sqr = radius_values(self.r)

    # Collisions and conversion functions
    def as_rect(self) -> pygame.Rect:
        """Returns the rectangle that fully encloses the circle"""
        pos = (self.x - self.r, self.y - self.r)
        return pygame.Rect(pos, (self.d, self.d))

    def collideswith(self, other) -> bool:
        """General collision function, accepts any implemented Shape.
        Checks whether the circle collides with a Shape,
        returns True if they do, False otherwise
        """
        if type(other) is Circle:
            rad = self.r + other.r

            dx = self.x - other.x
            dy = self.y - other.y

            return dx * dx + dy * dy <= rad * rad
        elif type(other) is pygame.Rect:
            test_x = self.x
            test_y = self.y

            if self.x < other.x:
                test_x = other.x
            elif self.x > other.right:
                test_x = other.right

            if self.y < other.y:
                test_y = other.y
            elif self.y > other.bottom:
                test_y = other.bottom

            dx = self.x - test_x
            dy = self.y - test_y

            return dx * dx + dy * dy <= self.r_sqr
        else:
            if type(other) is list or type(other) is tuple and len(other) == 2:
                self.collidepoint(*other)
            else:
                raise NotImplementedError(
                    "The shape type does not exist yet"
                    " or doesn't have a matching collision algorythm"
                )

    def collidepoint(self, x: float, y: float) -> bool:
        """Checks whether the circle collides with a point,
        returns True if they do, False otherwise
        """

        dx = self.x - x
        dy = self.y - y
        return dx * dx + dy * dy <= self.r_sqr

    def collidecircle(self, other: Circle) -> bool:
        """Checks whether the circle collides with the other circle,
        returns True if they do, False otherwise
        """

        radii_squared = self.r_sqr + other.r_sqr + 2 * self.r * other.r
        dx = self.x - other.x
        dy = self.y - other.y

        return dx * dx + dy * dy <= radii_squared

    def colliderect(self, other: pygame.Rect) -> bool:
        """Checks whether the circle collides with the rect,
        returns True if they do, False otherwise
        """
        test_x = self.x
        test_y = self.y

        if self.x < other.x:
            test_x = other.x
        elif self.x > other.right:
            test_x = other.right

        if self.y < other.y:
            test_y = other.y
        elif self.y > other.bottom:
            test_y = other.bottom

        dx = self.x - test_x
        dy = self.y - test_y

        return dx * dx + dy * dy <= self.r_sqr

    # def collideline(self, other: Line) -> bool:
    def contains(self, other: Circle) -> bool:
        """Checks whether the circle contains the other circle,
        returns True if they do, False otherwise
        """

        dx = self.x - other.x
        dy = self.y - other.y
        dr = self.r - other.r
        return dx * dx + dy * dy <= dr * dr

    def __call__(self, *args, **kwargs):
        return (self.x, self.y), self.r

    def __repr__(self) -> str:
        return f"Circle({(self.x, self.y)}, {self.r})"
