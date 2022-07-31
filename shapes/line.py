from typing import Sequence
from shape import Shape


class Line:
    def __init__(self, point1: Sequence[float], point2: Sequence[float]) -> None:
        super().__init__()
        self.point1 = point1
        self.point2 = point2
        self.iters = [self.point1[0], self.point1[1], self.point2[0], self.point2[1]]

    def __iter__(self):
        self._n = 0
        return self

    def __next__(self):
        if self._n < 4:
            self._n += 1
            return self.iters[self._n - 1]
        else:
            raise StopIteration
