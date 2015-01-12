JPEG = 1
PNG = 2
GIF = 3

FORMATS = {
    JPEG: "JPEG",
    PNG: "PNG",
    GIF: "GIF",
}
FORMAT_CHOICES = [(x, FORMATS[x]) for x in FORMATS]

DEFAULT_FORMAT = JPEG
DEFAULT_JPEG_QUALITY = 88

def get_format(id):
    return FORMATS.get(id) or DEFAULT_FORMAT
