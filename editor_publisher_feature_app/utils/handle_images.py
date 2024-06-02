import re
import base64
import uuid
import os
import logging
from django.conf import settings

logger = logging.getLogger(__name__)

def handle_images(content):
    """
    Handles embedded images in base64 format within the content.

    This function decodes base64 images, saves them as files, and replaces
    the base64 data URLs with absolute URLs to the saved images.

    Args:
        content (str): Blog content in HTML format.

    Returns:
        str: Content with embedded images replaced by absolute URLs.
    """
    img_pattern = re.compile(r'<img src="data:image/(png|jpeg|jpg);base64,([^"]+)"')
    matches = img_pattern.findall(content)
    
    if not matches:
        return content

    for img_format, img_str in matches:
        full_img_url = save_base64_image(img_str, img_format)
        if full_img_url:
            content = content.replace(f'data:image/{img_format};base64,{img_str}', full_img_url)

    return content

def save_base64_image(img_str, img_format):
    """
    Saves a base64 encoded image to disk and returns its absolute URL.

    Args:
        img_str (str): Base64 encoded image string.
        img_format (str): Image format (e.g., png, jpeg, jpg).

    Returns:
        str: Absolute URL to the saved image, or None if saving fails.
    """
    try:
        img_data = base64.b64decode(img_str)
        img_name = f'{uuid.uuid4()}.{img_format}'
        img_path = os.path.join(settings.MEDIA_ROOT, 'blog_images', img_name)
        
        os.makedirs(os.path.dirname(img_path), exist_ok=True)
        
        with open(img_path, 'wb') as img_file:
            img_file.write(img_data)
        
        img_url = f'{settings.MEDIA_URL}blog_images/{img_name}'
        full_img_url = f'{settings.SITE_URL}{img_url}'
        return full_img_url
    except Exception as e:
        logger.error(f"Error processing image: {e}")
        return None
