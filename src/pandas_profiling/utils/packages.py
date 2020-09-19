import importlib.util


def is_installed(package_name):
    spec = importlib.util.find_spec(package_name)
    return spec is not None
