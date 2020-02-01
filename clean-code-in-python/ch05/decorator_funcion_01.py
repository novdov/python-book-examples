import functools

from utils.logger import logger

RETRIES_LIMIT = 3


class ControlledException(Exception):
    """A generic exception on the program's domain."""


def retry(operation):
    @functools.wraps(operation)
    def wrapped(*args, **kwargs):
        last_raised = None
        for _ in range(RETRIES_LIMIT):
            try:
                return operation(*args, **kwargs)
            except ControlledException as e:
                logger.info(f"retrying {operation.__qualname__}")
                last_raised = e
        raise last_raised

    return wrapped


class OperationObject:
    def __init__(self):
        self._times_called = 0

    def run(self) -> int:
        self._times_called += 1
        return self._times_called

    def __str__(self):
        return f"{self.__class__.__name__}()"

    __repr__ = __str__


class RunWithFailure:
    def __init__(
        self, task: OperationObject, fall_n_times: int = 0, exception_cls=ControlledException,
    ):
        self._task = task
        self._fall_n_times = fall_n_times
        self._times_failed = 0
        self._exception_cls = exception_cls

    def run(self):
        called = self._task.run()
        if self._times_failed < self._fall_n_times:
            self._times_failed += 1
            raise self._exception_cls(f"{self._task!s} failed")
        return called


@retry
def run_operation(task):
    return task.run()


if __name__ == "__main__":
    task = OperationObject()
    failing_task = RunWithFailure(task, fall_n_times=2)
    times_run = run_operation(failing_task)

    print(times_run)
