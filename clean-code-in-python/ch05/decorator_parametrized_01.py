import functools

from utils.logger import logger

RETRIES_LIMIT = 3


class ControlledException(Exception):
    """A generic exception on the program's domain."""


def with_retry(retries_limit: int = RETRIES_LIMIT, allowed_exceptions=None):
    allowed_exceptions = allowed_exceptions or (ControlledException,)

    def retry(operation):
        @functools.wraps(operation)
        def wrapped(*args, **kwargs):
            last_retried = None
            for _ in range(retries_limit):
                try:
                    return operation(*args, **kwargs)
                except allowed_exceptions as e:
                    logger.info(f"retrying {operation} due to {e}")
                    last_retried = e
            raise last_retried

        return wrapped

    return retry


@with_retry()
def run_operation(task):
    return task.run()


@with_retry(retries_limit=5)
def run_with_custom_retries_limit(task):
    return task.run()


@with_retry(allowed_exceptions=(AttributeError,))
def run_with_custom_exception(task):
    return task.run()


@with_retry(retries_limit=4, allowed_exceptions=(ZeroDivisionError, AttributeError))
def run_with_custom_parameters(task):
    return task.run()
