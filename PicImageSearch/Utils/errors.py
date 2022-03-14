def get_error_message(code: int) -> str:
    if code == 404:
        return "Source down"
    elif code == 302:
        return "Moved temporarily, or blocked by captcha"
    elif code == 413 or code == 430:
        return "image too large"
    elif code == 400:
        return "Did you have upload the image ?, or wrong request syntax"
    elif code == 403:
        return "Forbidden,or token invalid"
    elif code == 429:
        return "Too many request"
    elif code == 500 or code == 503:
        return "Server error, or wrong picture format"
    else:
        return "Unknown error, please report to the project maintainer"
