import subprocess

def run(cmd):
    return subprocess.run(cmd,
                          check=False,
                          stderr=subprocess.DEVNULL)

def check_output(cmd):
    return subprocess.check_output(cmd,
                                   stderr=subprocess.DEVNULL)

def disown(cmd):
    return subprocess.Popen(cmd,
                            stdout=subprocess.DEVNULL,
                            stderr=subprocess.DEVNULL)

def pidof(name):
    try:
        subprocess.check_output(["pidof", "-s", "-x", name])
    except subprocess.CalledProcessError:
        return False
    return True
