import warnings

import osconfeed

DB_NAME = "data/schedule1_db"
CONFERENCE = "conference.115"


class Record:
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)


def load_db(db):
    raw_data = osconfeed.load()
    warnings.warn(f"loading {DB_NAME}")
    for collection, rec_list in raw_data["Schedule"].items():
        record_type = collection[:-1]
        for record in rec_list:
            key = f"{record_type}.{record['serial']}"
            record["serial"] = key
            db[key] = Record(**record)
