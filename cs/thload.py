from cs import colorscheme
from cs import wallpaper
from cs import status
from cs import logger
import json, os

def load(theme_name):
    theme_path = os.path.join(os.getenv("HOME"), ".config", "cs",
                              "themes", f"{theme_name}.json")
    if os.path.exists(theme_path):
        theme = json.load(open(theme_path))
        if theme["colorscheme"]["type"]=="wallpaper":
            scheme = colorscheme.Colorscheme(theme["wallpaper"], theme["colorscheme"]["light"])
            logger.info(f"Loading {theme_name} theme...")
            scheme.generate()
            scheme.currentScheme(name=False)
        else:
            scheme = colorscheme.Colorscheme(theme["colorscheme"]["name"], theme["colorscheme"]["light"])
            scheme.get()
            scheme.set()
            if "wallpaper" in theme:
                wallpaper.set(theme["wallpaper"])
            scheme.currentScheme()
    else:
        logger.error(f"{theme_name} does not exist")
        exit(1)
