from pandas_profiling.config import config

from tqdm.auto import tqdm


def create_bar(total: float, description: str) -> tqdm:
    """Returns a tqdm bar with the project default format

        Args:
            total: The number of expected iterations
            description: The description of the bar

        Returns:
            A tqdm object
    """
    disable_progress_bar = not(config['progress_bar'].get(bool))
    return tqdm(desc=description, total=total, leave=False, unit='%', dynamic_ncols=True,
                disable=disable_progress_bar)
