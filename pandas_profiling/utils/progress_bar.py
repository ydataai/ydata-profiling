from pandas_profiling.utils.notebook import in_ipynb

if in_ipynb():
    from tqdm import tqdm_notebook as tqdm
else:

    from tqdm import tqdm


def create_bar(total: float, description: str) -> tqdm:
    """Returns a tqdm bar with the project default format

        Returns:
            A tqdm object
    """
    return tqdm(desc=description, total=total, leave=False, unit='%', dynamic_ncols=True)
