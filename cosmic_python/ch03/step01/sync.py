import hashlib
import os
import shutil
from pathlib import Path
from typing import Union

BLOCK_SIZE = 65536


def hash_file(path: Union[str, Path]) -> str:
    hasher = hashlib.sha1()
    with Path(path).open("rb") as file:
        buf = file.read(BLOCK_SIZE)
        while buf:
            hasher.update(buf)
            buf = file.read(BLOCK_SIZE)
    return hasher.hexdigest()


def sync(source: Union[str, Path], dest: Union[str, Path]) -> None:
    """Synchronize two file directories, source and dest.

    :param source: Union[str, Path]. source directory
    :param dest: Union[str, Path]. destination directory
    :return: None. Synchronize two directories and terminate function.
    """
    source_hashes = dict()
    for folder, _, files in os.walk(source):
        for filename in files:
            source_hashes[hash_file(Path(folder).joinpath(filename))] = filename

    seen = set()
    for folder, _, files in os.walk(dest):
        for filename in files:
            dest_path = Path(folder).joinpath(filename)
            dest_hash = hash_file(dest_path)
            seen.add(dest_hash)

            # If there's a file in target that's not in source, delete it
            if dest_hash not in source_hashes:
                dest_path.remove()
            # If there's a file in target that has a difference path in source,
            # move it to the correct path
            elif dest_hash in source_hashes and filename != source_hashes[dest_hash]:
                shutil.move(dest_path, Path(folder).joinpath(source_hashes[dest_hash]))
        # For every file that appears in source but not target, copy the file to the target
        for source_hash, filename in source_hashes.items():
            if source_hash not in seen:
                shutil.copy(Path(source).joinpath(filename), Path(dest).joinpath(filename))
