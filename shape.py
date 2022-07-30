from __future__ import annotations

from abc import ABC, abstractmethod

__all__ = "Shape"

import pygame


class Shape(ABC):
    
    @abstractmethod
    def copy(self):
        """"""
    
    @abstractmethod
    def update(self, *args) -> None:
        """"""
    
    @abstractmethod
    def collidepoint(self, *args) -> bool:
        """"""
    
    @abstractmethod
    def colliderect(self, other: Shape) -> bool:
        """"""
    
    @abstractmethod
    def collidecircle(self, other: Shape) -> bool:
        """"""
    
    # IDEA: general purpose collide that will dispatch to correct method for
    # shape type vs shape type
    @abstractmethod
    def as_rect(self) -> pygame.Rect:
        """"""
    
    def __repr__(self):
        """"""
