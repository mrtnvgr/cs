import os, json
import logger

def get(path, string):
    if os.path.exists(path):
        status = json.load(open(path))
        if string!=None and string!=".":
            for elem in string.split("."):
                if elem!="":
                    status = status[elem]
        return status
    else:
        logger.error("Status file doesnt exist")
        exit(1)
