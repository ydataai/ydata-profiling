# coding=UTF-8

'''
This file contains all templates used for generating the HTML profile report
'''

#TODO: rewrite this using Jinja template language

base_html=u'''
    <meta charset="UTF-8">

    <style>

        .variablerow {
            border: 1px solid #e1e1e8;
            border-top: hidden;
            padding-top: 2em;
            padding-bottom: 1em;
        }

        .headerrow {
            border: 1px solid #e1e1e8;
            background-color: #f5f5f5;
            padding: 2em;
        }
        .namecol {
            margin-top: -1em;
        }

        .dl-horizontal dt {
            text-align: left;
            padding-right: 1em;
            white-space: normal;
        }

        .dl-horizontal dd {
            margin-left: 0;
        }

        .ignore {
            opacity: 0.4;
        }

        .container.pandas-profiling {
            max-width:975px;
        }

        .col-md-12 {
            padding-left: 2em;
        }

        .indent {
            margin-left: 1em;
        }

        /* Table example_values */
            table.example_values {
                border: 0;
            }

            .example_values th {
                border: 0;
                padding: 0 ;
                color: #555;
                font-weight: 600;
            }

            .example_values tr, .example_values td{
                border: 0;
                padding: 0;
                color: #555;
            }

        /* STATS */
            table.stats {
                border: 0;
            }

            .stats th {
                border: 0;
                padding: 0 2em 0 0;
                color: #555;
                font-weight: 600;
            }

            .stats tr {
                border: 0;
            }

            .stats tr:hover{
                text-decoration: underline;
            }

            .stats td{
                color: #555;
                padding: 1px;
                border: 0;
            }


        /* Sample table */
            table.sample {
                border: 0;
                margin-bottom: 2em;
                margin-left:1em;
            }
            .sample tr {
                border:0;
            }
            .sample td, .sample th{
                padding: 0.5em;
                white-space: nowrap;
                border: none;

            }

            .sample thead {
                border-top: 0;
                border-bottom: 2px solid #ddd;
            }

            .sample td {
                width:100%%;
            }


        /* There is no good solution available to make the divs equal height and then center ... */
            .histogram {
                margin-top: 3em;
            }
        /* Freq table */

            table.freq {
                margin-bottom: 2em;
                border: 0;
            }
            table.freq th, table.freq tr, table.freq td {
                border: 0;
                padding: 0;
            }

            .freq thead {
                font-weight: 600;
                white-space: nowrap;
                overflow: hidden;
                text-overflow: ellipsis;

            }

            td.fillremaining{
                width:auto;
                max-width: none;
            }

            td.number, th.number {
                text-align:right ;
            }

        /* Freq mini */
            .freq.mini td{
                width: 50%%;
                padding: 1px;
                font-size: 12px;

            }
            table.freq.mini {
                 width:100%%;
            }
            .freq.mini th {
                overflow: hidden;
                text-overflow: ellipsis;
                white-space: nowrap;
                max-width: 5em;
                font-weight: 400;
                text-align:right;
                padding-right: 0.5em;
            }

            .missing {
                color: #a94442;
            }
            .alert, .alert > th, .alert > td {
                color: #a94442;
            }


        /* Bars in tables */
            .freq .bar{
                float: left;
                width: 0;
                height: 100%%;
                line-height: 20px;
                color: #fff;
                text-align: center;
                background-color: #337ab7;
                border-radius: 3px;
                margin-right: 4px;
            }
            .other .bar {
                background-color: #999;
            }
            .missing .bar{
                background-color: #a94442;
            }
            .tooltip-inner {
                width: 100%%;
                white-space: nowrap;
                text-align:left;
            }

            .extrapadding{
                padding: 2em;
            }



    </style>

<div class="container pandas-profiling">
     <div class="row headerrow highlight">
            <h1>Overview</h1>
    </div>

    %(overview_html)s

    <div class="row headerrow highlight">
            <h1>Variables</h1>
    </div>

    %(rows_html)s

    <div class="row headerrow highlight">
            <h1>Sample</h1>
    </div>

    %(sample_html)s
</div>

'''

wrapper_html = u'''
<!doctype html>

<html lang="en">
<head>
  <meta charset="utf-8">

  <title>Profile report</title>
  <meta name="description" content="Profile report generated by pandas-profiling. See GitHub.">
  <meta name="author" content="pandas-profiling">
    <script src="https://ajax.googleapis.com/ajax/libs/jquery/1.11.3/jquery.min.js"></script>

    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.6/css/bootstrap.min.css"
          integrity="sha384-1q8mTJOASx8j1Au+a5WDVnPi2lkFfwwEAa8hDDdjZlpLegxhjVME1fgjWPGmkzs7" crossorigin="anonymous">
    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.6/css/bootstrap-theme.min.css"
          integrity="sha384-fLW2N01lMqjakBkx3l/M9EahuwpSfeNvV63J5ezn3uZzapT0u7EYsXMjQV+0En5r" crossorigin="anonymous">
    <script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.6/js/bootstrap.min.js" integrity="sha384-0mSbJDEHialfmuBBQP6A4Qrprq5OVfW37PRR3j5ELqxss1yVqOtnepnHVP9aJ7xS" crossorigin="anonymous"></script>
    <script>
       $(function () {
              $('[data-toggle="tooltip"]').tooltip()
        })
    </script>
</head>

<body>
    %s
</body>
</html>
'''


sample_html = u'''
    <div class="row variablerow">
        <div class="col-md-12" style="overflow:scroll; width: 100%%; overflow-y: hidden;">
                {sample_table_html}
        </div>
    </div>
'''

overview_template= u'''
    <div class="row variablerow">
        <div class="col-md-6 namecol">
            <p class="h4">Dataset info</p>
             <table class="stats" style="margin-left: 1em;" >
                        <tbody><tr><th>Number of variables</th>
                        <td>{0[nvar]}</td></tr>
                        <tr><th>Number of observations</th>
                        <td>{0[n]}</td></tr>
                        <tr><th>Total Missing (%)</th>
                        <td>{0[total_missing]}</td></tr>
                        <tr><th>Total size in memory</th>
                        <td>{0[memsize]}</td></tr>
                        <tr><th>Average record size in memory</th>
                        <td>{0[recordsize]}</td></tr>
                        </tbody></table>
        </div>
        <div class="col-md-6 namecol">
            <p class="h4">Variables types</p>
             <table class="stats" style="margin-left: 1em;">
                        <tbody><tr><th>Numeric</th>
                        <td>{0[NUM]}</td></tr>
                        <tr><th>Categorical</th>
                        <td>{0[CAT]}</td></tr>
                        <tr><th>Date</th>
                        <td>{0[DATE]}</td></tr>
                        <tr><th>Text (Unique)</th>
                        <td>{0[UNIQUE]}</td></tr>
                        <tr><th>Rejected</th>
                        <td>{0[REJECTED]}</td></tr>
                        </tbody></table>
        </div>
        <div class="col-md-12" style="padding-left: 1em;">
            <p class="h4">Warnings</p>
            <ul class="list-unstyled">{messages}</ul>
        </div>
     </div>
'''

_row_header = u'''<div class="row variablerow">
        <div class="col-md-3 namecol">
            <p class="h4">{varname}<br/><small>{vartype}</small></p>
        </div>
'''
_row_header_ignore = u'''<div class="row variablerow ignore">
        <div class="col-md-3 namecol">
            <p class="h4"><s>{varname}</s><br/><small>{vartype}</small></p>
        </div>
'''

_row_footer = u'''    </div>'''

row_templates_dict = {}
row_templates_dict['NUM'] = _row_header.format(vartype="Numeric", varname="{0[varname]}") + u'''
        <div class="col-md-6">
            <div class="row">
                <div class="col-sm-6">
                    <table class="stats ">
                        <tr><th>Distinct count</th>
                        <td>{0[distinct_count]}</td></tr>
                        <tr><th>Unique (%)</th>
                        <td>{0[p_unique]}</td></tr>
                        <tr class="{row_classes[p_missing]}"><th>Missing (%)</th>
                        <td>{0[p_missing]}</td></tr>
                        <tr class="{row_classes[p_missing]}"><th>Missing (n)</th>
                        <td>{0[n_missing]}</td></tr>
                        <tr class="{row_classes[p_infinite]}"><th>Infinite (%)</th>
                        <td>{0[p_infinite]}</td></tr>
                        <tr class="{row_classes[p_infinite]}"><th>Infinite (n)</th>
                        <td>{0[n_infinite]}</td></tr>
                    </table>

                </div>
                <div class="col-sm-6">
                    <table class="stats ">

                        <tr><th>Mean</th>
                        <td>{0[mean]}</td></tr>
                        <tr><th>Minimum</th>
                        <td>{0[min]}</td></tr>
                        <tr><th>Maximum</th>
                        <td>{0[max]}</td></tr>
                        <tr class="{row_classes[p_zeros]}"><th>Zeros (%)</th>
                        <td>{0[p_zeros]}</td></tr>
                    </table>
                </div>
            </div>
        </div>
        <div class="col-md-3 collapse in" id="minihistogram{0[varid]}">
             <img src="{0[mini_histogram]}">

        </div>
       <div class="col-md-12 text-right">
            <a role="button" data-toggle="collapse" data-target="#descriptives{0[varid]},#minihistogram{0[varid]}" aria-expanded="false" aria-controls="collapseExample">
                Toggle details
            </a>
        </div>
        <div class="row collapse col-md-12" id="descriptives{0[varid]}">
            <div class="col-sm-4">
                  <p class="h4">Quantile statistics</p>
                  <table class="stats indent">
                        <tr><th>Minimum</th>
                        <td>{0[min]}</td></tr>
                        <tr><th>5-th percentile</th>
                        <td>{0[5%]}</td></tr>
                        <tr><th>Q1</th>
                        <td>{0[25%]}</td></tr>
                        <tr><th>Median</th>
                        <td>{0[50%]}</td></tr>
                        <tr><th>Q3</th>
                        <td>{0[75%]}</td></tr>
                        <tr><th>95-th percentile</th>
                        <td>{0[95%]}</td></tr>
                        <tr><th>Maximum</th>
                        <td>{0[max]}</td></tr>
                        <tr><th>Range</th>
                        <td>{0[range]}</td></tr>
                        <tr><th>Interquartile range</th>
                        <td>{0[iqr]}</td></tr>
                  </table>
                  <p class="h4">Descriptive statistics</p>
                  <table class="stats indent">
                        <tr><th>Standard deviation</th>
                        <td>{0[std]}</td></tr>
                        <tr><th>Coef of variation</th>
                        <td>{0[cv]}</td></tr>
                        <tr><th>Kurtosis</th>
                        <td>{0[kurtosis]}</td></tr>
                        <tr><th>Mean</th>
                        <td>{0[mean]}</td></tr>
                        <tr><th>MAD</th>
                        <td>{0[mad]}</td></tr>
                        <tr class="{row_classes[skewness]}"><th>Skewness</th>
                        <td>{0[skewness]}</td></tr>
                        <tr><th>Sum</th>
                        <td>{0[sum]}</td></tr>
                        <tr><th>Variance</th>
                        <td>{0[variance]}</td></tr>
                        <tr><th>Memory size</th>
                        <td>{0[memorysize]}</td></tr>
                 </table>
            </div>
             <div class="col-sm-8 histogram">
                 <img src="{0[histogram]}">
             </div>
      </div>
''' + _row_footer

row_templates_dict['DATE'] = _row_header.format(vartype="Date", varname="{0[varname]}") + u'''
        <div class="col-sm-3">
            <table class="stats ">
                <tr><th>Distinct count</th>
                <td>{0[distinct_count]}</td></tr>
                <tr><th>Unique (%)</th>
                <td>{0[p_unique]}</td></tr>
                <tr class="{row_classes[p_missing]}"><th>Missing (%)</th>
                <td>{0[p_missing]}</td></tr>
                <tr class="{row_classes[p_missing]}"><th>Missing (n)</th>
                <td>{0[n_missing]}</td></tr>
                <tr class="{row_classes[p_infinite]}"><th>Infinite (%)</th>
                <td>{0[p_infinite]}</td></tr>
                <tr class="{row_classes[p_infinite]}"><th>Infinite (n)</th>
                <td>{0[n_infinite]}</td></tr>
            </table>
        </div>
        <div class="col-sm-6">
            <table class="stats ">
                <tr><th>Minimum</th>
                <td>{0[min]}</td></tr>
                <tr><th>Maximum</th>
                <td>{0[max]}</td></tr>
            </table>
        </div>


''' + _row_footer

row_templates_dict['DISCRETE'] = row_templates_dict['NUM']

row_templates_dict['CAT'] = _row_header.format(vartype="Categorical", varname="{0[varname]}") + u'''
       <div class="col-md-3">

            <table class="stats ">
                <tr class="{row_classes[distinct_count]}"><th>Distinct count</th>
                <td>{0[distinct_count]}</td></tr>
                <tr><th>Unique (%)</th>
                <td>{0[p_unique]}</td></tr>
                <tr class="{row_classes[p_missing]}"><th>Missing (%)</th>
                <td>{0[p_missing]}</td></tr>
                <tr class="{row_classes[p_missing]}"><th>Missing (n)</th>
                <td>{0[n_missing]}</td></tr>
                <tr class="{row_classes[p_infinite]}"><th>Infinite (%)</th>
                <td>{0[p_infinite]}</td></tr>
                <tr class="{row_classes[p_infinite]}"><th>Infinite (n)</th>
                <td>{0[n_infinite]}</td></tr>
            </table>



        </div>
         {0[minifreqtable]}

        <div class="col-md-12 text-right">
                <a role="button" data-toggle="collapse" data-target="#freqtable{0[varid]}, #minifreqtable{0[varid]}" aria-expanded="true" aria-controls="collapseExample">
                    Toggle details
                </a>
        </div>
         {0[freqtable]}
''' + _row_footer

row_templates_dict['UNIQUE'] = _row_header.format(vartype="Categorical, Unique", varname="{0[varname]}") + u'''
        <div class="col-md-3 collapse in" id="minivalues{0[varid]}">{0[firstn]}</div>
        <div class="col-md-6 collapse in" id="minivalues{0[varid]}">{0[lastn]}</div>
        <div class="col-md-12 text-right">
            <a role="button" data-toggle="collapse" data-target="#values{0[varid]},#minivalues{0[varid]}" aria-expanded="false" aria-controls="collapseExample">
                Toggle details
            </a>
        </div>
        <div class="col-md-12 collapse" id="values{0[varid]}">
            <p class="h4">First 20 values</p>
                {0[firstn_expanded]}
            <p class="h4">Last 20 values</p>
                {0[lastn_expanded]}
        </div>

''' + _row_footer

row_templates_dict['CONST'] = _row_header_ignore.format(vartype="Constant", varname="{0[varname]}") + u'''
         <div class="col-md-3">
            <p> <em>This variable is constant and should be ignored for analysis</em></p>

        </div>
        <div class="col-md-6">
            <table class="stats ">
                <tr><th>Constant value</th>
                <td>{0[mode]}</td></tr>
            </table>
        </div>
''' + _row_footer

row_templates_dict['CORR'] = _row_header_ignore.format(vartype="Highly correlated", varname="{0[varname]}") + u'''
         <div class="col-md-3">
            <p> <em>This variable is highly correlated with {0[correlation_var]} and should be ignored for analysis</em></p>

        </div>
        <div class="col-md-6">
            <table class="stats ">
                <tr><th>Correlation</th>
                <td>{0[correlation]}</td></tr>
            </table>
        </div>
''' + _row_footer

mini_freq_table = u'''
        <div class="col-md-6 collapse in"  id="minifreqtable{varid}">
            <table class="mini freq">
                {rows}
            </table>
        </div>
'''
mini_freq_table_row = u'''<tr class="{extra_class}">
                    <th>{label}</th>
                     <td>
                          <div class="bar" style="width:{width}%" data-toggle="tooltip" data-placement="right" data-html="true" data-delay=500 title="Percentage: {percentage}%">
{label_in_bar}
                          </div>{label_after_bar}
                   </td>
                </tr>
'''

freq_table = u'''

         <div class="col-md-12 collapse extrapadding" id="freqtable{varid}">
            <table class="freq table table-hover">
                <thead><tr>
                    <td class="fillremaining">Value</td>
                    <td class="number">Count</td>
                     <td class="number">Frequency (%)</td>
                    <td style="min-width:200px">&nbsp;</td>
                </tr></thead>

                {rows}
            </table>

        </div>

'''
freq_table_row = u'''
<tr class="{extra_class}">
        <td class="fillremaining">{label}</td>
        <td class="number">{count}</td>
        <td class="number">{percentage}%</td>
        <td>
            <div class="bar" style="width:{width}%">&nbsp;</div>
        </td>
</tr>
'''

messages=dict()
messages['CONST'] = u'{0[varname]} has constant value {0[mode]} <span class="label label-primary">Rejected</span>'
messages['CORR'] = u'{0[varname]} is highly correlated with {0[correlation_var]} (ρ = {0[correlation]}) <span class="label label-primary">Rejected</span>'
messages['HIGH_CARDINALITY'] = u'{varname} has a high cardinality: {0[distinct_count]} distinct values  <span class="label label-warning">Warning</span>'
messages['n_duplicates'] = u'Dataset has {0[n_duplicates]} duplicate rows <span class="label label-warning">Warning</span>'
messages['skewness'] = u'{varname} is highly skewed (γ1 = {0[skewness]})'
messages['p_missing'] = u'{varname} has {0[n_missing]} / {0[p_missing]} missing values <span class="label label-default">Missing</span>'
messages['p_infinite'] = u'{varname} has {0[n_infinite]} / {0[p_infinite]} infinite values <span class="label label-default">Infinite</span>'
messages['p_zeros'] = u'{varname} has {0[n_zeros]} / {0[p_zeros]} zeros'

message_row = u'<li>{message}</l>'
