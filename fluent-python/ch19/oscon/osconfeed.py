import json
import warnings
from pathlib import Path
from urllib.request import urlopen

URL = "http://www.oreilly.com/pub/sc/osconfeed"
JSON = Path(__file__).absolute().parent.joinpath("data/osconfeed.json")


def load():
    if not JSON.exists():
        msg = f"downloading {URL} to {JSON}"
        warnings.warn(msg)

        with urlopen(URL) as remote, open(JSON, "wb") as local:
            local.write(remote.read())

    with open(JSON) as fp:
        return json.load(fp)


if __name__ == "__main__":
    feed = load()
    print(sorted(feed["Schedule"].keys()))

    for key, value in sorted(feed["Schedule"].items()):
        print(f"{len(value):3} {key}")
