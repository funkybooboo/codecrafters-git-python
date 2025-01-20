import sys
import os
from typing import List, Dict, Callable
import zlib
import hashlib


def main():
    # You can use print statements as follows for debugging, they'll be visible when running tests.
    # print("Logs from your program will appear here!", file=sys.stderr)
    command_map: Dict[str, Callable[[List[str]], None]] = {
        "init": init,
        "cat-file": cat_file,
        "hash-object": hash_object
    }

    command: str = sys.argv[1]
    args: List[str] = sys.argv[2:]

    command_func = command_map[command]
    if command_func:
        command_func(args)
    else:
        raise RuntimeError(f"Unknown command #{command}")


def init(args: List[str]):
    os.mkdir(".git")
    os.mkdir(".git/objects")
    os.mkdir(".git/refs")
    with open(".git/HEAD", "w", encoding='utf-8') as f:
        f.write("ref: refs/heads/main\n")
    print("Initialized git directory")


def cat_file(args: List[str]):
    if len(args) == 2 and args[0] == "-p":
        blob_sha: str = args[1]
        blob_dir_name: str = blob_sha[:2]
        blob_file_name: str = blob_sha[2:]
        with open(f".git/objects/{blob_dir_name}/{blob_file_name}", "rb") as f:
            compressed_line: bytes = f.readline()
            decompressed_data: bytes = zlib.decompress(compressed_line)
            line: str = decompressed_data.decode("utf-8")
            null_byte_index: int = line.find("\0")
            content: str = line[null_byte_index+1:]
            print(content, end="")


def hash_object(args: List[str]):
    if len(args) == 2 and args[0] == "-w":
        file_path: str = args[1]

        size: int = os.path.getsize(file_path)
        with open(file_path, "rb") as f:
            content: bytes = f.read()

        line: bytes = f"blob {size}\0".encode('utf-8') + content

        sha1_hash = hashlib.sha1()
        sha1_hash.update(line)
        blob_sha: str = sha1_hash.hexdigest()

        print(blob_sha, end="")

        blob_dir_name: str = blob_sha[:2]
        blob_file_name: str = blob_sha[2:]

        compressed_line: bytes = zlib.compress(line)

        os.makedirs(f".git/objects/{blob_dir_name}", exist_ok=True)

        with open(f".git/objects/{blob_dir_name}/{blob_file_name}", "wb") as f:
            f.write(compressed_line)


if __name__ == "__main__":
    main()
