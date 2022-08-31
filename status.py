import json

def get(path, string):
    status = json.load(open(path))
    if string!=None and string!=".":
        for elem in string.split("."):
            if elem!="":
                status = status[elem]
    return status

