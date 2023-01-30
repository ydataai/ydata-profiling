from pathlib import Path

import pandas as pd

from ydata_profiling import ProfileReport
from ydata_profiling.utils.cache import cache_file

if __name__ == "__main__":
    file_name = cache_file(
        "vektis_postcodes.csv",
        "https://www.vektis.nl/uploads/Docs%20per%20pagina/Open%20Data%20Bestanden/2017/Vektis%20Open%20Databestand%20Zorgverzekeringswet%202017%20-%20postcode3.csv",
    )

    df = pd.read_csv(file_name, sep=";", low_memory=False)
    report = ProfileReport(
        df,
        title="Vektis Postal Code 2017",
        correlations={
            "kendall": {"calculate": False},
            "phi_k": {"calculate": False},
            "cramers": {"calculate": False},
        },
    )
    report.to_file(Path("vektis_report.html"))
