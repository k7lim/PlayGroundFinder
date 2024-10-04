import os
import anthropic
import instructor
from dotenv import find_dotenv, load_dotenv
from pydantic import BaseModel
from typing import Type, TypeVar

from .image_utils import logger, process_image
load_dotenv(find_dotenv())

# Define client
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")

if not ANTHROPIC_API_KEY:
    logger.warning("ANTHROPIC_API_KEY environment variable not set. Some features may not work.")
    client = None
else:
    client = instructor.from_anthropic(anthropic.Anthropic(api_key=ANTHROPIC_API_KEY))

T = TypeVar('T', bound=BaseModel)

def identify_object_from_image(image_data: str, object_type: Type[T], image_format: str) -> T:
    """
    Given an image base64 string, identify an object of the specified type in the image
    """

    logger.info(f"Identifying {object_type.__name__} in image")

    try:
        result = client.chat.completions.create(
                model="claude-3-5-sonnet-20240620",
                max_tokens=1024,
                max_retries=3,
                messages=[
                    {
                        "role": "user",
                        "content": [
                        {
                            "type": "text",
                            "text": f"""Identify a {object_type.__name__} using the given image.""",
                        },
                        {"type": "image",
                            "source": {
                                "type": "base64",
                                "media_type": image_format,
                                "data": image_data,
                        },}
                        ],
                    }
                ],
                response_model=object_type,
        )
        return result
    except Exception as e:
        logger.error(f"Error in identify_object_from_image: {str(e)}")
        raise
