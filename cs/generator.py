import colorsys, re
from cs import util
from cs import logger


def gen(img, light=False):
    colors = genColors(img)
    return build(adjustColors(colors, light))


def getColors(colors, img):
    args = ["-resize", "25%", "-colors", str(colors), "-unique-colors", "txt:-"]
    try:
        colors = util.check_output(["convert", f"{img}[0]", *args]).splitlines()
    except:
        logger.error(f"File {img} doesnt exist")
        exit(1)
    return [re.search("#.{6}", str(col)).group(0) for col in colors[1:]]


def genColors(img):
    for i in range(0, 20, 1):
        colors = getColors(16 + i, img)

        if len(colors) > 16:
            break

        if i == 19:
            logger.error("Imagemagick couldn't generate a suitable palette.")
            exit(1)
    return colors


def adjustColors(colors, light):
    colors = colors[:1] + colors[8:16] + colors[8:-1]
    if light:
        logger.info("Generating light colorscheme...")
        for color in colors:
            color = saturate(color, 0.6)
            color = darken(color, 0.5)
        colors[0] = lighten(colors[-1], 0.95)
        colors[7] = darken(colors[0], 0.75)
        colors[8] = darken(colors[0], 0.25)
        colors[15] = colors[7]
    else:
        colors[0] = darken(colors[0], 0.80)
        colors[7] = lighten(colors[0], 0.75)
        colors[8] = lighten(colors[0], 0.25)
        colors[15] = colors[7]
    return colors


def build(colors):
    clrs = {}
    clrs["background"] = colors[0]
    clrs["foreground"] = colors[15]
    clrs["cursor"] = colors[15]
    for index, color in enumerate(colors[:-1]):
        clrs[f"color{index}"] = color
    return clrs


def darken(color, amount):
    color = [int(col * (1 - amount)) for col in hex_to_rgb(color)]
    return rgb_to_hex(color)


def lighten(color, amount):
    color = [int(col + (255 - col) * amount) for col in hex_to_rgb(color)]
    return rgb_to_hex(color)


def blend(color, color2):
    r1, g1, b1 = hex_to_rgb(color)
    r2, g2, b2 = hex_to_rgb(color2)

    r3 = int(0.5 * r1 + 0.5 * r2)
    g3 = int(0.5 * g1 + 0.5 * g2)
    b3 = int(0.5 * b1 + 0.5 * b2)

    return rgb_to_hex((r3, g3, b3))


def saturate(color, amount):
    r, g, b = hex_to_rgb(color)
    r, g, b = [x / 255.0 for x in (r, g, b)]
    h, l, s = colorsys.rgb_to_hls(r, g, b)
    s = amount
    r, g, b = colorsys.hls_to_rgb(h, l, s)
    r, g, b = [x * 255.0 for x in (r, g, b)]
    return rgb_to_hex((int(r), int(g), int(b)))


def hex_to_rgb(color):
    return tuple(bytes.fromhex(color.strip("#")))


def rgb_to_hex(color):
    return "#%02x%02x%02x" % (*color,)
