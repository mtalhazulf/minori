import base64
from io import BytesIO
from typing import List, Tuple

from PIL import Image


def validate_base64_image(base64_image: str, **kwargs) -> Image:
    return validate_image(base64.b64decode(base64_image), **kwargs)


def validate_image(
    image: bytes,
    valid_formats: List[str] = None,
    min_size: Tuple[int, int] = None,
    max_size: Tuple[int, int] = None,
    max_bytes: int = None,
) -> Image:
    with BytesIO(image) as img_io:
        img = Image.open(img_io)
        width, height = img.size

        if valid_formats is not None and img.format not in valid_formats:
            raise ValueError(
                f"Formato dell'immagine non valido, fornire uno dei seguenti formati: {', '.join(valid_formats)}"
            )

        if min_size is not None:
            if min_size[0] > width or min_size[1] > height:
                raise ValueError(
                    f"L'imagine fornita è troppo piccola, fornire un immagine di almeno {min_size[0]}x{min_size[1]}"
                )

        if max_size is not None:
            if max_size[0] < width or min_size[1] < height:
                raise ValueError(
                    f"L'imagine fornita è troppo grande, fornire un immagine di almeno {min_size[0]}x{min_size[1]}"
                )

        if max_bytes and max_bytes < len(image):
            raise ValueError(f"L'imagine fornita è troppo pesante, dimensione massima {max_bytes}")

        return img
