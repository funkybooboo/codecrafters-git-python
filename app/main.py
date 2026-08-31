import sys
import os
import zlib


def main():
    # You can use print statements as follows for debugging, they'll be visible when running tests.
    # print("Logs from your program will appear here!", file=sys.stderr)

    if len(sys.argv) < 1:
        raise RuntimeError("No arg")

    command = sys.argv[1]

    if command == "init":
        os.mkdir(".git")
        os.mkdir(".git/objects")
        os.mkdir(".git/refs")
        with open(".git/HEAD", "w") as f:
            f.write("ref: refs/heads/main\n")
        print("Initialized git directory")

    elif command == "cat-file":
        if len(sys.argv) < 4:
            raise RuntimeError("Usage: cat-file -p <hash>")

        flag = sys.argv[2]
        if flag == "-p":
            hash = sys.argv[3]
            dir = hash[0] + hash[1]
            file = hash[2:]
            path = f".git/objects/{dir}/{file}"
            with open(path, "rb") as f:
                compressed = f.read()
            raw = zlib.decompress(compressed)
            null_idx = raw.index(b"\x00")
            _header = raw[:null_idx].decode("ascii")
            content = raw[null_idx + 1 :]
            try:
                print(content.decode("utf-8"), end="")
            except UnicodeDecodeError:
                sys.stdout.buffer.write(content)
        else:
            raise RuntimeError("Unknown flag")

    else:
        raise RuntimeError(f"Unknown command #{command}")


if __name__ == "__main__":
    main()
