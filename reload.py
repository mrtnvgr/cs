import subprocess, shutil, os
import logger

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
    path = os.path.join(os.getenv("HOME"), ".cache",
                        "cs", "colors.Xresources")
    if shutil.which("xrdb"):
        rc = subprocess.run(["xrdb", "-merge", "-quiet", path],
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
    pass
