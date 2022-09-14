import shutil, json, os
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
        
        # Load status
        theme_status_path = os.path.join(theme_path, "status.json")
        status = json.load(open(theme_status_path))
        
        # Copy wallpaper into theme directory
        wallpaper_name = os.path.basename(status["wallpaper"])
        theme_wallpaper_path = os.path.join(theme_path, wallpaper_name)
        shutil.copy2(status["wallpaper"], theme_wallpaper_path)
        
        # Change wallpaper value
        status["wallpaper"] = wallpaper_name

        # Change colorscheme name to theme name
        status["colorscheme"]["name"] = name
        
        # Save status
        json.dump(status, open(theme_status_path, "w"), indent=4)

        logger.info(f"Current state saved as {name} to {theme_path}")
