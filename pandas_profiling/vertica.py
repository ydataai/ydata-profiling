import vertica_python
from dotenv import find_dotenv, load_dotenv
from jinja2 import Template
import os
import sys
import json
from datetime import datetime
import numpy as np
import ssl
from collections import OrderedDict
import pandas as pd


def get_vertica_python_conn(cfg=None):
    """Generate vertica_python configuration object from environment."""
    cfg = cfg or default_cfg
    params = {
        'host': cfg['host'],
        'port': 5433,
        'database': cfg['database'],
        'read_timeout': 10 * 60 * 60,
        'unicode_error': 'strict',
        'password': cfg['password'],
        'user': cfg['user']}
    if 'VERTICA_NO_SSL' not in cfg.keys():
        ssl_context = ssl.SSLContext(ssl.PROTOCOL_SSLv23)
        ssl_context.verify_mode = ssl.CERT_NONE
        ssl_context.check_hostname = False
        params['ssl'] = ssl_context
    conn = vertica_python.connect(**params)
    return conn


# could set vertica variables
# unique_template = Template(r"""\set col {{ col }}
# select count(distinct :col) from {{ schema }}.{{ table }}""")
# ...but we have jinja2!
def open_template(fname):
    cur_dir = os.path.dirname(os.path.realpath(__file__))
    with open(os.path.join(cur_dir,
                           "vertica",
                           fname), "r") as f:
        x = Template(f.read())
    return x


count_template = open_template("count.sql.j2")
type_template = open_template("type.sql.j2")
unique_template = open_template("unique.sql.j2")
null_template = open_template("null.sql.j2")
zero_template = open_template("zero.sql.j2")
inf_template = open_template("inf.sql.j2")
dist_template = open_template("dist.sql.j2")
response_template = open_template("response.sql.j2")
common_template = open_template("common.sql.j2")
smallest_template = open_template("smallest.sql.j2")
largest_template = open_template("largest.sql.j2")
# basic stats from aggregate functions
agg_stats_template = open_template("agg_stats.sql.j2")
agg_stats_date_template = open_template("agg_stats_date.sql.j2")
# analytic function
boxplot_template = open_template("boxplot.sql.j2")
dist_binned_template = open_template("dist_binned.sql.j2")
response_binned_template = open_template("response_binned.sql.j2")
corr_template = open_template("corr.sql.j2")


def get_basic_stats(cur,
                    results: dict,
                    col: str,
                    n: int = 100,
                    schema: str = "marketing",
                    table: str = "test_table",
                    analytic: bool = True) -> dict:
    """Get the basic statistics for the given column.

    Needs a vertica_python cursor,
    the dictionary of results,
    and the column to be analyzed.

    If analytic is true, try to get the analytic functions.
    Will check database compat.

    Ref for column types:
    https://github.com/uber/vertica-python/blob/edd8ccba72ffdf076888a85eea43b7b11a050077/vertica_python/datatypes.py
    """

    vartype = results["type"]

    # if datetime or string, don't count zeroes
    # if vartype in ["CAT"]:
    # TODO
    if True:
        count_templates = [unique_template, null_template]
        count_template_names = ["n_unique", "n_missing"]
    elif vartype in ["DATE"]:
        count_templates = [unique_template, null_template, inf_template]
        count_template_names = ["n_unique", "n_missing", "n_infinite"]
    else:
        count_templates = [unique_template, null_template, zero_template, inf_template]
        count_template_names = ["n_unique", "n_missing", "n_zeros", "n_infinite"]

    # only use analytic functions if on Vertica
    # if analytic is passed to be true, try it
    if analytic:
        analytic = (type(cur) == vertica_python.vertica.cursor.Cursor)
    for i, t in enumerate(count_templates):
        query = t.render({"col": col,
                          "schema": schema,
                          "table": table,
                          "analytic": analytic})
        cur.execute(query)
        x = cur.fetchall()
        unique = x[0]["count"]
        results[count_template_names[i]] = unique
        results["p_" + count_template_names[i][2:]] = unique / float(n)

    query = common_template.render({"col": col, "schema": schema, "table": table, "num": 10})
    cur.execute(query)
    a = cur.fetchall()
    x = [b[col] for i, b in enumerate(a) if b[col] is not None]
    y = [b["count"] for i, b in enumerate(a) if b[col] is not None]
    results["common"] = pd.Series(y, index=x)  # [x, y]
    results["common"].replace(to_replace=[np.inf, np.NINF, np.PINF], value=np.nan,
                              inplace=True)
    # string
    if vartype in ["CONST", "UNIQUE", "IGNORE", "STRING"]:
        return results
    # datetime
    elif vartype == "DATE":
        query = agg_stats_date_template.render({"col": col,
                                                "schema": schema,
                                                "table": table,
                                                "analytic": analytic})
    else:
        query = agg_stats_template.render({"col": col,
                                           "schema": schema,
                                           "table": table,
                                           "analytic": analytic})

    cur.execute(query)
    a = cur.fetchall()
    for key in a[0].keys():
        results[key] = a[0][key]

    return results


def get_ordinal_stuff(cur,
                      results: dict,
                      col: str,
                      schema: str = "marketing",
                      table: str = "test_table") -> dict:
    """Get the ordinal stuff."""

    # sanity check that we don't run this on the primary key or something
    if results["n_unique"] > 500:
        print("Too many records to run the raw distribution!")
        return results

    query = dist_template.render({"col": col,
                                  "schema": schema,
                                  "table": table})
    cur.execute(query)
    a = cur.fetchall()
    x = [b[col] for b in a]
    y = [b["count"] for b in a]
    results["dist"] = str([x, y])

    return results


def get_continuous_stuff(cur,
                         results: dict,
                         col: str,
                         schema: str = "marketing",
                         table: str = "test_table") -> dict:
    """Get the ordinal stuff."""

    # the boxplot query works, but it's very slow compared to the others (requires sorting the column)
    # query = boxplot_template.render({"col":col,
    #                                  "schema":"marketing",
    #                                  "table":"test_table"})
    # cur.execute(query)
    # a = cur.fetchall()
    # results["percentiles"] = []
    # for percentile in [5,25,50,75,95]:
    #     results["percentiles"].append([percentile,a[0][str(percentile)]])

    query = smallest_template.render({"col": col, "schema": schema, "table": table, "num": 5})
    cur.execute(query)
    a = cur.fetchall()
    x = [b[col] for b in a]
    y = [b["count"] for b in a]
    results["smallest"] = [x, y]
    query = largest_template.render({"col": col, "schema": schema, "table": table, "num": 5})
    cur.execute(query)
    a = cur.fetchall()
    x = [b[col] for b in a]
    y = [b["count"] for b in a]
    results["largest"] = [x, y]

    if results["min"] != results["max"]:
        nbins = 50
        query = dist_binned_template.render({"col": col,
                                             "schema": schema,
                                             "table": table,
                                             "nbins": nbins,
                                             "min": results["min"],
                                             "max": results["max"]})
        cur.execute(query)
        a = cur.fetchall()
        x = [b["bucket"] for b in a]
        y = [b["count"] for b in a]
        results["dist"] = str([x, y])

    return results


def infer_coltype(col,
                  cur,
                  n: int,
                  schema: str,
                  table: str,
                  verbose: bool = False):
    """Infer col type!

    There are four checks for the column type:
    1) Look to see if it is explicit in the col name.
    If it is, done! Else:
    2a) Check for a type_code with the database.
    2b) Check the type of the variable as returned to python from database.
    If it's a date or string, done! Else, it's a number:
    3a) Check how many distinct values, decide.
    """

    if verbose:
        print("Inferring coltype for col={}".format(col))
    # infer from col name
    coltypes = {"ordinal": "ORD",
                "interval": "ORD",
                "binary": "BNRY",
                "continuous": "NUM",
                "nominal": "CAT",
                "date": "DATE",
                "passthrough": "OTH",
                "ignore": "OTH"}
    for x in coltypes:
        if x in col:
            return coltypes[x]

    # get a sample
    query = type_template.render({"col": col,
                                  "schema": schema,
                                  "table": table})
    cur.execute(query)
    x = cur.fetchall()
    if verbose:
        print(x)
        print(cur.description)
        print(cur.description[0])
        print(type(cur.description[0]))

    # use this flag to check for unique, constant, categorical within string
    str_type = False
    # infer from vertica type code
    if type(cur) == vertica_python.vertica.cursor.Cursor or type(cur.description[0]) != tuple:
        type_code = cur.description[0].type_code
        if verbose:
            print(type_code)
        if type_code in [8, 9]:
            str_type = True
        elif type_code in [10, 11, 12, 13, 14, 15]:
            return "DATE"
        # ignore booleans...
        # TODO: map boolean to binary type (map to 0/1)
        elif type_code in [5]:
            return "OTH"
    # infer from the type
    else:
        val = x[0][col]
        if verbose:
            print(type(val))
        if type(val) == str:
            str_type = True

    query = unique_template.render({"col": col,
                                    "schema": schema,
                                    "table": table})
    cur.execute(query)
    x = cur.fetchall()
    n_unique = x[0]["count"]
    # just define a local results object here...
    results = {"n_unique": n_unique}
    if results["n_unique"] == n:
        return "UNIQUE"
    elif results["n_unique"] == 1:
        return "CONST"
    # elif results["n_unique"] / float(n) < 0.5:
    #     return "NUM"
    # how to distinguish nominal and ordinal? not really a way here
    # use the col type in Vertica: strings -> nominal, numeric -> ordinal
    elif results["n_unique"] == 2:
        return "BNRY"
    elif results["n_unique"] < 500:
        return "CAT"
    elif str_type:
        return "OTH"
    else:
        return "NUM"


def get_col_stuff(cur,
                  col: str,
                  coltype: str = "",
                  table_size: int = 100,
                  schema: str = "",
                  table: str = "test_table"):
    print("Getting info for col={}".format(col))

    # first get the column type
    coltype = infer_coltype(col, cur, table_size, schema, table)
    # # map these onto something that pandas_profiling already knows
    # if coltype in ["IGNORE", "STRING"]:
    #     coltype = "UNIQUE"
    results = {"type": coltype}
    # now get basic stats
    # some branching based on the coltype in basic_stats
    # if coltype not in ["STRING", "IGNORE", "UNIQUE", "CONST"]:
    results = get_basic_stats(cur, results, col,
                              schema=schema,
                              table=table,
                              n=table_size)
    if coltype == "CAT":
        results = get_ordinal_stuff(cur, results, col, schema=schema, table=table)
    elif coltype == "NUM":
        results = get_continuous_stuff(cur, results, col, schema=schema, table=table)
    else:
        print("skipping details for col={}".format(col))
    for key in ['25%', '5%', '50%', '75%', '95%', 'count',
                'n_infinite', 'p_infinite',
                'n_unique', 'p_unique', 'is_unique',
                'n_missing', 'p_missing',
                'p_zeros',
                'freq', 'histogram', 'iqr',
                'kurtosis', 'mad', 'max', 'mean', 'min', 'mini_histogram', 'cv',
                'range', 'skewness', 'std', 'sum', 'top', 'type', 'variance', 'mode']:
        if key not in results:
            results[key] = np.nan
    return results


def test(cur):
    col = "household_size_interval"
    coltype = "ordinal"
    print(col)

    results = get_col_stuff(cur, col)
    print(results)

    col = "discretionary_spending_dollars_continuous"
    coltype = "continuous"
    print(col)

    results = get_col_stuff(cur, col)
    print(results)


def get_all_cols(cur,
                 schema: str = "",
                 table: str = "test_table") -> list:
    """Get all of the column names.

    Does this provide a reliable order?"""

    cur.execute(Template("""select *
    from
    {% if schema | length > 0 %}{{ schema }}.{% endif %}{{ table }}
    limit 1""").render({"schema": schema, "table": table}))
    dict_keys = cur.fetchall()[0].keys()
    keys = list(dict_keys)
    print(keys)
    # for sqlite, need to remove the index explicitly...
    if "index" in keys:
        keys = [x for x in dict_keys if x not in ["index"]]
        print(keys)
    return keys

# @click.command()
# @click.argument('schema', type=str)
# @click.argument('table', type=str)


def main_vertica(cur, schema, table,
                 cache_results=False):
    """
    """
    # get the size of the table
    q = count_template.render({"schema": schema,
                               "table": table})
    cur.execute(q)
    x = cur.fetchall()
    count = x[0]["count"]
    # use this when inferring col type
    print(datetime.now())

    cols = get_all_cols(cur, table=table, schema=schema)
    print(len(cols))

    print(datetime.now())
    print(table)

    fname = "data/processed/{}_{}_col_info.json".format(schema, table)
    if os.path.isfile(fname) and cache_results:
        with open(fname, "r") as f:
            all_results = json.loads(f.read())
    else:
        all_results = OrderedDict([(col,
                                    pd.Series(get_col_stuff(cur, col, schema=schema,
                                                            table_size=count,
                                                            table=table), name=col))
                                   for col in cols])
        print("Col info run complete")
        # print(all_results)

    # for i in range(len(all_results)):
    #     all_results[i]["col"] = cols[i]

    if cache_results:
        with open(fname, "w") as f:
            f.write(json.dumps(all_results, indent=4))

    return all_results

    print(datetime.now())

    print("Getting correlations")
    all_coltypes = [infer_coltype(col, result, schema=schema, table=table) for col, result in zip(cols, all_results)]
    print(all_coltypes)
    corr_cols = [col for i, col in enumerate(cols) if all_coltypes[i] in ["ordinal", "continuous"]]
    print(corr_cols)
    print(len(corr_cols))
    corr_mat = np.zeros((len(corr_cols), len(corr_cols)))
    for i, col in enumerate(corr_cols):
        print("Running correlations for col={}".format(col))
        q = corr_template.render({"cols": zip([col for j in range(len(corr_cols) - (i + 1))], corr_cols[i + 1:]),
                                  "schema": schema,
                                  "table": table})
        cur.execute(q)
        x = cur.fetchall()
        corr_mat[i + 1, :] = [y["corr_{0}".format(j + 1)] for j, y in enumerate(x)]

    print(datetime.now())
    # i = 0
    # col = corr_cols[i]
    # q = corr_template.render({"cols": zip([col for j in range(len(corr_cols)-(i+1))],corr_cols[i+1:]),
    #                           "schema": schema,
    #                           "table": table})
    # print(q)
    # cur.execute(q)
    # x = cur.fetchall()
    # print(x)
    # # corr = x[0]["corr"]
    # # print(corr)
    # # print([y["corr"] for y in x])
    # print([y["corr_{0}".format(i+1)] for i,y in enumerate(x)])
    # corr_mat[i+1,:] = [y["corr_{0}".format(i+1)] for i,y in enumerate(x)]
    # print(datetime.now())

    if cache_results:
        fname = "data/processed/{}_{}_col_corr.csv".format(schema, table)
        np.savetxt(fname, corr_mat, delimeter=",")
    return all_results


def write_var_codes(cur):
    """Use the marketing.vertica_datatypes table to lookup all of the variable codes.

    Writes out a file called `vertica_datatypes.json`."""

    cur.execute("select * from marketing.vertica_datatypes")
    x = cur.fetchall()
    print(x)
    print(cur.description)
    type_lookup = {}
    for x in cur.description:
        print(x.type_code, x.name.rstrip("_").replace("_", " ").upper())
        if x.type_code in type_lookup:
            type_lookup[x.type_code].append(x.name.rstrip("_").replace("_", " ").upper())
        else:
            type_lookup[x.type_code] = [x.name.rstrip("_").replace("_", " ").upper()]
    print(type_lookup)
    with open(os.path.join(os.path.dirname(os.path.realpath(__file__)),
                           "vertica", "vertica_datatypes.json"), "w") as f:
        f.write(json.dumps(type_lookup, indent=4))


if __name__ == "__main__":
    dotenv_success = load_dotenv(find_dotenv())

    conn_info = {"host": "vertica.private.massmutual.com",
                 "port": 5433,
                 "user": os.environ.get("user"),
                 "password": os.environ.get("pw"),
                 "database": "advana",
                 "read_timeout": 6000,
                 "unicode_error": "strict",
                 "ssl": True}

    con = get_vertica_python_conn(conn_info)
    cur = con.cursor("dict")

    # test(cur)

    # schema = sys.argv[1]
    # table = sys.argv[2]
    # main_vertica(cur, schema,table)

    # write_var_codes(cur)
