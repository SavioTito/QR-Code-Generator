"""Core QR code generation logic.

This module contains the pure, UI-independent functions used by both the
command-line interface (``qrgen.cli``) and the graphical interface
(``qrgen.gui``).
"""
from __future__ import annotations

from pathlib import Path
from typing import Optional, Union

import qrcode
from qrcode.constants import (
    ERROR_CORRECT_L,
    ERROR_CORRECT_M,
    ERROR_CORRECT_Q,
    ERROR_CORRECT_H,
)
from PIL import Image

# Human-readable error-correction levels mapped to the library constants.
# L ~7%, M ~15%, Q ~25%, H ~30% recovery capacity.
ERROR_LEVELS = {
    "L": ERROR_CORRECT_L,
    "M": ERROR_CORRECT_M,
    "Q": ERROR_CORRECT_Q,
    "H": ERROR_CORRECT_H,
}


def build_qr_image(
    data: str,
    *,
    error: str = "M",
    box_size: int = 10,
    border: int = 4,
    fill: str = "black",
    back: str = "white",
) -> Image.Image:
    """Build a QR code image from ``data``.

    Args:
        data: The text or URL to encode.
        error: Error-correction level, one of ``"L"``, ``"M"``, ``"Q"``, ``"H"``.
        box_size: Number of pixels per QR module.
        border: Width of the quiet zone, in modules (minimum 4 is recommended).
        fill: Foreground (module) color.
        back: Background color.

    Returns:
        A ``PIL.Image.Image`` in RGB mode.

    Raises:
        ValueError: If ``data`` is empty or the error level is invalid.
    """
    if not data or not data.strip():
        raise ValueError("Data to encode cannot be empty.")

    level = ERROR_LEVELS.get(error.upper())
    if level is None:
        raise ValueError(
            f"Invalid error-correction level: {error!r}. Use L, M, Q or H."
        )

    qr = qrcode.QRCode(
        version=None,              # auto-select the smallest version that fits
        error_correction=level,
        box_size=box_size,
        border=border,
    )
    qr.add_data(data)
    qr.make(fit=True)

    return qr.make_image(fill_color=fill, back_color=back).convert("RGB")


def embed_logo(
    qr_img: Image.Image,
    logo_path: Union[str, Path],
    *,
    scale: float = 0.22,
) -> Image.Image:
    """Overlay a logo in the centre of a QR code image.

    The logo is placed on a small white pad so it stays readable. Use this
    only with QR codes built at error-correction level ``"H"`` so the code
    remains scannable despite the covered modules.

    Args:
        qr_img: The QR code image returned by :func:`build_qr_image`.
        logo_path: Path to the logo image (PNG with transparency works best).
        scale: Logo width as a fraction of the QR width (0.0 - 1.0).

    Returns:
        A new ``PIL.Image.Image`` in RGB mode with the logo embedded.
    """
    logo = Image.open(logo_path).convert("RGBA")
    base = qr_img.convert("RGBA")

    qr_w, qr_h = base.size
    logo_w = int(qr_w * scale)
    logo_h = int(logo_w * logo.size[1] / logo.size[0])
    logo = logo.resize((logo_w, logo_h), Image.LANCZOS)

    # White pad behind the logo for contrast.
    pad = Image.new("RGBA", (logo_w + 20, logo_h + 16), (255, 255, 255, 255))
    pad.paste(logo, (10, 8), logo)

    pos = ((qr_w - pad.size[0]) // 2, (qr_h - pad.size[1]) // 2)
    base.paste(pad, pos, pad)
    return base.convert("RGB")


def generate_qr(
    data: str,
    output: Union[str, Path] = "qrcode.png",
    *,
    error: str = "M",
    box_size: int = 10,
    border: int = 4,
    fill: str = "black",
    back: str = "white",
    logo: Optional[Union[str, Path]] = None,
) -> Path:
    """Generate a QR code and save it to ``output``.

    When a ``logo`` is supplied, the error-correction level is automatically
    raised to ``"H"`` (if it was ``"L"`` or ``"M"``) to keep the code readable.

    Returns:
        The :class:`pathlib.Path` of the saved image.
    """
    if logo and error.upper() in ("L", "M"):
        error = "H"

    img = build_qr_image(
        data, error=error, box_size=box_size, border=border, fill=fill, back=back
    )
    if logo:
        img = embed_logo(img, logo)

    output = Path(output)
    if output.parent and not output.parent.exists():
        output.parent.mkdir(parents=True, exist_ok=True)
    img.save(output)
    return output
