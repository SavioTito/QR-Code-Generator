"""
qrgen - A simple, offline QR Code Generator.

Public API:
    build_qr_image(data, ...) -> PIL.Image
    embed_logo(qr_img, logo_path, ...) -> PIL.Image
    generate_qr(data, output, ...) -> pathlib.Path
"""
from .core import build_qr_image, embed_logo, generate_qr, ERROR_LEVELS

__version__ = "1.0.0"
__all__ = ["build_qr_image", "embed_logo", "generate_qr", "ERROR_LEVELS"]
