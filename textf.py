# coding=utf-8

def escape(fed):
    if fed is not None:
        result = fed.replace("\\", "\\\\")
        result = result.replace("`", "\\`")
        result = result.replace("*", "\\*")
        result = result.replace("_", "\\_")
        result = result.replace("{", "\\{")
        result = result.replace("}", "\\}")
        result = result.replace("[", "\\[")
        result = result.replace("]", "\\]")
        result = result.replace("(", "\\(")
        result = result.replace(")", "\\)")
        result = result.replace("-", "\\-")
        result = result.replace(".", "\\.")
        result = result.replace("!", "\\!")
        result = result.replace("~", "\\~")
        result = result.replace(">", "\\>")
        result = result.replace("=", "\\=")
        result = result.replace("|", "\\|")
    else:
        result = fed
    return result

def hex(fed):
    # use fullwidth char
    if fed is not None:
        result = fed.replace("&", "＆")
        result = result.replace("+", "＋")
        result = result.replace("#", "＃")
        result = result.replace("%", "%25")
    else:
        result = fed
    return result