import re


def camel_to_snake_converter(value):
    pattern = re.compile(r"(?<!^)(?=[A-Z])")
    return pattern.sub("_", value).lower()


def snake_to_camel_converter(value):
    init, *temp = value.split("_")
    return "".join([init.lower(), *map(str.title, temp)])
