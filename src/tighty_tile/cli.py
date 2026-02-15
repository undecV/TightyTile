"""TightyTile - minimal-dimension image concatenation tool."""

import logging
from datetime import datetime
from pathlib import Path
from typing import TYPE_CHECKING

import click
from click_default_group import DefaultGroup
from PIL import Image
from rich.console import Console
from rich.logging import RichHandler

from .concatenate import (
    Orient,
    concatenate,
    fit_resize,
    save_image,
    str_to_orient,
)

if TYPE_CHECKING:
    from PIL.Image import Image as PILImage

logger = logging.getLogger(__name__)
rich_handler = RichHandler()
rich_handler.setFormatter(logging.Formatter("%(message)s"))
logging.getLogger().addHandler(rich_handler)

console = Console()
print = console.print  # noqa: A001


@click.group(cls=DefaultGroup, default="concat", default_if_no_args=True)
@click.option(
    "--verbose",
    "-v",
    count=True,
    default=1,
    help="Enable verbose output.",
)
def cli(verbose: int) -> None:
    """Command-line interface for TightyTile."""
    logging_level = logging.WARNING  # Default level
    match verbose:
        case 0:
            logging_level = logging.WARNING
        case 1:
            logging_level = logging.INFO
        case _:
            logging_level = logging.DEBUG

    logger.setLevel(logging_level)
    for handler in logging.getLogger().handlers:
        handler.setLevel(logging_level)

    logger.debug("[Arguments] verbose=%r", verbose)
    if verbose >= 5:  # noqa: PLR2004
        logger.debug("Logging module now has Super Cow Powers!")


@cli.command()
@click.argument(
    "image_paths",
    nargs=-1,
    type=click.Path(
        exists=True,
        file_okay=True,
        dir_okay=False,
        readable=True,
        path_type=Path,
    ),
)
@click.option(
    "-d",
    "--direction",
    type=click.Choice(str_to_orient.keys(), case_sensitive=False),
    default="horizontal",
    help="Direction to concatenate images.",
)
@click.option(
    "--output",
    "-o",
    type=click.Path(
        exists=False,
        file_okay=True,
        dir_okay=False,
        writable=True,
        path_type=Path,
    ),
    help="Output file path for the concatenated image.",
)
def concat(
    image_paths: list[Path],
    direction: str,
    output: Path | None,
) -> None:
    """Concatenate multiple images into a single image."""
    logger.debug("[Arguments] image_paths=%r", image_paths)
    logger.debug("[Arguments] direction=%r", direction)
    logger.debug("[Arguments] output=%r", output)

    if len(image_paths) < 2:  # noqa: PLR2004
        error_message = "At least two images are required for concatenation."
        logger.error(error_message)
        raise click.UsageError(error_message)

    # Processing arguments
    if direction.lower() not in str_to_orient:
        error_message = f"Unsupported direction: {direction}"
        logger.error(error_message)
        raise click.UsageError(error_message)

    orient: Orient = str_to_orient[direction.lower()]
    now_str = datetime.now().astimezone().strftime("%Y%m%dT%H%M%S")
    default_output_stem = "TightyTile_" + now_str
    default_output_name = f"{default_output_stem}.webp"
    default_output: Path = Path.cwd() / default_output_name

    logger.debug("[Processed] orient=%r", orient)
    logger.debug("[Processed] default_output=%r", default_output)

    output_path = (output if output is not None else default_output).resolve()
    logger.info('Output will be saved to: "%s"', output_path)

    images: list[PILImage] = []
    for image_path in image_paths:
        with Image.open(image_path) as image:
            images.append(image.copy())
            logger.debug(
                "[Loading] image=%r size=(%r, %r)",
                image.filename,
                image.width,
                image.height,
            )

    resized_images: list[PILImage] = fit_resize(images=images, orient=orient)
    concatenated_image: PILImage = concatenate(
        images=resized_images, orient=orient
    )
    try:
        save_image(
            image=concatenated_image,
            path=output_path,
        )
    except Exception as exception:
        message = f"{exception}"
        raise click.ClickException(message) from exception


if __name__ == "__main__":
    cli()
