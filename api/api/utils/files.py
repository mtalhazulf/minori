from pathlib import Path
from typing import Union


def get_hash(path: Union[str, Path], hash_algoritm):
    BUF_SIZE = 65536  # lets read stuff in 64kb chunks!
    with open(path, "rb") as f:
        hash = hash_algoritm()
        while True:
            bytes = f.read(BUF_SIZE)  # read entire file as bytes
            if not bytes:
                break
            hash.update(bytes)

    return hash.hexdigest()
