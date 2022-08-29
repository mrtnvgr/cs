#!/bin/python
import argparse, subprocess, \
       shutil, json, os

class Main:
    def __init__(self):
        self.getargs()
        self.setpaths()
        self.cmds()

    def getargs(self):
        parser = argparse.ArgumentParser("cs")
        parser.add_argument("cmd", type=str, choices=("set",
                                                      "convert",
                                                      "conv") )
        parser.add_argument("name", type=str)
        self.args = parser.parse_args()

    def setpaths(self):
        self.path_me = os.path.dirname(os.path.realpath(__file__))
        self.path_home = os.getenv("HOME")
        self.path_config = os.path.join(self.path_home, ".config", "cs")
        self.path_cache = os.path.join(self.path_home, ".cache", "cs")
        for folder in (self.path_home,
                       self.path_config,
                       self.path_cache):
            os.makedirs(folder, exist_ok=True)

    def cmds(self):
        if self.args.cmd=="set":
            print(f"[{self.paint(2, '*')}] Getting colorscheme...")
            self.scheme = self.getColorscheme()
            self.getFullColorScheme()
            print(f"[{self.paint(2, '*')}] Generating templates...")
            self.generateTemplates()
            print(f"[{self.paint(2, '*')}] Updating colors...")
            self.updaters()
            self.genStatus()
            self.currentScheme()
        elif self.args.cmd in ("convert","conv"):
            self.convertColorscheme()

    def getColorscheme(self):
        paths = []
        paths.append(os.path.join(self.path_config, "colorschemes"))
        paths.append(os.path.join(self.path_me, "colorschemes"))
        for path in paths:
            path = os.path.join(path, f"{self.args.name}.json")
            if os.path.exists(path):
                return json.load(open(path))
        print(f"[{self.paint(1, 'x')}] Unknown colorscheme: {self.args.name}")
        exit(1)

    def getFullColorScheme(self):
        for color in self.scheme.copy():
            self.scheme[f"{color}_strip"] = self.scheme[color][1:]

    def generateTemplates(self):
        path = os.path.join(self.path_me, "templates")
        for file in os.listdir(path):
            path = os.path.join(path, file)
            if os.path.isfile(path):
                template = open(path).read()
                template = template.format(**self.scheme)
                open(os.path.join(self.path_cache, file), "w").write(template)
        self.generateOptionalTemplates()

    def generateOptionalTemplates(self):
        path = os.path.join(self.path_home, ".termux")
        if os.path.exists(path):
            path = os.path.join(path, "colors.properties")
            template = open(os.path.join(self.path_me, "templates",
                                         "optional",
                                         "colors.termux")).read()
            open(path, "w").write(template.format(**self.scheme))
            

    def convertColorscheme(self):
        if os.path.exists(self.args.name):
            text = open(self.args.name).read()
            if text[0]=="{":
                self.scheme = {}
                text = json.loads(text)
                if "colors" in text and "special" in text:
                    for pack in ("special","colors"):
                        for color in text[pack]:
                            self.scheme[color] = text[pack][color]
                    self.saveColorscheme()
        else:
            print(f"[{self.paint(1, 'x')}] File {self.args.name} doesnt exist")

    def saveColorscheme(self):
        path = os.path.join(self.path_config, "colorschemes",
                            self.args.name)
        json.dump(self.scheme, open(path, "w"))
        print(f"[{self.paint(3, '*')}] Colorscheme saved to {path}")

    def updaters(self):
        self.updateTermux()
        self.updatexrdb()
        self.updatetty()

    def updateTermux(self):
        path = os.path.join(self.path_home, ".termux")
        if os.path.exists(path):
            subprocess.run(["termux-reload-settings"])


    def updatexrdb(self):
        path = os.path.join(os.getenv("HOME"), ".cache",
                            "cs", "colors.Xresources")
        if shutil.which("xrdb"):
            rc = subprocess.run(["xrdb", "-merge", "-quiet", path],
                                 check=False,
                                 stderr=subprocess.DEVNULL).returncode
            if rc==1:
                print(f"[{self.paint(3, '!')}] Xresources failed")

    def updatetty(self):
        path = os.path.join(os.getenv("HOME"), ".cache",
                            "cs", "colors.sh")
        term = os.getenv("TERM")
        if term=="linux":
            subprocess.run(["sh", path])
        
    def genStatus(self):
        path = os.path.join(os.getenv("HOME"), ".cache",
                            "cs", "status.json")
        status = {"colorscheme": {"name": self.args.name}}
        json.dump(status, open(path,"w"))

    def currentScheme(self):
        print(f"[{self.paint(2, '*')}] Current colorscheme: {self.args.name.title()}")
        self.colorPalette()

    def colorPalette(self):
        for i in range(0, 16):
            if i % 8 == 0:
                print()
            if i > 7:
                i = "8;5;%s" % i
            print("\033[4%sm%s\033[0m" % (i, " " * (80 // 20)), end="")
        print("\n")

    @staticmethod
    def paint(color, text, bold=1):
        return f"\x1b[{0+bold};{color+30};40m{text}\x1b[0m"

    @staticmethod
    def strip(color):
        return color[1:]

if __name__=="__main__":
    Main()
