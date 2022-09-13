import shutil, os
from cs import logger

def save(status_path, name):
    if os.path.exists(status_path):
        themes_path = os.path.join(os.getenv("HOME"), ".config", "cs", "themes")
        os.makedirs(themes_path, exist_ok=True)
        theme_path = os.path.join(themes_path, f"{name}.json")
        shutil.copy2(status_path, theme_path)
        logger.info(f"Current status saved as {name} to {theme_path}")
