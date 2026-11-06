"""Core PDF watermarking logic. Runs 100% locally, no network access."""

import io
import math

from pypdf import PdfReader, PdfWriter
from reportlab.lib.colors import Color
from reportlab.pdfgen import canvas


def _make_overlay(width, height, text, opacity, font_size, angle, color):
    """Build a one-page PDF of the given size with a tiled, rotated text."""
    buf = io.BytesIO()
    c = canvas.Canvas(buf, pagesize=(width, height))
    r, g, b = color
    c.setFillColor(Color(r, g, b, alpha=opacity))
    c.setFont("Helvetica-Bold", font_size)

    text_width = c.stringWidth(text, "Helvetica-Bold", font_size)
    step_x = text_width + font_size * 3
    step_y = font_size * 5
    diag = math.hypot(width, height)

    c.saveState()
    c.translate(width / 2, height / 2)
    c.rotate(angle)
    y = -diag
    row = 0
    while y < diag:
        offset = (step_x / 2) if row % 2 else 0
        x = -diag - offset
        while x < diag:
            c.drawString(x, y, text)
            x += step_x
        y += step_y
        row += 1
    c.restoreState()

    c.showPage()
    c.save()
    buf.seek(0)
    return PdfReader(buf).pages[0]


def hex_to_rgb(value):
    value = value.lstrip("#")
    if len(value) != 6:
        return (0.5, 0.5, 0.5)
    return tuple(int(value[i:i + 2], 16) / 255 for i in (0, 2, 4))


def watermark_pdf(
    pdf_bytes,
    text,
    opacity=0.25,
    font_size=28,
    angle=45,
    color="#808080",
    password=None,
):
    """Return the bytes of a watermarked copy of the given PDF."""
    if not text.strip():
        raise ValueError("Watermark text is empty.")

    reader = PdfReader(io.BytesIO(pdf_bytes))
    if reader.is_encrypted:
        if not reader.decrypt(""):
            raise ValueError("This PDF is password-protected. Remove the password first.")

    rgb = hex_to_rgb(color)
    writer = PdfWriter()
    overlays = {}

    for page in reader.pages:
        # Make the page "upright" so the overlay lines up with what you see.
        page.transfer_rotation_to_content()
        box = page.mediabox
        w, h = float(box.width), float(box.height)
        key = (round(w), round(h))
        if key not in overlays:
            overlays[key] = _make_overlay(w, h, text, opacity, font_size, angle, rgb)
        overlay = overlays[key]
        page.merge_translated_page(overlay, float(box.left), float(box.bottom), over=True)
        writer.add_page(page)

    # Strip original metadata (author, software, dates...).
    writer.add_metadata({"/Producer": "", "/Creator": ""})

    if password:
        writer.encrypt(user_password=password, algorithm="AES-256")

    out = io.BytesIO()
    writer.write(out)
    return out.getvalue()
