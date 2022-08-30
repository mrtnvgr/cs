import subprocess, re

def gen(img, light=False):
    colors = genColors(img)
    return adjustColors(colors, light)

def getColors(colors, img):
    args = ["-resize", "25%", "-colors", str(colors),
            "-unique-colors", "txt:-"]
    img += "[0]"
    colors = subprocess.check_output(["convert", img, *args]).splitlines()
    return [re.search("#.{6}", str(col)).group(0) for col in colors[1:]]

def genColors(img):
    for i in range(0, 20, 1):
        raw_colors = getColors(16 + i, img)

        if len(raw_colors) > 16:
            break

        if i == 19:
            logging.error("Imagemagick couldn't generate a suitable palette.")
            exit(1)
    return raw_colors

def adjustColors(colors, light):
    raw_colors = colors[:1] + colors[8:16] + colors[8:-1]
    if light:
        for color in raw_colors:
            color = saturate(color, 0.5)
        raw_colors[0] = lighten(colors[-1], 0.85)
        raw_colors[7] = colors[0]
        raw_colors[8] = darken(colors[-1], 0.4)
        raw_colors[15] = colors[0]
    else:
        if raw_colors[0][1]!="0":
            raw_colors[0] = darken(raw_colors[0], 0.40)
        raw_colors[7] = blend(raw_colors[7], "#EEEEEE")
        raw_colors[8] = darken(raw_colors[7], 0.30)
        raw_colors[15] = blend(raw_colors[15], "#EEEEEE")
    return colors

def hex_to_rgb(color):
    return tuple(bytes.fromhex(color.strip("#")))

def rgb_to_hex(color):
    return "#%02x%02x%02x" % (*color,)

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

print(gen("120.jpg"))
