def paint(color, text, bold=1):
    return f"\033[{0+bold};{color+30};40m\033[49m{text}\033[0m"


def info(text, func=print, func_args={}):
    return func(f"[{paint(2, '*')}] {text}", **func_args)


def warning(text, func=print, func_args={}):
    return func(f"[{paint(3, '!')}] {text}", **func_args)


def error(text, func=print, func_args={}):
    return func(f"[{paint(1, 'x')}] {paint(1, 'error')}: {text}", **func_args)
