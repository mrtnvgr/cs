from cs import wallpaper
from cs import reload
from cs import logger
from cs import util
import shutil, json, os

def load(theme_name):
    """ Load theme """
    theme_path = os.path.join(util.paths["themes"], theme_name)
    # Check if theme exists
    if os.path.exists(theme_path):
        
        logger.info(f"Loading {theme_name} theme...")

        # Loading theme status file
        theme_status_path = os.path.join(theme_path, "status.json")
        theme = json.load(open(theme_status_path))
        
        logger.info("Copying cache folder...")
        
        # Erase old cache folder if exists
        if os.path.exists(util.paths["cache"]):
            shutil.rmtree(util.paths["cache"])

        # Copy theme folder to cache
        shutil.copytree(theme_path, util.paths["cache"])
    
        # Reload all templates
        reload.reload_all()
        
        # Check if wallpaper in theme
        if "wallpaper" in theme:

            # Overwrite path with absolute one
            theme["wallpaper"] = os.path.join(theme_path, theme["wallpaper"])

            # Save status file
            status_path = os.path.join(util.paths["cache"], "status.json")
            json.dump(theme, open(status_path, "w"), indent=4)
            
            # Set wallpaper
            wallpaper.set(theme["wallpaper"])

    else:
        logger.error(f"{theme_name} does not exist")
        exit(1)
