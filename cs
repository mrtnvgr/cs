#!/bin/python
import subprocess, shutil, \
       json, os, sys
import generator, logger

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
        light = False
        for arg in args:
            if arg in ("-l", "--light"):
                light = True
                args.remove(arg)
        if len(args)==1:
            self.help()
        elif len(args)==2:
            name = None
        else:
            name = args[2]
        self.args = Namespace(cmd=args[1], name=name, light=light)

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
                self.updaters()
            else:
                logging.error("Status file doesnt exist")
                exit(1)
        else:
            if self.args.name!=None:
                if self.args.cmd=="set":
                    self.scheme = self.getColorscheme()
                    self.setColorscheme()
                    self.genStatus()
                    self.currentScheme()
                elif self.args.cmd in ("generate", "gen"):
                    logger.info("Generating colors from wallpaper...")
                    self.scheme = generator.gen(self.args.name, light=self.args.light)
                    # TODO: genstatus light tag
                    self.setColorscheme()
                    self.genStatus(wallpaper=True)
                    self.currentScheme(name=False)
                elif self.args.cmd in ("import","imp"):
                    self.importColorscheme()
                elif self.args.cmd in ("delete","del"):
                    self.deleteColorscheme()
            else:
                logger.error("Unknown command or invalid usage")
                exit(1)

    def setColorscheme(self):
        self.getFullColorScheme()
        self.generateTemplates()
        self.updaters()

    def getColorscheme(self):
        logger.info("Getting colorscheme...")
        for path in self.path_colorschemes:
            path = os.path.join(path, f"{self.args.name}.json")
            if os.path.exists(path):
                self.scheme_path = path
                return json.load(open(path))
        logger.error(f"Unknown colorscheme: {self.args.name}")
        exit(1)

    def getFullColorScheme(self):
        for color in self.scheme.copy():
            self.scheme[f"{color}_strip"] = self.scheme[color][1:]

    def generateTemplates(self):
        logger.info("Generating templates...")
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
            

    def importColorscheme(self):
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
            logger.error(f"File {self.args.name} doesnt exist")
            exit(1)

    def saveColorscheme(self):
        path = os.path.join(self.path_config, "colorschemes",
                            self.args.name)
        json.dump(self.scheme, open(path, "w"))
        logger.info(f"Colorscheme saved to {path}")

    def deleteColorscheme(self):
        for folder in self.path_colorschemes:
            path = os.path.join(folder, f"{self.args.name}.json")
            if os.path.exists(path):
                ch = logger.warning(f"Delete: {path} (y/n): ", func=input).lower()
                if ch=="y":
                    os.remove(path)

    def listColorschemes(self):
        logger.info("Colorschemes: ")
        for path in self.path_colorschemes:
            for file in os.listdir(path):
                if file.endswith(".json"):
                    print(f"    - {self.beautify(file)}")

    def updaters(self):
        logger.info("Updating colors...")
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
                logger.warning("Xresources failed")

    def updatetty(self):
        path = os.path.join(os.getenv("HOME"), ".cache",
                            "cs", "colors.sh")
        term = os.getenv("TERM")
        if term=="linux":
            subprocess.run(["sh", path])
        
    def genStatus(self, wallpaper=False):
        path = os.path.join(os.getenv("HOME"), ".cache",
                            "cs", "status.json")
        status = {"source": {}, 
                  "colorscheme": {"name": self.args.name, 
                                  "light": self.args.light}}
        
        if wallpaper:
            status["source"]["type"] = "wallpaper"
            status["source"]["path"] = os.path.abspath(self.args.name)
        else:
            status["source"]["type"] = "colorscheme"
            status["source"]["path"] = self.scheme_path
        json.dump(status, open(path,"w"))

    def currentScheme(self, name=True):
        logger.info("Current colorscheme: ", func_args={"end": ''})
        if name: print(f"{self.beautify(self.args.name)}")
        self.colorPalette()

    def colorPalette(self):
        for i in range(0, 16):
            if i % 8 == 0:
                print()
            if i > 7:
                i = "8;5;%s" % i
            print("\033[4%sm%s\033[0m" % (i, " "*4), end="")
        print("\n")

    def help(self):
        print("cs {mode} {name}")
        print("    Modes:")
        print("        set {name} - set colorscheme")
        print("        del (delete) {name} - delete colorscheme")
        print("        gen (generate) {path} - generate colorscheme from wallpaper")
        print("        imp (import) {path} - import colorscheme from other formats")
        print("        rel (reload) - reload templates")
        print("        list - print colorschemes")
        print("        help - print help")
        print("    Optional arguments:")
        print("        -l (--light) - generate light colorscheme")
        exit(0)

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
