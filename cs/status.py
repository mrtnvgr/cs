import os, json
from cs import logger
from cs import util

def get(path, string):
    # If status path exists
    if os.path.exists(path):

        # Load status
        status = json.load(open(path))

        # If string is not empty
        if string!=None and string!=".":

            # Iterate through string keys
            for elem in string.split("."):

                # If key isn't Empty
                if elem!="":

                    # Check if key in status
                    if elem in status:

                        # Overwrite status with key
                        status = status[elem]

                    else:
                        logger.error(f"Status does not contain '{elem}' key")
                        exit(1)

        # Indent output if status is dict
        if type(status) is dict:
            status = json.dumps(status, indent=4)
        
        return status

    else:
        logger.error("Status file doesnt exist")
        exit(1)

def gen(cs_name, light, cs_path, wallpaper=False):
    # Set status path
    path = os.path.join(util.paths["cache"], "status.json")

    # Status default dict
    status = {"colorscheme": {"name": cs_name,
                              "light": light,
                              "path": cs_path}}

    # Get wallpaper value from old status
    if os.path.exists(path):
        old_status = json.load(open(path))
        if "wallpaper" in old_status: 
            status["wallpaper"] = old_status["wallpaper"]
    
    if wallpaper:
        status["wallpaper"] = status["colorscheme"]["path"]
        status["colorscheme"]["type"] = "wallpaper"
        name = os.path.basename(status["colorscheme"]["path"])
        if "." in name:
            name = ''.join(name.split(".")[:-1])
        status["colorscheme"]["name"] = name
    else:
        status["colorscheme"]["type"] = "colorscheme"
        status["colorscheme"]["name"] = cs_name

    json.dump(status, open(path, "w"), indent=4)
