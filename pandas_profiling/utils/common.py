import collections


def update(d: dict, u: dict) -> dict:
    """ Recursively update a dict.

    Args:
        d: Dictionary to update.
        u: Dictionary with values to use.

    Returns:
        The merged dictionairy.
    """
    for k, v in u.items():
        if isinstance(v, collections.Mapping):
            d[k] = update(d.get(k, {}), v)
        else:
            d[k] = v
    return d
