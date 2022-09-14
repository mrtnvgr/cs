import shutil, os
from cs import logger

def save(cache_path, name):
    status_path = os.path.join(cache_path, "status.json")
    if os.path.exists(status_path):
        theme_path = os.path.join(os.getenv("HOME"), ".config", "cs", "themes", name)
        
        if os.path.exists(theme_path):
            logger.warning(f"Theme {name} already exists")
            ch = logger.warning("Overwrite? (y/n): ", func=input).lower()
            if ch == "y":
                shutil.rmtree(theme_path)
            else:
                exit(1)
        shutil.copytree(cache_path, theme_path)
        
        logger.info(f"Current state saved as {name} to {theme_path}")
