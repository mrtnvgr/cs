import platform, json, glob, os
from pathlib import Path
from cs import logger
from cs import util

def set_special(index, color, iterm_name="h", alpha=100):
    if platform.system == "Darwin" and iterm_name:
        return "\033]P%s%s\033\\" % (iterm_name, color.strip("#"))

    if index in [11, 708] and alpha != "100":
        return "\033]%s;[%s]%s\033\\" % (index, alpha, color)

    return "\033]%s;%s\033\\" % (index, color)


def set_color(index, color):
    if platform.system == "Darwin" and index < 20:
        return "\033]P%1x%s\033\\" % (index, color.strip("#"))

    return "\033]4;%s;%s\033\\" % (index, color)


def create_sequences(colors, vte_fix=False):
    sequences = [set_color(index, colors["color%s" % index])
                 for index in range(16)]

    sequences.extend([
        set_special(10, colors["foreground"], "g"),
        set_special(11, colors["background"], "h"),
        set_special(12, colors["cursor"], "l"),
        set_special(13, colors["foreground"], "j"),
        set_special(17, colors["foreground"], "k"),
        set_special(19, colors["background"], "m"),
        set_color(232, colors["background"]),
        set_color(256, colors["foreground"]),
        set_color(257, colors["background"]),
    ])

    if not vte_fix:
        sequences.extend(
            set_special(708, colors["background"], "")
        )

    return "".join(sequences)


def send(to_send=True, vte_fix=False):
    colors = json.load(open(os.path.join(util.paths["cache"], "colors.json")))
    if platform.system == "Darwin":
        tty_pattern = "/dev/ttys00[0-9]*"
    else:
        tty_pattern = "/dev/pts/[0-9]*"

    sequences = create_sequences(colors, vte_fix)

    if to_send:
        for term in glob.glob(tty_pattern):
            try:
                with open(term, "w") as file:
                    file.write(sequences)
            except PermissionError as p:
                path = Path(p.filename)
                owner = path.owner()
                group = path.group()
                logger.warning(f"Permission denied: {p.filename} is owned by {owner}:{group}")
    
    with open(os.path.join(util.paths["cache"], "sequences"), "w") as file:
        file.write(sequences)
