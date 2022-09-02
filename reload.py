import subprocess, platform, shutil, os
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
    if shutil.which("qtile") and getpid("qtile"):
        cmd = ["pkill", "-SIGUSR1", "qtile"]
        if not shutil.which("pkill"):
            logger.warning("pkill not found??? trying killall...")
            cmd[0] = "killall"
        subprocess.run(cmd, check=False,
                       stderr=subprocess.DEVNULL)

def getpid(name):
    if not shutil.which("pidof"):
        return False
    try:
        if platform.system() != 'Darwin':
            subprocess.check_output(["pidof", "-s", name])
        else:
            subprocess.check_output(["pidof", name])
    except subprocess.CalledProcessError:
        return False
    return True
