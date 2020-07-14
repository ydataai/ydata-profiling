import numpy as np
import pandas as pd

from pandas_profiling.config import config

import visions as vis
from visions import (Categorical, Boolean, Float, DateTime, URL, Complex, Path, File, Image, Integer, Generic,
                     Object)

from visions.typesets.typeset import VisionsTypeset

class ProfilingTypeSet(VisionsTypeset):
    """Base typeset for pandas-profiling"""
    def __init__(self):
        types = {
            Categorical,
            Boolean,
            Float,
            DateTime,
            URL,
            Complex,
            Path,
            File,
            Image,
            Integer,
            Object
        }
        super().__init__(types)