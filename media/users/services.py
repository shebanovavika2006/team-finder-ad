import random
from io import BytesIO

from django.core.files.base import ContentFile
from PIL import Image, ImageDraw


def generate_default_avatar(user) -> None:
    r, g, b = (random.randint(50, 200) for _ in range(3))
    image = Image.new("RGB", (200, 200), color=(r, g, b))
    draw = ImageDraw.Draw(image)

    first_char = user.first_name[0] if user.first_name else user.email[0]
    letter = first_char.upper()

    draw.text((90, 90), letter, fill=(255, 255, 255))

    buffer = BytesIO()
    image.save(buffer, format="PNG")
    
    filename = f"avatar_{user.id}_{user.email}.png"
    user.avatar.save(filename, ContentFile(buffer.getvalue()), save=True)
