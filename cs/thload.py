from cs import wallpaper
from cs import reload
from cs import logger
from cs import util
import shutil, json, os

def load(theme_name):
    theme_path = os.path.join(util.paths["themes"], theme_name)
    if os.path.exists(theme_path):
        logger.info(f"Loading {theme_name} theme...")
        theme_status_path = os.path.join(theme_path, "status.json")
        theme = json.load(open(theme_status_path))
        
        logger.info("Copying templates...")
        if os.path.exists(util.paths["cache"]):
            shutil.rmtree(util.paths["cache"])
        shutil.copytree(theme_path, util.paths["cache"])

        reload.reload_all()
        
        if "wallpaper" in theme:
            wallpaper.set(os.path.join(theme_path, theme["wallpaper"]))

    else:
        logger.error(f"{theme_name} does not exist")
        exit(1)
