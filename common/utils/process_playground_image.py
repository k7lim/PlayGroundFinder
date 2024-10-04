import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

from common.utils.instructor_utils import identify_object_from_image
from common.schemas import PlaygroundImage
from common.utils.image_utils import process_image

def process_playground_image(image_input: str) -> tuple[str, PlaygroundImage]:
    """
    Given an image input (URL, base64 string, or file path), identify a PlaygroundImage object in the image
    """
    # Process the image and get the base64 encoded string and MIME type
    image_data, image_format, processed_file_path = process_image(image_input)
    
    logger.debug(f"Processed file path: {processed_file_path}")

    # Identify the playground image from the image
    playground_image = identify_object_from_image(image_data, PlaygroundImage, image_format)
    
    logger.debug(f"Identified playground image: {playground_image}")
    
    return processed_file_path, playground_image

def main(image_str: str):
    # Convert the processed image to an outfit
    processed_file_path, salepage = process_playground_image(image_str)

    # Render the result page with the processed image path
    print(processed_file_path)
    print(str(salepage))

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Usage: python image_to_playground.py <image_url>")
        sys.exit(1)
    image_url = sys.argv[1]
    main(image_url)
