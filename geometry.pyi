from typing import (
    Optional,
    Tuple,
    Sequence,
    overload,
    Union,
    Callable,
    List,
    Iterator,
)

from typing_extensions import Literal as Literal
from typing_extensions import Protocol

from pygame.math import Vector2, Vector3
from pygame.rect import Rect


Coordinate = Union[Tuple[float, float], Sequence[float], Vector2]

_CanBeLine = Union[
    Rect,
    "Line",
    Tuple[float, float, float, float],
    Tuple[Coordinate, Coordinate],
    Sequence[float],
    Sequence[Coordinate],
]

class _HasLineAttribute(Protocol):
    # An object that has a line attribute that is either a line, or a function
    # that returns a line confirms to the rect protocol
    line: Union[LineValue, Callable[[], LineValue]]

LineValue = Union[_CanBeLine, _HasLineAttribute]


class Line:
    x1: float
    y1: float
    x2: float
    y2: float
    a: Tuple[float, float]
    b: Tuple[float, float]
    __safe_for_unpickling__: Literal[True]
    __hash__: None  # type: ignore

    @overload
    def __init__(self, line: Line) -> None: ...
    @overload
    def __init__(self, x1: float, y1: float, x2: float, y2: float) -> None: ...
    @overload
    def __init__(self, first: Sequence[float], second: Sequence[float]) -> None: ...
    @overload
    def __init__(self, single_arg: LineValue) -> None: ...
    def __len__(self) -> Literal[4]: ...
    def __iter__(self) -> Iterator[float]: ...
    @overload
    def __getitem__(self, i: int) -> float: ...
    @overload
    def __getitem__(self, s: slice) -> List[float]: ...
    @overload
    def __setitem__(self, key: int, value: float) -> None: ...
    @overload
    def __setitem__(self, key: slice, value: Union[float, Line]) -> None: ...
    def __copy__(self) -> "Line": ...
    copy = __copy__
    @overload
    def update(self, left: float, top: float, width: float, height: float) -> None: ...
    @overload
    def update(self, left_top: Coordinate, width_height: Coordinate) -> None: ...
    @overload
    def update(self, single_arg: LineValue) -> None: ...
    @overload
    def collidepoint(self, x: float, y: float) -> bool: ...
    @overload
    def collidepoint(self, x_y: Coordinate) -> bool: ...
    @overload
    def collideline(self, line: Line) -> bool: ...
    @overload
    def collideline(self, x1: float, y1: float, x2: float, y2: float) -> bool: ...
    @overload
    def collideline(self, first: Sequence[float], second: Sequence[float]) -> bool: ...
    @overload
    def raycast(self, line: Line) -> Optional[Tuple[float, float]]: ...
    @overload
    def raycast(self, x1: float, y1: float, x2: float, y2: float) -> Optional[Tuple[float, float]]: ...
    @overload
    def raycast(self, first: Sequence[float], second: Sequence[float]) -> Optional[Tuple[float, float]]: ...


_CanBeCircle = Union[
    Vector3,
    "Circle",
    Tuple[float, float, float],
    Sequence[float]
]
class _HasCirclettribute(Protocol):
    # An object that has a circle attribute that is either a circle, or a function
    # that returns a circle
    circle: Union[CircleValue, Callable[[], CircleValue]]

CircleValue = Union[_CanBeCircle, _HasCirclettribute]


class Circle:
    x: float
    y: float
    r: float
    r_sqr: float
    __safe_for_unpickling__: Literal[True]
    __hash__: None  # type: ignore

    @overload
    def __init__(self, circle: Circle) -> None: ...
    @overload
    def __init__(self, x: float, y: float, r: float) -> None: ...
    @overload
    def __init__(self, single_arg: CircleValue) -> None: ...
    def __copy__(self) -> "Circle": ...
    copy = __copy__