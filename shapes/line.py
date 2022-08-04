from typing import Sequence, Tuple


class LineSegment:
    def __init__(
        self,
        point1: Sequence[Tuple[float, float]],
        point2: Sequence[Tuple[float, float]],
    ) -> None:
        super().__init__()
        self.point1 = point1
        self.point2 = point2
        self.iters = [self.point1[0], self.point1[1], self.point2[0], self.point2[1]]

    def __getitem__(self, index):
        return self.iters[index]

    def __iter__(self):
        self._n = 0
        return self.iters

    def __next__(self):
        if self._n < 4:
            self._n += 1
            return self.iters[self._n - 1]
        else:
            raise StopIteration
