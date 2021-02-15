# coding=utf-8

def escape(fed):
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
    return result

def hex(fed):
    # use fullwidth char
    result = fed.replace("&", "＆")
    result = result.replace("+", "＋")
    result = result.replace("#", "＃")
    result = result.replace("%", "%25")
    return result