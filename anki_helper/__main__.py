"""Command-line entry point: python3 -m anki_helper <command>"""

from __future__ import annotations

import argparse
import sys

from .ankiconnect import AnkiConnect, AnkiConnectError
from .notetype import MODEL_NAME, ensure_note_type


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="anki_helper")
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("setup", help=f"create or update the {MODEL_NAME!r} note type in Anki")
    args = parser.parse_args(argv)

    ac = AnkiConnect()
    try:
        if args.command == "setup":
            print(f"Note type {MODEL_NAME!r}: {ensure_note_type(ac)}")
    except AnkiConnectError as e:
        print(f"error: {e}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
