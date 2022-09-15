import shutil, os
from cs import sequences
from cs import util
from cs import logger
import yaml

def reload_all():
    logger.info("Reloading colors...")
    reload_termux()
    reload_xrdb()
    reload_tty()
    sequences.send()
    reload_qtile()
    reload_qutebrowser()

def reload_termux():
    termux_path = os.path.join(util.paths["home"], ".termux")
    if os.path.exists(termux_path):
        colors_path = os.path.join(util.paths["cache"], "colors.termux")
        shutil.copy2(colors_path, os.path.join(termux_path, "colors.properties"))
        util.run(["termux-reload-settings"])

def reload_xrdb():
    generated = os.path.join(util.paths["cache"], "colors.Xresources")
    user = os.path.join(util.paths["home"], ".Xresources")
    files = [generated, user]

    if os.environ.get("DISPLAY"): # check if Xorg is running
        if shutil.which("xrdb"):
            for file in files:
                if os.path.exists(file):
                    util.run(["xrdb", "-merge", "-quiet", file])

def reload_tty():
    path = os.path.join(util.paths["cache"], "colors-tty.sh")
    term = os.getenv("TERM")
    if term=="linux":
        util.run(["sh", path])

def reload_qtile():
    if shutil.which("qtile"):
        cmd = ["pkill", "-SIGUSR1", "qtile"]
        if not shutil.which("pkill"):
            logger.warning("pkill not found??? trying killall...")
            cmd[0] = "killall"
        util.run(cmd)

def reload_qutebrowser():
    if shutil.which("qutebrowser"):
        template_path = os.path.join(util.paths["cache"], "colors-qutebrowser.yml")
        qutebrowser_path = os.path.join(util.paths["home"], ".config", "qutebrowser", "autoconfig.yml")

        if os.path.exists(template_path) and os.path.exists(qutebrowser_path):
            colors = yaml.safe_load(open(template_path))
            autoconfig = yaml.safe_load(open(qutebrowser_path))
            for color in colors:
                autoconfig["settings"][color] = {"global": colors[color]}
            yaml.safe_dump(autoconfig, open(qutebrowser_path, "w"))

            if util.pidof("qutebrowser"):
                util.disown(["qutebrowser", ":config-source"])
