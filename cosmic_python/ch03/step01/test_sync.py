import shutil
import tempfile
from pathlib import Path

from . import sync


def test_when_a_file_exists_in_the_source_but_not_the_dest():
    try:
        source = tempfile.mkdtemp()
        dest = tempfile.mkdtemp()

        content = "I am a very useful file"
        filename = "my-file"
        Path(source).joinpath(filename).write_text(content)

        sync.sync(source, dest)

        expected_path = Path(dest).joinpath(filename)

        assert expected_path.exists()
        assert expected_path.read_text() == content
    finally:
        shutil.rmtree(source)
        shutil.rmtree(dest)


def test_when_a_has_been_removed_in_the_source():
    try:
        source = tempfile.mkdtemp()
        dest = tempfile.mkdtemp()

        content = "I am a file that was renamed"
        source_path = Path(source).joinpath("source-filename")
        old_dest_path = Path(dest).joinpath("dest-filename")
        expected_dest_path = Path(dest).joinpath("source-filename")

        source_path.write_text(content)
        old_dest_path.write_text(content)

        sync.sync(source, dest)

        assert old_dest_path.exists() is False
        assert expected_dest_path.read_text() == content
    finally:
        shutil.rmtree(source)
        shutil.rmtree(dest)
