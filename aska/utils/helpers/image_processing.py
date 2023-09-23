import os
import uuid
from PIL import Image, ImageDraw, ImageFont, ImageColor


def create_text_image(
    text, width, height, text_color="black", background_color=None, filename=None
):
    """
    Creates an image with the given text in the center using a bold font.

    Parameters:
        - text (str): The text to be displayed in the image.
        - width (int): The width of the image in pixels.
        - height (int): The height of the image in pixels.
        - text_color (str or tuple): The color of the text as a string ("black", "white", etc.)
                                      or a tuple of RGB values (e.g. (255, 0, 0) for red).
                                      Default is "black".
        - background_color (str or tuple): The background color of the image as a string ("black", "white", etc.)
                                            or a tuple of RGBA values (e.g. (255, 255, 255, 127) for semi-transparent white).
                                            Default is None, which means transparent.

    Returns:
        str: The path of the saved image file.
    """
    if background_color is None:
        # Create a new image with a transparent background
        image = Image.new("RGBA", (width, height), color=(0, 0, 0, 0))
    else:
        # Create a new image with the specified background color
        image = Image.new("RGBA", (width, height), color=background_color)

    # Draw the text in the center of the image using a bold font
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype("arialbd.ttf", size=min(width, height) // 2)
    left, top, right, bottom = draw.textbbox((0, 0), text, font=font)
    x = (width - right) // 2
    y = (height - bottom) // 2
    if isinstance(text_color, str):
        # Convert color name to RGB value
        text_color = ImageColor.getrgb(text_color)
    draw.text((x, y), text, fill=text_color, font=font)

    # Save the image to a file
    if filename:
        filename = filename + ".png"
    else:
        filename = f"{str(uuid.uuid4())}.png"

    image.save(filename)

    # Return the path of the saved file
    return os.path.abspath(filename)
