"""
Utility functions and classes for the Virt341 system
"""

from io import BytesIO
from segno import make


def generate_qr_code(data):
    """
    Generates a QR code for the given data (URL or text) and returns it as a binary PNG image.
    """
    qr = make(data)
    img_io = BytesIO()
    qr.save(img_io, kind="png", scale=10)
    img_io.seek(0)

    return img_io


if __name__ == "__main__":
    with open("test.jpg", "wb") as img_file:
        # print(generate_qr_code("google.com").readlines())
        img_file.write(generate_qr_code("https://google.com").read())
