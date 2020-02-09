import time

from utils import logger


class DBHandler:
    def __init__(self, db):
        self.db = db
        self.is_closed = False

    @staticmethod
    def read_n_records(limit: int):
        return [(i, f"row [i]") for i in range(limit)]

    def close(self):
        logger.debug(f"Closing connection to database {self.db}")
        self.is_closed = True


def stream_db_records(db_handler: DBHandler):
    try:
        while True:
            yield db_handler.read_n_records(10)
            time.sleep(1)
    except GeneratorExit:
        db_handler.close()


class CustomException(Exception):
    """An exception of the domain model."""


def stream_data(db_handler: DBHandler):
    while True:
        try:
            yield db_handler.read_n_records(10)
        except CustomException as e:
            logger.info(f"controlled error {e!r}, continuing", e)
        except Exception as e:
            logger.info(f"unhandled error {e!r}, stopping", e)
            db_handler.close()
            break


if __name__ == "__main__":
    streamer = stream_db_records(DBHandler("test_db"))
    print(next(streamer))
    print(next(streamer))
    streamer.close()

    streamer = stream_data(DBHandler("test_db"))
    print(next(streamer))
    print(next(streamer))
    streamer.throw(CustomException)
    streamer.throw(RuntimeError)
