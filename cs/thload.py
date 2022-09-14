from cs import wallpaper
from cs import reload
from cs import logger
import shutil, json, os

def load(theme_name):
    theme_path = os.path.join(os.getenv("HOME"), ".config", "cs",
                              "themes", theme_name)
    cache_path = os.path.join(os.getenv("HOME"), ".cache", "cs")
    if os.path.exists(theme_path):
        logger.info(f"Loading {theme_name} theme...")
        theme_status_path = os.path.join(theme_path, "status.json")
        theme = json.load(open(theme_status_path))
        
        logger.info("Copying templates...")
        if os.path.exists(cache_path):
            shutil.rmtree(cache_path)
        shutil.copytree(theme_path, cache_path)

        reload.reload_all()
        
        if "wallpaper" in theme:
            wallpaper.set(theme["wallpaper"])

    else:
        logger.error(f"{theme_name} does not exist")
        exit(1)
