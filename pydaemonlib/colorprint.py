import sys

if sys.platform == "win32":
    import colors


tpl_red = "\033[91m{0}\033[0m"
tpl_green = "\033[92m{0}\033[0m"
tpl_empty = "\033[98m{0}\033[0m"


def red(string):
    if sys.platform == "win32":
        return colors.red(string)
    return tpl_red.format(string)


def green(string):
    if sys.platform == "win32":
        return colors.green(string)
    return tpl_green.format(string)


def empty(string):
    if sys.platform == "win32":
        return string
    return tpl_empty.format(string)
