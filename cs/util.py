import subprocess, os

def run(cmd):
    return subprocess.run(cmd,
                          check=False,
                          stderr=subprocess.DEVNULL)

def check_output(cmd):
    return subprocess.check_output(cmd,
                                   stderr=subprocess.DEVNULL)

def disown(cmd):
    return subprocess.Popen(cmd,
                            stdout=subprocess.DEVNULL,
                            stderr=subprocess.DEVNULL)

def pidof(name):
    try:
        subprocess.check_output(["pidof", "-s", "-x", name])
    except subprocess.CalledProcessError:
        return False
    return True

def getPaths():
    paths = {}
    paths["me"] = os.path.dirname(os.path.realpath(__file__))
    paths["home"] = os.getenv("HOME")
    paths["config"] = os.path.join(paths["home"], ".config", "cs")
    paths["cache"] = os.path.join(paths["home"], ".cache", "cs")
    paths["colorschemes"] = (os.path.join(paths["config"], "colorschemes"),
                             os.path.join(paths["me"], "colorschemes"))
    for folder in list(paths.values()):
        if type(folder)==str:
            os.makedirs(folder, exist_ok=True)
        else:
            for fol in folder:
                os.makedirs(fol, exist_ok=True)
    return paths
