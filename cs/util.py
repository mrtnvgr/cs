import subprocess, requests, os

# Generate paths dict
paths = {}
paths["me"] = os.path.dirname(os.path.realpath(__file__))
paths["home"] = os.getenv("HOME")
paths["config"] = os.path.join(paths["home"], ".config", "cs")
paths["cache"] = os.path.join(paths["home"], ".cache", "cs")
paths["colorschemes"] = (
    os.path.join(paths["config"], "colorschemes"),
    os.path.join(paths["me"], "colorschemes"),
)
paths["themes"] = os.path.join(paths["config"], "themes")


def run(cmd):
    return subprocess.run(cmd, check=False, stderr=subprocess.DEVNULL)


def check_output(cmd):
    return subprocess.check_output(cmd, stderr=subprocess.DEVNULL)


def disown(cmd):
    return subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


def pidof(name):
    try:
        subprocess.check_output(["pidof", "-s", "-x", name])
    except subprocess.CalledProcessError:
        return False
    return True


def setupPaths():
    """Create path dirs if they dont exist"""
    for folder in list(paths.values()):
        if type(folder) == str:
            os.makedirs(folder, exist_ok=True)
        else:
            for fol in folder:
                os.makedirs(fol, exist_ok=True)
    return paths


def beautify(text):
    """Beautify text"""
    text = text.removesuffix(".json")
    if "_" in text:
        text = text.replace("_", " ")
    else:
        if "-" in text:
            text = text.replace("_", " ")

    if len(text) > 2:
        text = text.title()

    return text


def isUrl(text):
    """Check if text is url"""
    return True if "http" in text and "://" in text else False


def downloadUrl(url, path):
    """Download url"""
    content = requests.get(url).content
    open(path, "wb").write(content)
