import json, os
from cs import logger

class Importer:
    def __init__(self):
        pass

    def importColorscheme(self, name):
        self.scheme = {}
        if os.path.exists(name):
            self.text = open(name).read()
            if self.text[0]=="{": # JSON
                self.text = json.loads(self.text)
                # PYWAL
                if "colors" in self.text and "special" in self.text:
                    for pack in ("special","colors"):
                        for color in self.text[pack]:
                            self.scheme[color] = self.text[pack][color]
            else:
                # XRESOURCES
                specials = ["foreground", "background", "cursor"]
                elems = list(specials)
                elems += [f"color{i}" for i in range(0,16)]
                for line in self.text.split("\n"):
                    if not line.startswith("!"):
                        line = line.replace(" ", "").lower().split(":")
                        if any(line):
                            if any([special in line[0] and special not in elems for special in specials]):
                                continue
                            for elem in elems:
                                if elem in line[0]:
                                    if elem not in self.scheme:
                                        logger.info(f"Colorscheme color: {': '.join(line)} -> {elem}")
                                        self.scheme[elem] = line[1]
                                        elems.remove(elem)
                                        break
                if elems!=[]:
                    logger.error("Enough colors not found")
                    exit(1)
            if self.scheme!={}: return self.scheme
        logger.error(f"File {name} doesnt exist")
        exit(1)
