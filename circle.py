from __future__ import annotations

from typing import Sequence, Tuple

import pygame

from shape import Shape

__all__ = "Circle",


def radius_values(radius: float) -> Tuple[float, float, float]:
    """takes the radius value as input and returns a tuple containing (in order):
       (radius: float, diameter: float, radius_squared: float)
    """
    return radius, 2 * radius, radius * radius
    # dunder methods


class Circle(Shape):
    __slots__ = ("x", "y", "radius", "diameter", "radius_squared")
    
    def __init__(self, center: Sequence[float, float], radius: float) -> None:
        if radius <= 0:
            radius = 1
        self.x, self.y = center
        # diameter and radius_squared are
        # convenient attributes for saving calculations
        self.radius, self.diameter, self.radius_squared = radius_values(radius)
    
    def copy(self) -> Circle:
        return Circle((self.x, self.y), self.radius)
    
    # Movement, scale and position functions
    def update(self, center: Sequence[float, float], radius: float) -> None:
        if radius <= 0:
            radius = 1
        self.x, self.y = center
        self.radius, self.diameter, self.radius_squared = radius_values(radius)
    
    def move(self, x: float, y: float) -> Circle:
        return Circle((self.x + x, self.y + y), self.radius)
    
    def move_ip(self, x: float, y: float) -> None:
        self.x += x
        self.y += y

    def move_to(self, x: float, y: float) -> Circle:
        return Circle((x, y), self.radius)

    def move_to_ip(self, x: float, y: float) -> None:
        self.x = x
        self.y = y
    
    def scale(self, radius: float) -> Circle:
        """Return a new Circle with position as self and updated radius"""
        if radius <= 0:
            radius = 1
        return Circle((self.x, self.y), radius)
    
    def scale_ip(self, radius: float) -> None:
        """Scales the Circle to the new radius"""
        if radius <= 0:
            radius = 1
        self.radius, self.diameter, self.radius_squared = radius_values(radius)
    
    # Collisions and conversion functions
    def as_rect(self) -> pygame.Rect:
        pos = (self.x - self.radius, self.y - self.radius)
        return pygame.Rect(pos, (self.diameter, self.diameter))
    
    def collidepoint(self, *args) -> bool:
        if len(args) == 2:
            x, y = args[0], args[1]
        elif len(args) == 1:
            x, y = args
        else:
            raise ValueError("Must either be (x,y) or x, y")
        
        dx = self.x - x
        dy = self.y - y
        return dx * dx + dy * dy <= self.radius_squared
    
    def collidecircle(self, other: Circle) -> bool:
        if not isinstance(other, Circle):
            raise TypeError("A circle object was expected!")
        
        if self.radius <= 0 or other.radius <= 0:
            raise ValueError("Circle radii must be non 0 positive numbers")
        
        radii_squared = self.radius_squared + \
                        other.radius_squared + \
                        2 * self.radius * other.radius
        dx = self.x - other.x
        dy = self.y - other.y
        
        return dx * dx + dy * dy <= radii_squared
    
    def colliderect(self, other: pygame.Rect) -> bool:
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
        
        return dx * dx + dy * dy <= self.radius_squared
    
    def __call__(self, *args, **kwargs):
        return (self.x, self.y), self.radius
    
    def __repr__(self) -> str:
        return f"Circle({(self.x, self.y)}, {self.radius})"
