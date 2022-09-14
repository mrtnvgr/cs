import shutil, imghdr, json, os
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

        # Load status
        status = json.load(open(os.path.join(cache_path, "status.json")))
        
        # Make theme directory
        os.makedirs(theme_path)

        # Copying files
        cache_files = os.listdir(cache_path)
        for file in cache_files:
            path = os.path.join(cache_path, file)
            if imghdr.what(path)!=None: # if file is image
                if file!=status["wallpaper"]: # if file is not theme wallpaper
                    os.remove(path) # cleaning old file
                    continue
            shutil.copy2(path, os.path.join(theme_path, file))
        
        theme_status_path = os.path.join(theme_path, "status.json")
        
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
