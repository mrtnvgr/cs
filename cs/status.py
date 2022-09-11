import os, json
from cs import logger

def get(path, string):
    if os.path.exists(path):
        status = json.load(open(path))
        if string!=None and string!=".":
            for elem in string.split("."):
                if elem!="":
                    status = status[elem]
        if type(status) is dict:
            status = json.dumps(status, indent=4)
        return status
    else:
        logger.error("Status file doesnt exist")
        exit(1)

def gen(cs_name, light, cs_path, wallpaper=False):
    status = {"source": {}, 
              "colorscheme": {"name": cs_name, 
                              "light": light}}
    
    if wallpaper:
        status["source"]["type"] = "wallpaper"
        status["source"]["path"] = os.path.abspath(cs_path)
    else:
        status["source"]["type"] = "colorscheme"
        status["source"]["path"] = cs_name 

    path = os.path.join(os.getenv("HOME"), ".cache",
                        "cs", "status.json")
    json.dump(status, open(path, "w"), indent=4)
