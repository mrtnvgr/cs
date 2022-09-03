import subprocess, shutil, os
from cs import logger

def reload_all():
    logger.info("Reloading colors...")
    reload_termux()
    reload_xrdb()
    reload_tty()
    reload_qtile()

def reload_termux():
    path = os.path.join(os.getenv("HOME"), ".termux")
    if os.path.exists(path):
        subprocess.run(["termux-reload-settings"])

def reload_xrdb():
    generated = os.path.join(os.getenv("HOME"), ".cache",
                             "cs", "colors.Xresources")
    files = [generated]
    user = os.path.join(os.getenv("HOME"), ".Xresources")
    if os.path.exists(user):
        files.append(user)
    if shutil.which("xrdb"):
        for file in files:
            rc = subprocess.run(["xrdb", "-merge", "-quiet", file],
                                 check=False,
                                 stderr=subprocess.DEVNULL).returncode
        if rc==1:
            logger.warning("Xresources failed")

def reload_tty():
    path = os.path.join(os.getenv("HOME"), ".cache",
                        "cs", "colors.sh")
    term = os.getenv("TERM")
    if term=="linux":
        subprocess.run(["sh", path])

def reload_qtile():
    if shutil.which("qtile"):
        cmd = ["pkill", "-SIGUSR1", "qtile"]
        if not shutil.which("pkill"):
            logger.warning("pkill not found??? trying killall...")
            cmd[0] = "killall"
        subprocess.run(cmd, check=False,
                       stderr=subprocess.DEVNULL)
