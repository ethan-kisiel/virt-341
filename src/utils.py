"""
Utility functions and classes for the Virt341 system
"""

import segno
from io import BytesIO

def generate_qr_code(data):
    """
    Generates a QR code for the given data (URL or text) and returns it as a binary PNG image.
    """
    qr = segno.make(data)
    img_io = BytesIO()
    qr.save(img_io, kind='png', scale=10)
    img_io.seek(0)  

    return img_io
