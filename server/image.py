from PIL import Image
from pathlib import Path
import base64
from io import BytesIO

def image_to_base64_uri(image_path):
    # Open an image file
    with Image.open(image_path) as image:
        # Convert image to bytes
        buffered = BytesIO()
        image.save(buffered, format=image.format)
        image_bytes = buffered.getvalue()

        # Encode bytes to base64
        image_base64 = base64.b64encode(image_bytes).decode('utf-8')

        return image_base64

