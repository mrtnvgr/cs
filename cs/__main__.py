#!/bin/python
import json, imghdr, shutil, os, sys
from cs import colorscheme
from cs import thsave
from cs import thload
from cs import importer
from cs import util
from cs import status as cs_status
from cs import reload
from cs import logger


class Main:
    def __init__(self):
        self.getargs()
        util.setupPaths()
        self.cmds()

    def getargs(self):
        args = sys.argv
        light = False
        for arg in args:
            if arg in ("-l", "--light"):
                light = True
                args.remove(arg)
        if len(args) == 1:
            self.help()
        elif len(args) == 2:
            name = None
        else:
            name = args[2]
        self.args = {"cmd": args[1], "name": name, "light": light}

    def cmds(self):
        if self.args["cmd"] == "list":
            self.listColorschemes()
        elif self.args["cmd"] == "help":
            self.help()
        elif self.args["cmd"] in ("reload", "rel"):
            path = os.path.join(util.paths["cache"], "status.json")
            if os.path.exists(path):
                reload.reload_all()
            else:
                logger.error("Status file doesnt exist")
                exit(1)
        elif self.args["cmd"] in ("status", "stat"):
            path = os.path.join(util.paths["cache"], "status.json")
            print(cs_status.get(path, self.args["name"]))
            exit(0)
        elif self.args["cmd"] in ("generate", "gen"):
            logger.info("Generating colors from wallpaper...")

            # Check if name arg is not specified
            if self.args["name"] == None:
                status_path = os.path.join(util.paths["cache"], "status.json")

                # Overwrite name arg with wallpaper path from status
                self.args["name"] = cs_status.get(status_path, "wallpaper")

            self.scheme = colorscheme.Colorscheme(self.args["name"], self.args["light"])
            self.scheme.generate()
            self.scheme.currentScheme(name=False)
        else:
            if self.args["name"] != None:
                if self.args["cmd"] == "set":
                    wallpaper = (
                        os.path.exists(self.args["name"])
                        and imghdr.what(self.args["name"]) != None
                    )
                    url = util.isUrl(self.args["name"])

                    if wallpaper or url:
                        if colorscheme.wallpaper.set(self.args["name"]) == True:
                            status_path = os.path.join(
                                util.paths["cache"], "status.json"
                            )
                            if os.path.exists(status_path):
                                status = json.load(open(status_path))
                                status["wallpaper"] = os.path.abspath(self.args["name"])
                                json.dump(status, open(status_path, "w"), indent=4)
                    else:
                        self.scheme = colorscheme.Colorscheme(
                            self.args["name"], self.args["light"]
                        )
                        self.scheme.get()
                        self.scheme.set()
                        self.scheme.currentScheme()
                elif self.args["cmd"] in ("import", "imp"):
                    imp = importer.Importer()
                    self.scheme = imp.importColorscheme(self.args["name"])
                    if self.scheme:
                        if not self.args["name"].endswith(".json"):
                            if "." in self.args["name"]:
                                self.args["name"] = self.args["name"].split(".")[0]
                            self.args["name"] += ".json"
                        self.saveColorscheme()
                elif self.args["cmd"] == "save":
                    thsave.save(self.args["name"])
                elif self.args["cmd"] == "load":
                    thload.load(self.args["name"])
                elif self.args["cmd"] in ("delete", "del"):
                    self.deleteColorscheme("colorscheme", util.paths["colorschemes"])
                    self.deleteColorscheme("theme", util.paths["themes"])
            else:
                logger.error("Unknown command or invalid usage")
                exit(1)

    def saveColorscheme(self):
        path = os.path.join(
            util.paths["config"], "colorschemes", os.path.basename(self.args["name"])
        )
        json.dump(self.scheme, open(path, "w"), indent=4)
        logger.info(f"Colorscheme saved to {path}")

    def deleteColorscheme(self, filetype, paths):
        if type(paths) is str:
            paths = [paths]
        for folder in paths:
            path = os.path.join(folder, self.args["name"])
            if os.path.exists(path) or os.path.exists(f"{path}.json"):
                name = os.path.basename(path)
                ch = logger.warning(
                    f"Delete {filetype}: {name} (y/n): ", func=input
                ).lower()
                if ch == "y":
                    if os.path.isfile(path):
                        os.remove(path)
                    else:
                        shutil.rmtree(path)

    def listColorschemes(self):
        for cpath, name in (
            (util.paths["colorschemes"], "Colorschemes: "),
            (util.paths["themes"], "Themes: "),
        ):
            files = []
            if type(cpath) is str:
                cpath = [cpath]

            for path in list(cpath):
                for file in os.listdir(path):
                    files.append(file)

            if files != []:
                print()
                logger.info(name)
                for file in sorted(files):
                    if file.endswith(".json"):
                        file = file.removesuffix(".json")
                    print(f"    - {util.beautify(file)} ({file})")
        print()

    def help(self):
        print("cs {mode} {name}")
        print("    Modes:")
        print("        set {name} - set colorscheme/wallpaper path/wallpaper url")
        print("        del (delete) {name} - delete colorscheme/theme")
        print(
            "        gen (generate) '' (current wallpaper) or {path/wallpaper url} - generate colorscheme from wallpaper"
        )
        print("        imp (import) {path} - import colorscheme from other formats")
        print("        save {theme name} - save theme")
        print("        load {theme name} - load theme")
        print("        rel (reload) - reload templates")
        print("        stat (status) {.output.type} - print status element")
        print("        list - print colorschemes/themes")
        print("        help - print help")
        print("    Optional arguments:")
        print("        -l (--light) - generate light colorscheme")
        exit(0)

    @staticmethod
    def strip(color):
        return color[1:]


def main():
    if sys.platform != "linux":
        logger.error("Only for linux")
        exit(1)
    else:
        Main()


if __name__ == "__main__":
    main()
