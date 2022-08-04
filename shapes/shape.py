from __future__ import annotations

from abc import ABC, abstractmethod

__all__ = "Shape"

import pygame


class Shape(ABC):
    """The abstract base class for Shapes
    Implements functions for collision, updating and conversion
    """

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

    # @abstractmethod
    # def collideline(self, other: Shape) -> bool:
    #     """"""

    @abstractmethod
    def collides_with(self, other: Shape) -> bool:
        """"""

    @abstractmethod
    def as_rect(self) -> pygame.Rect:
        """"""

    def __repr__(self):
        """"""
