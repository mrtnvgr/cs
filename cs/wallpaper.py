from cs import util
from cs import logger

import requests
import tempfile
import shutil
import os


def set(path):
    """Set wallpaper"""

    # If path is url, download file
    isurl = util.isUrl(path)
    if isurl:

        logger.info("Downloading wallpaper...")

        # Get content from url
        file = requests.get(path)

        # Check if file is image
        if "image" in file.headers["Content-Type"]:

            # Create temp file
            tp = tempfile.NamedTemporaryFile(prefix="cswp-")

            # Overwrite path to temp file path
            path = tp.file.name

            # Write content to temp file
            tp.seek(0)
            tp.write(file.content)

    # Check if path exists
    if os.path.exists(path):

        # Xorg wallpaper managers
        if os.environ.get("DISPLAY"):

            if shutil.which("feh"):

                util.run(["feh", "--bg-fill", path])
                current(path, isurl)
                return True

            else:
                logger.warning(f"Your wallpaper manager is not supported")

    else:

        logger.error("Wallpaper does not exist")


def current(path, isurl):
    """Print current wallpaper info"""
    name = os.path.basename(path)
    if not isurl:
        logger.info(f"Current wallpaper is {name}")
