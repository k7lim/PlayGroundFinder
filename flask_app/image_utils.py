import base64
import logging
import requests
from io import BytesIO
from PIL import Image, UnidentifiedImageError
import os
import time
from requests.exceptions import SSLError, RequestException, HTTPError

# Add logger
logging.basicConfig()
logger = logging.getLogger("app")
logger.setLevel("INFO")



def process_image(image_input: str, max_retries=3, retry_delay=1, output_dir="uploads"):
    """
    Process an image from either a URL, a base64-encoded string, or a file path.

    Args:
        image_input (str): Either a URL, a base64-encoded string, or a file path of the image.
        max_retries (int): Maximum number of retries for URL fetching.
        retry_delay (int): Delay in seconds between retries.
        output_dir (str): Directory to save the processed image.

    Returns:
        tuple: A tuple containing:
            - str: The base64-encoded string of the image.
            - str: The MIME type of the processed image.
            - str: The file path of the processed image.

    Raises:
        requests.exceptions.RequestException: If there's an error fetching the image from URL.
        ValueError: If the input is neither a valid URL, base64 string, nor a valid file path.
    """

    # Save the image to the uploads directory
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    processed_file_path = None

    if image_input.startswith(('http://', 'https://')):
        # It's a URL, fetch and process
        image = fetch_image_from_url(image_input, max_retries, retry_delay)
    elif ',' in image_input and 'base64' in image_input:
        # It's a base64-encoded string
        image = decode_base64_image(image_input)
    else:
        # Assume it's a file path
        image = open_image_file(image_input)
        processed_file_path = image_input

    image_format = image.format.lower() if image.format else "png"

    # Resize the image if necessary
    resized_image = resize_image_if_needed(image)

    if processed_file_path is None or resized_image != image:
        # Save the processed image to a file
        os.makedirs(output_dir, exist_ok=True)
        processed_file_path = os.path.join(output_dir, f"processed_{int(time.time())}.{image_format}")
        resized_image.save(processed_file_path, format=image_format)
        image = resized_image

    buffered = BytesIO()
    image.save(buffered, format=image_format)
    img_str = base64.b64encode(buffered.getvalue()).decode()

    mime_type = {
        "jpeg": "image/jpeg",
        "png": "image/png",
        "gif": "image/gif",
        "webp": "image/webp"
    }.get(image_format, "image/png")

    return img_str, mime_type, processed_file_path
def fetch_image_from_url(url: str, max_retries: int, retry_delay: int) -> Image.Image:
    for attempt in range(max_retries):
        try:
            response = requests.get(url, timeout=30)
            response.raise_for_status()
            return Image.open(BytesIO(response.content))
        except (SSLError, RequestException, HTTPError) as e:
            if attempt == max_retries - 1:
                logger.error(f"Failed to download image after {max_retries} attempts: {str(e)}")
                raise
            logger.warning(f"Attempt {attempt + 1} failed, retrying in {retry_delay} seconds...")
            time.sleep(retry_delay)
            retry_delay *= 2  # Exponential backoff
    raise ValueError("Failed to fetch image from URL")

def decode_base64_image(base64_string: str) -> Image.Image:
    try:
        image_data = base64.b64decode(base64_string.split(',')[1])
        return Image.open(BytesIO(image_data))
    except:
        raise ValueError("Invalid input: not a valid base64 string")

def open_image_file(file_path: str) -> Image.Image:
    try:
        with open(file_path, "rb") as f:
            image_data = f.read()
        return Image.open(BytesIO(image_data))
    except FileNotFoundError:
        raise ValueError("Invalid input: file not found")
    except UnidentifiedImageError:
        raise ValueError("Invalid input: cannot identify image file")

def resize_image_if_needed(image: Image.Image) -> Image.Image:
    width, height = image.size
    max_size = 1568
    max_pixels = 1150000  # 1.15 megapixels

    if max(width, height) > max_size or (width * height) > max_pixels:
        if width > height:
            new_width = max_size
            new_height = int(height * (max_size / width))
        else:
            new_height = max_size
            new_width = int(width * (max_size / height))

        return image.resize((new_width, new_height), Image.Resampling.LANCZOS)
    return image

def image_to_base64(image: Image.Image) -> tuple[str, str]:
    buffered = BytesIO()
    image_format = image.format.lower() if image.format else "png"
    image.save(buffered, format=image_format)
    img_str = base64.b64encode(buffered.getvalue()).decode()

    mime_type = {
        "jpeg": "image/jpeg",
        "png": "image/png",
        "gif": "image/gif",
        "webp": "image/webp"
    }.get(image_format, "image/png")

    return img_str, mime_type
