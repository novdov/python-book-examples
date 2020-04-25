import hashlib
import os
import shutil
from enum import Enum, auto
from pathlib import Path
from typing import Dict, Generator, Union

BLOCK_SIZE = 65536


class Action(Enum):
    COPY = auto()
    MOVE = auto()
    DELETE = auto()


def sync(source: Union[str, Path], dest: Union[str, Path]) -> None:
    """Synchronize two file directories, source and dest.

    :param source: Union[str, Path]. source directory
    :param dest: Union[str, Path]. destination directory
    :return: None. Synchronize two directories and terminate function.
    """
    source_hashes = read_paths_and_hashes(source)
    dest_hashes = read_paths_and_hashes(dest)

    # step 2: call functional core
    actions = determine_actions(source_hashes, dest_hashes, source, dest)

    # imperative shell step 3, apply outputs
    for action, *paths in actions:
        if action == Action.COPY:
            shutil.copyfile(*paths)
        if action == Action.MOVE:
            shutil.move(*paths)
        if action == Action.DELETE:
            os.remove(paths[0])


def determine_actions(
    src_hashes: Dict[str, str],
    dst_hashes: Dict[str, str],
    src_folder: Union[str, Path],
    dst_folder: Union[str, Path],
) -> Generator:
    src_folder = _to_path(src_folder)
    dst_folder = _to_path(dst_folder)

    for sha, filename in src_hashes.items():

        if sha not in dst_hashes:
            source_path = src_folder.joinpath(filename)
            dest_path = dst_folder.joinpath(filename)
            yield Action.COPY, source_path, dest_path

        elif dst_hashes[sha] != filename:
            old_dest_path = dst_folder.joinpath(dst_hashes[sha])
            newed_dest_path = dst_folder.joinpath(filename)
            yield Action.MOVE, old_dest_path, newed_dest_path

    for sha, filename in dst_hashes.items():
        if sha not in src_hashes:
            yield Action.DELETE, dst_folder.joinpath(filename)


def read_paths_and_hashes(root: Union[str, Path]) -> Dict[str, str]:
    hashes = dict()
    for file in Path(root).rglob("*"):
        hashes[hash_file(file)] = file.name
    return hashes


def hash_file(path: Union[str, Path]) -> str:
    hasher = hashlib.sha1()
    with Path(path).open("rb") as file:
        buf = file.read(BLOCK_SIZE)
        while buf:
            hasher.update(buf)
            buf = file.read(BLOCK_SIZE)
    return hasher.hexdigest()


def _to_path(p):
    return Path(p)
