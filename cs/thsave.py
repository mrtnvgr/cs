import shutil, imghdr, json, os
from cs import logger
from cs import util


def save(name):
    """Save current state to theme"""

    status_path = os.path.join(util.paths["cache"], "status.json")
    # If status exists
    if os.path.exists(status_path):
        theme_path = os.path.join(util.paths["themes"], name)

        # Ask user to overwrite if theme already exists
        if os.path.exists(theme_path):
            logger.warning(f"Theme {name} already exists")
            ch = logger.warning("Overwrite? (y/n): ", func=input).lower()

            if ch != "y":
                exit(1)

        # Load status
        status = json.load(open(status_path))

        # Make theme directory
        os.makedirs(theme_path, exist_ok=True)

        # Copying files
        cache_files = os.listdir(util.paths["cache"])
        for file in cache_files:
            path = os.path.join(util.paths["cache"], file)
            if imghdr.what(path) != None:  # if file is image
                if file != status["wallpaper"]:  # if file is not theme wallpaper
                    if file != os.path.basename(status["wallpaper"]):
                        os.remove(path)  # cleaning old file
                        continue
            shutil.copy2(path, os.path.join(theme_path, file))

        theme_status_path = os.path.join(theme_path, "status.json")

        # Copy wallpaper into theme directory
        wallpaper_name = os.path.basename(status["wallpaper"])
        theme_wallpaper_path = os.path.join(theme_path, wallpaper_name)

        # Check that the files are not the same
        if status["wallpaper"] != theme_wallpaper_path:

            # Check if file is url
            if util.isUrl(status["wallpaper"]):

                cached_wallpaper = os.path.join(
                    util.paths["cache"], os.path.basename(status["wallpaper"])
                )
                print(cached_wallpaper)
                if not os.path.exists(cached_wallpaper):

                    logger.info("Downloading wallpaper...")

                    # Download file
                    util.downloadUrl(status["wallpaper"], theme_wallpaper_path)

            else:

                # Copy wallpaper to theme folder
                shutil.copy2(status["wallpaper"], theme_wallpaper_path)

        # Change wallpaper value
        status["wallpaper"] = wallpaper_name

        # Change colorscheme name to theme name
        status["colorscheme"]["name"] = name

        # Save status
        json.dump(status, open(theme_status_path, "w"), indent=4)

        logger.info(f"Current state saved as {name} to {theme_path}")
