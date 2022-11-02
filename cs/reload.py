import shutil, os
from cs import sequences
from cs import util
from cs import logger
import yaml


def reload_all():
    """Reload all"""
    logger.info("Reloading colors...")

    # Reload functions
    reload_termux()
    reload_xrdb()
    reload_tty()
    sequences.send()
    reload_st()
    reload_qtile()
    reload_qutebrowser()


def reload_termux():
    """Reload termux colors"""

    # Get termux config path
    termux_path = os.path.join(util.paths["home"], ".termux")

    # Check if path exists
    if os.path.exists(termux_path):

        # Get termux template path
        colors_path = os.path.join(util.paths["cache"], "colors.termux")

        # Copy template into termux folder
        shutil.copy2(colors_path, os.path.join(termux_path, "colors.properties"))

        # Run termux reload settings cmd
        util.run(["termux-reload-settings"])


def reload_xrdb():
    """Merge user and cs xresources files"""

    # Get xresources template path
    generated = os.path.join(util.paths["cache"], "colors.Xresources")

    # Get user xresources home file path
    user = os.path.join(util.paths["home"], ".Xresources")

    # Set files to list
    files = [generated, user]

    # Check if Xorg is running
    if os.environ.get("DISPLAY"):

        # Check if xrdb command is available
        if shutil.which("xrdb"):

            # Iterate through files
            for file in files:

                # Check if file exists
                if os.path.exists(file):

                    # Merge file to xrdb db
                    util.run(["xrdb", "-merge", "-quiet", file])


def reload_tty():
    """Reload tty colors"""

    # Get tty template path
    path = os.path.join(util.paths["cache"], "colors-tty.sh")

    # Get term system variable
    term = os.getenv("TERM")

    # Check if current terminal is tty (linux)
    if term == "linux":

        # Check if path exists
        if os.path.exists(path):

            # Execute tty template
            util.run(["sh", path])

def reload_st():
    """Reload st colors"""
    # NOTE: xresources-with-reload-signal patch required

    # Check if st is installed
    if shutil.which("st"):

        # Check if st is running
        if util.pidof("st"):
                
            # Send USER1 signal (xresources reload request) to st processes
            util.sigsend("st", "SIGUSR1")

def reload_qtile():
    """Reload qtile colors"""

    # Check if qtile is installed
    if shutil.which("qtile"):

        # Check if qtile is running
        if util.pidof("qtile"):

            # Send USER1 signal (config reload request) to qtile processes
            util.sigsend("qtile", "SIGUSR1")


def reload_qutebrowser():
    """Reload qutebrowser colors"""

    # Check if qutebrowser is installed
    if shutil.which("qutebrowser"):

        # Get qutebrowser template path
        template_path = os.path.join(util.paths["cache"], "colors-qutebrowser.yml")

        # Get qutebrowser autoconfig path
        qutebrowser_path = os.path.join(
            util.paths["home"], ".config", "qutebrowser", "autoconfig.yml"
        )

        # Check if template and autoconfig exists
        if os.path.exists(template_path):

            # Load colors from template
            colors = yaml.safe_load(open(template_path))

            # Load autoconfig settings
            if os.path.exists(qutebrowser_path):
                autoconfig = yaml.safe_load(open(qutebrowser_path))
            else:
                autoconfig = {}

            # Iterate through template colora
            for color in colors:

                # Merge template color setting to autoconfig as global value
                autoconfig["settings"][color] = {"global": colors[color]}

            # Save merged autoconfig settings
            yaml.safe_dump(autoconfig, open(qutebrowser_path, "w"))

            # Check if qutebrowser is running
            if util.pidof("qutebrowser"):

                # Run config reload cmd in background
                util.disown(["qutebrowser", ":config-source"])
