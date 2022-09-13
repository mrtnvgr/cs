import json, os
from cs import logger

def load(theme_name):
    theme_path = os.path.join(os.getenv("HOME"), ".config", "cs",
                              "themes", f"{theme_name}.json")
    if os.path.exists(theme_path):
        theme = json.load(open(theme_path))
        if theme["source"]["type"]=="wallpaper":
            print(theme)
    else:
        logger.error(f"{theme_name} does not exist")
        exit(1)
