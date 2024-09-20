"""
Utility functions and classes for the Virt341 system
"""

import segno
from io import BytesIO

def generate_qr_code(data):
    """
    Generates a QR code for the given data (URL or text) and returns it as a binary PNG image.
    """
    # Generate QR code
    qr = segno.make(data)
    
    # Save the QR code to a BytesIO object in PNG format
    img_io = BytesIO()
    qr.save(img_io, kind='png')
    img_io.seek(0)  # Rewind the file pointer to the beginning
    
    return img_io
