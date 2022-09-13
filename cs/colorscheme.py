from cs import logger
from cs import status
from cs import reload
from cs import generator
from cs import wallpaper
from cs import util
import json, os

class Colorscheme:
    def __init__(self, name, light):
        self.name = name
        self.path = name
        self.light = light
        self.paths = util.getPaths()

    def get(self):
        logger.info("Getting colorscheme...")
        for path in self.paths["colorschemes"]:
            path = os.path.join(path, f"{self.name}.json")
            if os.path.exists(path):
                self.path = path
                self.scheme = json.load(open(path))
                return
        logger.error(f"Unknown colorscheme: {self.name}")
        exit(1)

    def set(self, wallpaper=False):
        self.getFullColorScheme()
        self.generateTemplates()
        status.gen(cs_name=self.name, light=self.light,
                   cs_path=self.path, wallpaper=wallpaper)
        reload.reload_all()

    def generate(self):
        self.scheme = generator.gen(self.name, light=self.light)
        wallpaper.set(self.name)
        self.set(wallpaper=True)

    def getFullColorScheme(self):
        for color in self.scheme.copy():
            self.scheme[f"{color}_strip"] = self.scheme[color][1:]

    def generateTemplates(self):
        logger.info("Generating templates...")
        templates_path = os.path.join(self.paths["me"], "templates")
        for file in os.listdir(templates_path):
            path = os.path.join(templates_path, file)
            if not os.path.isdir(path):
                template = open(path).read()
                template = template.format(**self.scheme)
                open(os.path.join(self.paths["cache"], file), "w").write(template)
