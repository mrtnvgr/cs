import subprocess, shutil, os
import logger

def update_all():
    logger.info("Updating colors...")
    update_termux()
    update_xrdb()
    update_tty()

def update_termux():
    path = os.path.join(os.getenv("HOME"), ".termux")
    if os.path.exists(path):
        subprocess.run(["termux-reload-settings"])


def update_xrdb():
    path = os.path.join(os.getenv("HOME"), ".cache",
                        "cs", "colors.Xresources")
    if shutil.which("xrdb"):
        rc = subprocess.run(["xrdb", "-merge", "-quiet", path],
                             check=False,
                             stderr=subprocess.DEVNULL).returncode
        if rc==1:
            logger.warning("Xresources failed")

def update_tty():
    path = os.path.join(os.getenv("HOME"), ".cache",
                        "cs", "colors.sh")
    term = os.getenv("TERM")
    if term=="linux":
        subprocess.run(["sh", path])
