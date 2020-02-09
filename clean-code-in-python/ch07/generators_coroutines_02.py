def stream_db_records(db_handler):
    retrieved_data = None
    page_size = 10
    try:
        while True:
            page_size = (yield retrieved_data) or page_size
            retrieved_data = db_handler.read_n_records(page_size)
    except GeneratorExit:
        db_handler.close()


def prepare_coroutine(coroutine):
    def wrapped(*args, **kwargs):
        advanced_coroutine = coroutine(*args, **kwargs)
        next(advanced_coroutine)
        return advanced_coroutine

    return wrapped


@prepare_coroutine
def auto_stream_db_records(db_handler):
    retrieved_data = None
    page_size = 10
    try:
        while True:
            page_size = (yield retrieved_data) or page_size
            retrieved_data = db_handler.read_n_records(page_size)
    except GeneratorExit:
        db_handler.close()
