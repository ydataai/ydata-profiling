import pandas as pd

from pandas_profiling import ProfileReport

if __name__ == "__main__":
    df = pd.read_csv(
        "https://www.vektis.nl/uploads/Docs%20per%20pagina/Open%20Data%20Bestanden/2017/Vektis%20Open%20Databestand%20Zorgverzekeringswet%202017%20-%20postcode3.csv",
        sep=";",
        low_memory=False,
    )
    report = ProfileReport(
        df,
        title="Vektis Postal Code 2017",
        correlations={
            "recoded": {"calculate": False},
            "kendall": {"calculate": False},
            "phi_k": {"calculate": False},
            "cramers": {"calculate": False},
        },
        plot={"histogram": {"bayesian_blocks_bins": False}},
    )
    report.to_file("vektis_report.html", True)
