"""Image concatenation utilities."""

import enum
import logging
from fractions import Fraction
from typing import TYPE_CHECKING

from PIL import Image

if TYPE_CHECKING:
    from pathlib import Path

    from PIL.Image import Image as PILImage

logger = logging.getLogger(__name__)


class Orient(enum.StrEnum):
    """Enumeration for image concatenation orientation."""

    HORIZONTAL = "horizontal"
    VERTICAL = "vertical"


str_to_orient: dict[str, Orient] = {
    "h": Orient.HORIZONTAL,
    "horizontal": Orient.HORIZONTAL,
    "v": Orient.VERTICAL,
    "vertical": Orient.VERTICAL,
}


def fit_resize(images: list[PILImage], orient: Orient) -> list[PILImage]:
    """Resize images to fit the minimal dimension based on orientation."""
    resized_images: list[PILImage] = []
    match orient:
        case Orient.HORIZONTAL:
            new_height: int = min(image.height for image in images)
            for image in images:
                ratio = Fraction(new_height, image.height)
                new_width = int(image.width * ratio)
                new_size = (new_width, new_height)
                resized_image = image.resize(new_size)  # type: ignore[call-arg]
                resized_images.append(resized_image)
        case Orient.VERTICAL:
            new_width: int = min(image.width for image in images)
            for image in images:
                ratio = Fraction(new_width, image.width)
                new_height = int(image.height * ratio)
                new_size = (new_width, new_height)
                resized_image = image.resize(new_size)  # type: ignore[call-arg]
                resized_images.append(resized_image)
    return resized_images


def concatenate(images: list[PILImage], orient: Orient) -> PILImage:
    """Concatenate images based on the specified orientation."""
    concatenated_size: tuple[int, int]
    match orient:
        case Orient.HORIZONTAL:
            new_width = sum(image.width for image in images)
            new_height = max(image.height for image in images)
            concatenated_size = (new_width, new_height)
        case Orient.VERTICAL:
            new_width = max(image.width for image in images)
            new_height = sum(image.height for image in images)
            concatenated_size = (new_width, new_height)
    logger.debug("[Concatenate] concatenated_size=%r", concatenated_size)
    concatenated_image = Image.new("RGB", concatenated_size)
    offset = 0
    for image in images:
        match orient:
            case Orient.HORIZONTAL:
                concatenated_image.paste(image, (offset, 0))
                offset += image.width
            case Orient.VERTICAL:
                concatenated_image.paste(image, (0, offset))
                offset += image.height
    return concatenated_image


def save_image(image: PILImage, path: Path) -> None:
    """Save the image to the specified path with the given format."""
    if path.exists():
        logger.warning(
            'Output file "%s" already exists and will be overwritten.', path
        )
    logger.info('Saving image to "%s"...', path)
    try:
        match path.suffix.lower():
            case ".png":
                image.save(
                    path,
                    format="PNG",
                    lossless=True,
                    compress_level=9,
                    optimize=True,
                )
            case ".jpg" | ".jpeg":
                image.save(
                    path,
                    format="JPEG",
                    quality=100,
                    subsampling=0,
                    optimize=True,
                    progressive=True,
                )
            case ".webp":
                image.save(
                    path,
                    format="WEBP",
                    lossless=True,
                    method=6,
                )
            case _:
                image.save(path)
    except (OSError, ValueError) as exception:
        message = f'Failed to save image to "{path}": "{exception}".'
        logger.fatal(message)
        raise
    logger.info('Image successfully saved to "%s".', path)
