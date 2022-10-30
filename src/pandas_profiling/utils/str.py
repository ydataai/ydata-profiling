import re

pattern = re.compile(r"(?<!^)(?=[A-Z])")


def camel_to_snake(input_string):
    """
    this converts a camelcase string to a snaked lowercase string
    """
    return pattern.sub("_", input_string).lower()
