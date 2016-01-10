import pandas as pd
import pandas_profiling

if __name__ == "__main__":
    import argparse
    import webbrowser

    parser = argparse.ArgumentParser(description='Profile the variables in a CSV file and generate a HTML report.')
    parser.add_argument("inputfile", help="CSV file to profile")
    parser.add_argument("-o", "--output", help="Output report file", default=pandas_profiling.DEFAULT_OUTPUTFILE)
    parser.add_argument("-s", "--silent", help="Only generate but do not open report", action="store_true")

    args = parser.parse_args()

    df = pd.read_csv(args.inputfile, sep=None, parse_dates=True)

    p = pandas_profiling.ProfileReport(df)
    p.to_file(outputfile=args.output)

    if not args.silent:
        webbrowser.open_new_tab(p.file.name)