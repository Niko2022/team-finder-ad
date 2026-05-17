from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
from django.core.files.base import ContentFile
import random


def generate_avatar(name: str):
    """Генерирует аватар с первой буквой имени на цветном фоне"""
    size = (200, 200)
    background_colors = [
        (66, 133, 244), (234, 67, 53), (251, 188, 5),
        (52, 168, 83), (156, 39, 176), (0, 188, 212)
    ]

    bg_color = random.choice(background_colors)
    image = Image.new('RGB', size, bg_color)
    draw = ImageDraw.Draw(image)

    initial = name[0].upper() if name else '?'

    try:
        font = ImageFont.truetype("arial.ttf", 100)
    except:
        try:
            font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 100)
        except:
            font = ImageFont.load_default()

    bbox = draw.textbbox((0, 0), initial, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    position = ((size[0] - text_width) // 2, (size[1] - text_height) // 2)

    draw.text(position, initial, fill='white', font=font)

    buffer = BytesIO()
    image.save(buffer, format='PNG')
    buffer.seek(0)

    return ContentFile(buffer.getvalue(), name=f'avatar_{name}.png')
