#!/bin/python
import subprocess, shutil, \
       json, os, sys
import generator

class Namespace:
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

class Main:
    def __init__(self):
        self.getargs()
        self.setpaths()
        self.cmds()

    def getargs(self):
        args = sys.argv
        if len(args)==1:
            self.help()
        elif len(args)==2:
            name = None
        else:
            name = args[2]
        self.args = Namespace(cmd=args[1], name=name)

    def setpaths(self):
        self.path_me = os.path.dirname(os.path.realpath(__file__))
        self.path_home = os.getenv("HOME")
        self.path_config = os.path.join(self.path_home, ".config", "cs")
        self.path_cache = os.path.join(self.path_home, ".cache", "cs")
        self.path_colorschemes = (
                os.path.join(self.path_config, "colorschemes"),
                os.path.join(self.path_me, "colorschemes"))
        for folder in (self.path_home,
                       self.path_config,
                       self.path_cache,
                       self.path_colorschemes):
            if type(folder)==str:
                os.makedirs(folder, exist_ok=True)
            else:
                for fol in folder:
                    os.makedirs(fol, exist_ok=True)

    def cmds(self):
        if self.args.cmd == "list":
            self.listColorschemes()
        elif self.args.cmd == "help":
            self.help()
        elif self.args.cmd in ("reload", "rel"):
            path = os.path.join(self.path_cache, "status.json")
            if os.path.exists(path):
                self.args.name = json.load(open(path))["colorscheme"]["name"]
                self.scheme = self.getColorscheme()
                self.setColorscheme()
        else:
            if self.args.name!=None:
                if self.args.cmd=="set":
                    self.scheme = self.getColorscheme()
                    self.setColorscheme()
                elif self.args.cmd in ("generate", "gen"):
                    print(f"[{self.paint(2, '*')}] Generating colors from wallpaper...")
                    self.scheme = generator.gen(self.args.name)
                    # TODO: light arg, change args.name to normal, genstatus wallpaper tag
                    self.setColorscheme()
                elif self.args.cmd in ("convert","conv"):
                    self.convertColorscheme()
                elif self.args.cmd in ("delete","del"):
                    self.deleteColorscheme()
            else:
                print(f"[{self.paint(1, 'x')}] error: Unknown command or invalid usage")
                exit(1)

    def setColorscheme(self):
        self.getFullColorScheme()
        self.generateTemplates()
        self.updaters()
        self.genStatus()
        self.currentScheme()

    def getColorscheme(self):
        print(f"[{self.paint(2, '*')}] Getting colorscheme...")
        for path in self.path_colorschemes:
            path = os.path.join(path, f"{self.args.name}.json")
            if os.path.exists(path):
                return json.load(open(path))
        print(f"[{self.paint(1, 'x')}] error: Unknown colorscheme: {self.args.name}")
        exit(1)

    def getFullColorScheme(self):
        for color in self.scheme.copy():
            self.scheme[f"{color}_strip"] = self.scheme[color][1:]

    def generateTemplates(self):
        print(f"[{self.paint(2, '*')}] Generating templates...")
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
            print(f"[{self.paint(1, 'x')}] error: File {self.args.name} doesnt exist")

    def saveColorscheme(self):
        path = os.path.join(self.path_config, "colorschemes",
                            self.args.name)
        json.dump(self.scheme, open(path, "w"))
        print(f"[{self.paint(3, '*')}] Colorscheme saved to {path}")

    def deleteColorscheme(self):
        for folder in self.path_colorschemes:
            path = os.path.join(folder, f"{self.args.name}.json")
            if os.path.exists(path):
                ch = input(f"[{self.paint(3, '!')}] delete: {path} (y/n): ").lower()
                if ch=="y":
                    os.remove(path)

    def listColorschemes(self):
        print(f"[{self.paint(2, '*')}] Colorschemes: ")
        for path in self.path_colorschemes:
            for file in os.listdir(path):
                if file.endswith(".json"):
                    print(f"    - {self.beautify(file)}")

    def updaters(self):
        print(f"[{self.paint(2, '*')}] Updating colors...")
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
        print(f"[{self.paint(2, '*')}] Current colorscheme: {self.beautify(self.args.name)}")
        self.colorPalette()

    def colorPalette(self):
        for i in range(0, 16):
            if i % 8 == 0:
                print()
            if i > 7:
                i = "8;5;%s" % i
            print("\033[4%sm%s\033[0m" % (i, " " * (80 // 20)), end="")
        print("\n")

    def help(self):
        print("cs {mode} {name}")
        print("    Modes:")
        print("        set - set colorscheme")
        print("        del (delete) - delete colorscheme")
        print("        gen (generate) - generate colorscheme from wallpaper")
        print("        conv (convert) - convert colorscheme from other formats")
        print("        rel (reload) - reload templates")
        print("        list - print colorschemes")
        print("        help - print help")
        exit(0)

    @staticmethod
    def paint(color, text, bold=1):
        return f"\x1b[{0+bold};{color+30};40m{text}\x1b[0m"

    @staticmethod
    def beautify(text):
        text = text.removesuffix(".json")
        if "_" in text:
            text = text.replace("_", " ")
        else:
            if "-" in text:
                text = text.replace("_", " ")
        return text.title()

    @staticmethod
    def strip(color):
        return color[1:]

if __name__=="__main__":
    Main()
