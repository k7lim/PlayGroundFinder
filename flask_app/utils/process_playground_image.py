from .instructor_utils import identify_object_from_image
from models import PlaygroundImageOrm
from .image_utils import process_image

def process_playground_image(image_input: str) -> PlaygroundImageOrm:
    """
    Given an image input (URL, base64 string, or file path), identify a Outfit object in the image
    """
    # Process the image and get the base64 encoded string and MIME type
    image_data, image_format, processed_file_path = process_image(image_input)

    # Identify the outfit from the image
    outfit = identify_object_from_image(image_data, PlaygroundImageOrm, image_format)
    return processed_file_path, outfit

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
