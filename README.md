# QR Code Generator

A simple, **offline** QR Code Generator written in Python. It converts any text or
URL into a scannable QR code image, with an optional logo embedded in the centre.
The project ships with both a **command-line interface** and a **Tkinter GUI**.

> Mini project for the **Python Programming (24SCH-301)** course
> University Institute of Computing (UIC), Chandigarh University.

---

## Features

- Generate QR codes from any text or URL
- Four error-correction levels: **L (~7%)**, **M (~15%)**, **Q (~25%)**, **H (~30%)**
- Embed a logo in the centre (error correction is automatically raised to **H**)
- Customisable foreground / background colours, module size and quiet-zone border
- Clean separation of logic (`qrgen.core`) from the CLI (`qrgen.cli`) and GUI (`qrgen.gui`)
- No paid service and no internet connection required

---

## Demo

| URL | Plain text | With logo |
|:---:|:---:|:---:|
| ![URL QR](examples/qr_url.png) | ![Text QR](examples/qr_text.png) | ![Branded QR](examples/qr_branded.png) |

---

## Installation

Requires **Python 3.8+**.

```bash
# clone the repository
git clone https://github.com/<your-username>/qr-code-generator.git
cd qr-code-generator

# (optional) create a virtual environment
python -m venv .venv
source .venv/bin/activate      # on Windows: .venv\Scripts\activate

# install dependencies
pip install -r requirements.txt
```

---

## Usage

### Graphical interface (GUI)

```bash
python main.py
```

Type the text or URL, pick an error-correction level, optionally choose a logo,
click **Generate** to preview, then **Save as PNG**.

### Command line (CLI)

```bash
# encode a URL (default output: qrcode.png)
python main.py "https://www.cuchd.in"

# choose an output file and error-correction level
python main.py "Hello World" -o hello.png -e H

# embed a logo in the centre (error correction forced to H)
python main.py "https://www.cuchd.in" --logo assets/cu_logo.png -o branded.png

# custom colours
python main.py "https://www.cuchd.in" --fill "#003366" --back "#f5f5f5"
```

You can also run the CLI module directly:

```bash
python -m qrgen.cli "https://www.cuchd.in"
```

#### CLI options

| Option | Description | Default |
|---|---|---|
| `data` | Text or URL to encode (prompted for if omitted) | — |
| `-o`, `--output` | Output image file | `qrcode.png` |
| `-e`, `--error` | Error-correction level: `L`, `M`, `Q`, `H` | `M` |
| `--fill` | Foreground colour | `black` |
| `--back` | Background colour | `white` |
| `--logo` | Path to a logo image to embed | — |
| `--box-size` | Pixels per QR module | `10` |
| `--border` | Quiet-zone width in modules | `4` |

---

## Use as a library

```python
from qrgen import generate_qr

# simple
generate_qr("https://www.cuchd.in", "qr.png")

# with a logo (error correction is raised to H automatically)
generate_qr("https://www.cuchd.in", "branded.png", logo="assets/cu_logo.png")
```

---

## Project structure

```
qr-code-generator/
├── main.py              # entry point (GUI with no args, CLI with args)
├── qrgen/
│   ├── __init__.py      # public API
│   ├── core.py          # QR generation + logo embedding (UI-independent)
│   ├── cli.py           # command-line interface (argparse)
│   └── gui.py           # Tkinter graphical interface
├── assets/
│   └── cu_logo.png      # sample logo for the --logo option
├── examples/            # sample generated QR codes
├── requirements.txt
├── LICENSE
└── README.md
```

---

## How it works

1. The input is validated (it must not be empty).
2. A `qrcode.QRCode` object is created with the chosen error-correction level.
3. The data is added and the module matrix is generated (`make(fit=True)` picks
   the smallest version that fits).
4. The matrix is rendered to a Pillow image.
5. If a logo is requested, it is pasted onto a white pad in the centre, using the
   logo's alpha channel as a mask.
6. The image is previewed (GUI) and saved as a PNG.

---

## Author

**Savio Tito** — UID 24BSC10046
BSc. Computer Science, Batch 24BSC-1
University Institute of Computing, Chandigarh University

## License

Released under the [MIT License](LICENSE).
# QR-Code-Generator
