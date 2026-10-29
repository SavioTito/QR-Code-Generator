#!/usr/bin/env python3
"""Entry point for the QR Code Generator.

- With no arguments it launches the graphical (Tkinter) interface.
- With arguments it behaves as the command-line tool.

Examples:
    python main.py                               # open the GUI
    python main.py "https://www.cuchd.in"        # CLI: encode a URL
    python main.py "Hello" -o hello.png -e H     # CLI with options
"""
import sys


def main() -> None:
    if len(sys.argv) > 1:
        from qrgen.cli import main as cli_main
        raise SystemExit(cli_main())

    from qrgen.gui import main as gui_main
    gui_main()


if __name__ == "__main__":
    main()
