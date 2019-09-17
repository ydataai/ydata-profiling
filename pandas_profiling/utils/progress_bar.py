from tqdm.auto import tqdm

from pandas_profiling.config import config


class ProgressBar(object):

    def __init__(self, total: float, description: str) -> None:
        """
            Args:
                total: The number of expected iterations
                description: The description of the bar
        """
        enable_progress_bar = config['progress_bar'].get(bool)
        if enable_progress_bar:
            self.bar = self.create_bar(total=total, description=description)
        else:
            self.bar = None

    def create_bar(self, total: float, description: str) -> tqdm:
        """Returns a tqdm bar with the project default format

            Args:
                total: The number of expected iterations
                description: The description of the bar

            Returns:
                A tqdm object
        """
        return tqdm(desc=description, total=total, leave=False, unit='%', dynamic_ncols=True)

    def _bar_exists(self) -> bool:
        """It checks whether the ProgressBar object has a tqdm bar attribute
            Returns:
                A boolean
       """
        return not (self.bar is None)

    def update_progress(self, progress: float = None):
        """It updates the progress of the tqdm bar

            Args:
                progress: The total of progress to update
        """
        if (self._bar_exists()) and (progress is not None):
            self.bar.update(progress)

    def update_description(self, description: str = None):
        """It updates the description of the tqdm bar

            Args:
                description: The description of the bar
        """
        if (self._bar_exists()) and (description is not None):
            self.bar.set_description(description)

    def update_progress_and_description(self, progress: float = None, description: str = None):
        """It updates the progress and description of the tqdm bar

            Args:
                progress: The total of progress to update
                description: The description of the bar
        """
        self.update_progress(progress)
        self.update_description(description)

    def close(self):
        """It closes the tqdm bar"""
        if self._bar_exists():
            self.bar.close()
