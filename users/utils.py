from io import BytesIO
import random

from PIL import Image, ImageDraw, ImageFont
from django.core.files.base import ContentFile

AVATAR_SIZE = (200, 200)
FONT_SIZE = 100

COLOR_BLUE = (66, 133, 244)
COLOR_RED = (234, 67, 53)
COLOR_YELLOW = (251, 188, 5)
COLOR_GREEN = (52, 168, 83)
COLOR_PURPLE = (156, 39, 176)
COLOR_CYAN = (0, 188, 212)

BACKGROUND_COLORS = [
    COLOR_BLUE,
    COLOR_RED,
    COLOR_YELLOW,
    COLOR_GREEN,
    COLOR_PURPLE,
    COLOR_CYAN,
]


def generate_avatar(name: str):
    """Генерирует аватар с первой буквой имени на цветном фоне"""

    bg_color = random.choice(BACKGROUND_COLORS)
    image = Image.new("RGB", AVATAR_SIZE, bg_color)
    draw = ImageDraw.Draw(image)

    initial = name[0].upper() if name else "?"

    try:
        font = ImageFont.truetype("arial.ttf", FONT_SIZE)
    except IOError:
        try:
            font = ImageFont.truetype(
                "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", FONT_SIZE
            )
        except IOError:
            font = ImageFont.load_default()

    bbox = draw.textbbox((0, 0), initial, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    position = ((AVATAR_SIZE[0] - text_width) // 2, (AVATAR_SIZE[1] - text_height) // 2)

    draw.text(position, initial, fill="white", font=font)

    buffer = BytesIO()
    image.save(buffer, format="PNG")
    buffer.seek(0)

    return ContentFile(buffer.getvalue(), name=f"avatar_{name}.png")
