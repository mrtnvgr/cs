import shutil, os
from cs import util
from cs import logger

def set(path):
    if os.path.exists(path):
        if shutil.which("feh"):
            util.run(["feh", "--bg-fill", path])
        else:
            logger.warning(f"feh is not installed")
