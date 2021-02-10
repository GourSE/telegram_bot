# escape for md

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
    result = result.replace("|", "\\|")
    result = result.replace("=", "\\=")
    return result

def hex(fed):
    result = fed.replace("+", "%2B")
    # this is a different ampercent, %26 does not work in api
    result = result.replace("&", "＆")
    result = result.replace("#", "%23")
    result = result.replace("%", "%25")
    return result