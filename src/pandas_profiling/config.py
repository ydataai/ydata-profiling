"""Configuration for the package."""
from enum import Enum
from typing import Dict, List, Optional

from pydantic import BaseModel, BaseSettings, Field


def _merge_dictionaries(dict1, dict2):
    """
    Recursive merge dictionaries.

    :param dict1: Base dictionary to merge.
    :param dict2: Dictionary to merge on top of base dictionary.
    :return: Merged dictionary
    """
    for key, val in dict1.items():
        if isinstance(val, dict):
            dict2_node = dict2.setdefault(key, {})
            _merge_dictionaries(val, dict2_node)
        else:
            if key not in dict2:
                dict2[key] = val

    return dict2


class Dataset(BaseModel):
    """Metadata of the dataset"""

    description: str = ""
    creator: str = ""
    author: str = ""
    copyright_holder: str = ""
    copyright_year: str = ""
    url: str = ""


class NumVars(BaseModel):
    quantiles: List[float] = [0.05, 0.25, 0.5, 0.75, 0.95]
    skewness_threshold = 20
    low_categorical_threshold = 5
    # Set to zero to disable
    chi_squared_threshold = 0.999


class CatVars(BaseModel):
    length = True
    characters = True
    words = True
    cardinality_threshold = 50
    n_obs = 5
    # Set to zero to disable
    chi_squared_threshold = 0.999
    coerce_str_to_date = False
    redact = False
    histogram_largest: int = 50


class BoolVars(BaseModel):
    n_obs: int = 3

    # string to boolean mapping dict
    mappings = {
        "t": True,
        "f": False,
        "yes": True,
        "no": False,
        "y": True,
        "n": False,
        "true": True,
        "false": False,
    }


class FileVars(BaseModel):
    active: bool = False


class PathVars(BaseModel):
    active: bool = False


class ImageVars(BaseModel):
    active = False
    exif = True
    hash = True


class UrlVars(BaseModel):
    active: bool = False


class Univariate(BaseModel):
    num = NumVars()
    cat = CatVars()
    image = ImageVars()
    bool = BoolVars()
    path = PathVars()
    file = FileVars()
    url = UrlVars()


class MissingPlot(BaseModel):
    # Force labels when there are > 50 variables
    # https://github.com/ResidentMario/missingno/issues/93#issuecomment-513322615
    force_labels = True
    cmap: str = "RdBu"


class ImageType(Enum):
    svg = "svg"
    png = "png"


class CorrelationPlot(BaseModel):
    cmap: str = "RdBu"
    bad: str = "#000000"


class Histogram(BaseModel):
    # Number of bins (set to 0 to automatically detect the bin size)
    bins = 50
    # Maximum number of bins (when bins=0)
    max_bins = 250
    x_axis_labels: bool = True


class Pie(BaseModel):
    # display a pie chart if the number of distinct values is smaller or equal (set to 0 to disable)
    max_unique = 10


class Plot(BaseModel):
    missing = MissingPlot()
    image_format: ImageType = ImageType.svg
    correlation: CorrelationPlot = CorrelationPlot()
    # PNG dpi
    dpi: int = 800
    histogram = Histogram()
    scatter_threshold = 1000
    pie: Pie = Pie()


class Theme(Enum):
    united = "united"
    flatly = "flatly"


class Style(BaseModel):
    primary_color = "#337ab7"
    logo: str = ""
    theme: Optional[Theme] = None


class Html(BaseModel):
    # Styling options for the HTML report
    style: Style = Style()

    # Show navbar
    navbar_show: bool = True

    # Minify the html
    minify_html: bool = True

    # Offline support
    use_local_assets: bool = True

    # If True, single file, else directory with assets
    inline: bool = True

    # Assets prefix if inline = True
    assets_prefix: Optional[str] = None

    # Internal usage
    assets_path: Optional[str] = None

    full_width: bool = False


class Duplicates(BaseModel):
    head: int = 10
    key: str = "# duplicates"


class Correlation(BaseModel):
    key = ""
    calculate = Field(default=True)
    warn_high_correlations = Field(default=10)
    threshold = Field(default=0.5)


class Correlations(BaseModel):
    pearson = Correlation(key="pearson")
    spearman = Correlation(key="spearman")


class Interactions(BaseModel):
    continuous: bool = True
    # FIXME: validate with column names
    targets: List[str] = []


class Samples(BaseModel):
    head = 10
    tail = 10
    random = 0


class Variables(BaseModel):
    descriptions: dict = {}


class IframeAttribute(Enum):
    src = "src"
    srcdoc = "srcdoc"


class Iframe(BaseModel):
    height = "800px"
    width = "100%"
    attribute = IframeAttribute.srcdoc


class Notebook(BaseModel):
    """When in a Jupyter notebook"""

    iframe = Iframe()


class Report(BaseModel):
    precision = 10


class Settings(BaseSettings):
    # Title of the document
    title: str = "Pandas Profiling Report"

    dataset: Dataset = Dataset()
    variables: Variables = Variables()
    infer_dtypes: bool = True

    # Show the description at each variable (in addition to the overview tab)
    show_variable_description: bool = True

    # Number of workers (0=multiprocessing.cpu_count())
    pool_size: int = 0

    # Show the progress bar
    progress_bar: bool = True

    # Per variable type description settings
    vars: Univariate = Univariate()

    # Sort the variables. Possible values: ascending, descending or None (leaves original sorting)
    sort: Optional[str] = None

    missing_diagrams: Dict[str, bool] = {
        "bar": True,
        "matrix": True,
        "dendrogram": True,
        "heatmap": True,
    }

    correlations: Dict[str, Correlation] = {
        "spearman": Correlation(key="spearman"),
        "pearson": Correlation(key="pearson"),
        "kendall": Correlation(key="kendall"),
        "cramers": Correlation(key="cramers"),
        "phi_k": Correlation(key="phi_k"),
    }

    interactions: Interactions = Interactions()

    categorical_maximum_correlation_distinct = 100
    # Use `deep` flag for memory_usage
    memory_deep: bool = False
    plot: Plot = Plot()
    duplicates: Duplicates = Duplicates()
    samples: Samples = Samples()

    reject_variables: bool = True

    # The number of observations to show
    n_obs_unique = 10
    n_freq_table_max = 10
    n_extreme_obs = 10

    # Report rendering
    report: Report = Report()
    html: Html = Html()
    notebook = Notebook()

    def update(self, updates):
        update = _merge_dictionaries(self.dict(), updates)
        return self.parse_obj(self.copy(update=update))


class Config:
    arg_groups = {
        "sensitive": {
            "samples": None,
            "duplicates": None,
            "vars": {"cat": {"redact": True}},
        },
        "dark_mode": {
            "html": {
                "style": {
                    "theme": Theme.flatly,
                    "primary_color": "#2c3e50",
                }
            }
        },
        "orange_mode": {
            "html": {
                "style": {
                    "theme": Theme.united,
                    "primary_color": "#d34615",
                }
            }
        },
        "explorative": {
            "vars": {
                "cat": {"characters": True, "words": True},
                "url": {"active": True},
                "path": {"active": True},
                "file": {"active": True},
                "image": {"active": True},
            },
            "n_obs_unique": 10,
            "n_extreme_obs": 10,
            "n_freq_table_max": 10,
            "memory_deep": True,
        },
    }

    _shorthands = {
        "dataset": {
            "creator": "",
            "author": "",
            "description": "",
            "copyright_holder": "",
            "copyright_year": "",
            "url": "",
        },
        "samples": {"head": 0, "tail": 0, "random": 0},
        "duplicates": {"head": 0},
        "interactions": {"targets": [], "continuous": False},
        "missing_diagrams": {
            "bar": False,
            "matrix": False,
            "heatmap": False,
            "dendrogram": False,
        },
        "correlations": {
            "pearson": {"calculate": False},
            "spearman": {"calculate": False},
            "kendall": {"calculate": False},
            "phi_k": {"calculate": False},
            "cramers": {"calculate": False},
        },
    }

    @staticmethod
    def get_arg_groups(key):
        kwargs = Config.arg_groups[key]
        return Config.shorthands(kwargs)

    @staticmethod
    def shorthands(kwargs):
        for key, value in list(kwargs.items()):
            if value is None and key in Config._shorthands:
                kwargs[key] = Config._shorthands[key]
        return kwargs
