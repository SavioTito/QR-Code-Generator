"""Tkinter graphical interface for the QR code generator.

Run with:
    python -m qrgen.gui
or simply:
    python main.py
"""
from __future__ import annotations

import tkinter as tk
from tkinter import filedialog, messagebox, ttk

from PIL import ImageTk

from .core import build_qr_image, embed_logo

FONT = ("Times New Roman", 12)
TITLE_FONT = ("Times New Roman", 16, "bold")


class QRGeneratorApp:
    """A small desktop app that turns text/URLs into QR code images."""

    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title("QR Code Generator")
        self.root.geometry("440x600")
        self.root.resizable(False, False)

        self.qr_image = None   # the current PIL image (for saving)
        self.logo_path = None  # optional logo file

        self._build_widgets()

    # ------------------------------------------------------------------ UI
    def _build_widgets(self) -> None:
        tk.Label(self.root, text="QR Code Generator", font=TITLE_FONT).pack(pady=12)

        tk.Label(self.root, text="Enter text or URL:", font=FONT).pack()
        self.entry = tk.Entry(self.root, width=42, font=FONT)
        self.entry.pack(pady=6)
        self.entry.focus()

        # Options row: error-correction level
        opts = tk.Frame(self.root)
        opts.pack(pady=4)
        tk.Label(opts, text="Error correction:", font=FONT).grid(row=0, column=0, padx=4)
        self.error_var = tk.StringVar(value="M")
        ttk.Combobox(
            opts, textvariable=self.error_var, values=["L", "M", "Q", "H"],
            width=5, state="readonly",
        ).grid(row=0, column=1, padx=4)

        # Optional logo
        logo_frame = tk.Frame(self.root)
        logo_frame.pack(pady=4)
        tk.Button(logo_frame, text="Choose logo...", command=self.choose_logo).grid(
            row=0, column=0, padx=4
        )
        self.logo_label = tk.Label(logo_frame, text="(no logo)", font=("Times New Roman", 10))
        self.logo_label.grid(row=0, column=1, padx=4)

        tk.Button(self.root, text="Generate", width=16, command=self.generate).pack(pady=10)

        self.preview = tk.Label(self.root)
        self.preview.pack(pady=10)

        self.save_btn = tk.Button(
            self.root, text="Save as PNG", width=16, command=self.save, state=tk.DISABLED
        )
        self.save_btn.pack(pady=5)

    # -------------------------------------------------------------- actions
    def choose_logo(self) -> None:
        path = filedialog.askopenfilename(
            title="Select a logo image",
            filetypes=[("Image files", "*.png *.jpg *.jpeg")],
        )
        if path:
            self.logo_path = path
            name = path.rsplit("/", 1)[-1]
            self.logo_label.config(text=name)

    def generate(self) -> None:
        data = self.entry.get().strip()
        if not data:
            messagebox.showwarning("Input required", "Please enter some text or a URL.")
            return

        # A logo covers part of the code, so force the strongest error correction.
        error = "H" if self.logo_path else self.error_var.get()

        try:
            img = build_qr_image(data, error=error, box_size=8, border=4)
            if self.logo_path:
                img = embed_logo(img, self.logo_path)
        except Exception as exc:  # noqa: BLE001 - surface any error to the user
            messagebox.showerror("Error", str(exc))
            return

        self.qr_image = img
        tk_img = ImageTk.PhotoImage(img.resize((260, 260)))
        self.preview.config(image=tk_img)
        self.preview.image = tk_img  # keep a reference so it is not garbage-collected
        self.save_btn.config(state=tk.NORMAL)

    def save(self) -> None:
        if self.qr_image is None:
            return
        path = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[("PNG Image", "*.png")],
            initialfile="qrcode.png",
        )
        if path:
            self.qr_image.save(path)
            messagebox.showinfo("Saved", f"QR code saved to:\n{path}")


def main() -> None:
    root = tk.Tk()
    QRGeneratorApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
