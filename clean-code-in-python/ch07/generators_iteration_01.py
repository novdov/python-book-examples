class SequenceIterator:
    """Non-iterable iterator."""

    def __init__(self, start: int = 0, step: int = 1):
        self.current = start
        self.step = step

    def __next__(self):
        value = self.current
        self.current += self.step
        return value


if __name__ == "__main__":
    si = SequenceIterator(1, 2)
    for _ in range(5):
        print(next(si))

    # Raise TypeError: not iterable
    # for _ in SequenceIterator():
    #     pass
