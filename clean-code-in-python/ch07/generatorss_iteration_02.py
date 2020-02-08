from typing import Callable

from utils import logger


class MappedRange:
    """Apply a transformation to a range of numbers."""

    def __init__(self, transformation: Callable, start: int, end: int):
        self._transformation = transformation
        self._wrapped = range(start, end)

    def __getitem__(self, index: int):
        value = self._wrapped.__getitem__(index)
        result = self._transformation(value)
        logger.debug(f"Index {index}: {result}")
        return result

    def __len__(self):
        return len(self._wrapped)


if __name__ == "__main__":
    mr = MappedRange(abs, -10, 5)
    print(mr[0], mr[-1])
    mr_list = list(mr)
