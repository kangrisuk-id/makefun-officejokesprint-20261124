#!/usr/bin/env python3
"""One-Line Office Joke: 24-Hour Sprint — entry program.

Writes this entry's single-line office joke to ``entry.txt`` in the
output directory. Pure Python standard library; no dependencies,
no network, nothing read from outside this file.

Output contract: the first writable directory wins, tried in order —
``$MAKEFUN_OUTPUT_DIR``, ``/output``, the directory beside this
script, then ``/tmp``. Each candidate is attempted independently and
an ``OSError`` on one simply moves on to the next.
"""

import os
import sys

JOKE = (
    "The office plant has survived four managers, two restructures "
    "and a flood, so we've quietly started reporting to it."
)

OUTPUT_NAME = "entry.txt"


def candidate_dirs() -> list:
    """Output directories to try, most preferred first."""
    dirs = []
    env_dir = os.environ.get("MAKEFUN_OUTPUT_DIR")
    if env_dir:
        dirs.append(env_dir)
    dirs.append("/output")
    dirs.append(os.path.dirname(os.path.abspath(__file__)))
    dirs.append("/tmp")
    return dirs


def write_joke() -> str:
    """Write the joke to the first writable candidate; return its path."""
    if not 1 <= len(JOKE) <= 200:
        raise ValueError("joke must be 1-200 characters")
    last_error = None
    for directory in candidate_dirs():
        try:
            os.makedirs(directory, exist_ok=True)
            path = os.path.join(directory, OUTPUT_NAME)
            with open(path, "w", encoding="utf-8") as handle:
                handle.write(JOKE)
            return path
        except OSError as error:  # read-only or missing dir: try the next
            last_error = error
    raise OSError(f"no writable output directory: {last_error}")


def main() -> int:
    try:
        write_joke()
    except (OSError, ValueError) as error:
        print(f"error: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
