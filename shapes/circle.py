from __future__ import annotations

from typing import Sequence, Tuple

import pygame

from shapes.shape import Shape

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
        """Returns a new Circle object that's a copy of the original"""
        return Circle((self.x, self.y), self.radius)
    
    # Movement, scale and position functions
    def update(self, center: Sequence[float, float], radius: float) -> None:
        """Updates the x and y position and radius in place"""
        if radius <= 0:
            radius = 1
        self.x, self.y = center
        self.radius, self.diameter, self.radius_squared = radius_values(radius)
    
    def move(self, x: float, y: float) -> Circle:
        """Returns a new Circle that's moved by the x and y offsets and
           has the same radius as the original
        """
        return Circle((self.x + x, self.y + y), self.radius)
    
    def move_ip(self, x: float, y: float) -> None:
        """Moves the circle's position by the x and y offsets in place"""
        self.x += x
        self.y += y
    
    def move_to(self, x: float, y: float) -> Circle:
        """Returns a new Circle with x and y as position and
           same radius as self
        """
        return Circle((x, y), self.radius)
    
    def move_to_ip(self, x: float, y: float) -> None:
        """Set the circle's x and y positions to the new position in place"""
        self.x = x
        self.y = y
    
    def scale(self, radius: float) -> Circle:
        """Return a new Circle with position as self and updated radius"""
        if radius <= 0:
            radius = 1
        return Circle((self.x, self.y), radius)
    
    def scale_ip(self, radius: float) -> None:
        """Scales the Circle to the new radius in place"""
        if radius <= 0:
            radius = 1
        self.radius, self.diameter, self.radius_squared = radius_values(radius)
    
    def scale_by(self, amount: float) -> Circle:
        """Returns a new Circle with same position as self and updated radius"""
        if amount <= 0:
            raise ValueError("Invalid amount passes")
        radius = self.radius
        if radius * amount <= 0:
            radius = 1
        
        return Circle((self.x, self.y), radius * amount)
    
    def scale_by_ip(self, amount: float) -> None:
        """Scales the Circle to the new radius in place"""
        if amount <= 0:
            raise ValueError("Invalid amount passes")
        
        self.radius *= amount
        
        if self.radius <= 1:
            self.radius = 1
        
        self.radius, self.diameter, self.radius_squared = radius_values(
            self.radius)
    
    # Collisions and conversion functions
    def as_rect(self) -> pygame.Rect:
        """Returns the rectangle that fully encloses the circle"""
        pos = (self.x - self.radius, self.y - self.radius)
        return pygame.Rect(pos, (self.diameter, self.diameter))
    
    def collides_with(self, shape: Shape) -> bool:
        """General collision function, accepts any implemented Shape.
           Checks whether the circle collides with a Shape,
           returns True if they do, False otherwise
        """
        if isinstance(shape, Circle):
            return self.collidecircle(shape)
        elif isinstance(shape, pygame.Rect):
            return self.colliderect(shape)
        else:
            raise NotImplementedError(
                "The shape type does not exist yet"
                " or doesn't have a matching collision algorythm"
            )
    
    def collidepoint(self, *args) -> bool:
        """Checks whether the circle collides with a point,
           returns True if they do, False otherwise
        """
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
        """Checks whether the circle collides with the other circle,
           returns True if they do, False otherwise
        """
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
        
        return dx * dx + dy * dy <= self.radius_squared
    
    # def collideline(self, other: Line) -> bool:
    
    def __call__(self, *args, **kwargs):
        return (self.x, self.y), self.radius
    
    def __repr__(self) -> str:
        return f"Circle({(self.x, self.y)}, {self.radius})"
