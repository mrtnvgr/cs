def paint(color, text, bold=1):
    return f"\x1b[{0+bold};{color+30};40m{text}\x1b[0m"

def info(text, func=print, func_args={}):
    func(f"[{paint(2, '*')}] {text}", **func_args)

def warning(text, func=print, func_args={}):
    func(f"[{paint(3, '!')}] {text}", **func_args)

def error(text, func=print, func_args={}):
    func(f"[{paint(1, 'x')}] {paint(1, 'error')}: {text}", **func_args)
