def get_content(*args, sep):
    result = ''

    for i in args:
        result += (i + sep)
    result = result.removesuffix(sep)

    return result
