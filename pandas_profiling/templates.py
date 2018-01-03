# coding=UTF-8
"""Contains all templates used for generating the HTML profile report"""

from jinja2 import Environment, PackageLoader

# Initializing Jinja
pl = PackageLoader('pandas_profiling', 'templates')
jinja2_env = Environment(lstrip_blocks=True, trim_blocks=True, loader=pl)

# Mapping between template name and file
templates = {'freq_table_row': 'freq_table_row.html',
             'mini_freq_table_row': 'mini_freq_table_row.html',
             'freq_table': 'freq_table.html',
             'mini_freq_table': 'mini_freq_table.html',
             'row_num': 'row_num.html',
             'row_date': 'row_date.html',
             'row_cat': 'row_cat.html',
             'row_bool': 'row_bool.html',
             'row_corr': 'row_corr.html',
             'row_recoded': 'row_recoded.html',
             'row_const': 'row_const.html',
             'row_unique': 'row_unique.html',
             'row_unsupported': 'row_unsupported.html',
             'overview': 'overview.html',
             'sample': 'sample.html',
             'base': 'base.html',
             'wrapper': 'wrapper.html'
             }

# Mapping between row type and var type
var_type = {'NUM': 'Numeric',
            'DATE': 'Date',
            'CAT': 'Categorical',
            'UNIQUE': 'Categorical, Unique',
            'BOOL': 'Boolean',
            'CONST': 'Constant',
            'CORR': 'Highly correlated',
            'RECODED': 'Recoded',
            'UNSUPPORTED': 'Unsupported'
            }


def template(template_name):
    """Return a jinja template ready for rendering. If needed, global variables are initialized.

    Parameters
    ----------
    template_name: str, the name of the template as defined in the templates mapping

    Returns
    -------
    The Jinja template ready for rendering
    """
    globals = None
    if template_name.startswith('row_'):
        # This is a row template setting global variable
        globals = dict()
        globals['vartype'] = var_type[template_name.split('_')[1].upper()]
    return jinja2_env.get_template(templates[template_name], globals=globals)


# mapping between row type and template name
row_templates_dict = {'NUM': template('row_num'),
                      'DATE': template('row_date'),
                      'DISCRETE': template('row_num'),
                      'CAT': template('row_cat'),
                      'BOOL': template('row_bool'),
                      'UNIQUE': template('row_unique'),
                      'CONST': template('row_const'),
                      'CORR': template('row_corr'),
                      'RECODED': template('row_recoded'),
                      'UNSUPPORTED': template('row_unsupported')
                      }

# The number of column to use in the display of the frequency table according to the category
mini_freq_table_nb_col = {'CAT': 6, 'BOOL': 3}

messages = dict()
messages['CONST'] = u'<a href="#pp_var_{0[varname]}"><code>{0[varname]}</code></a> has constant value {0[mode]} <span class="label label-primary">Rejected</span>'
messages['CORR'] = u'<a href="#pp_var_{0[varname]}"><code>{0[varname]}</code></a> is highly correlated with <a href="#pp_var_{0[correlation_var]}"><code>{0[correlation_var]}</code></a> (ρ = {0[correlation]}) <span class="label label-primary">Rejected</span>'
messages['RECODED'] = u'<a href="#pp_var_{0[varname]}"><code>{0[varname]}</code></a> is a recoding of <a href="#pp_var_{0[correlation_var]}"><code>{0[correlation_var]}</code></a> <span class="label label-primary">Rejected</span>'
messages['HIGH_CARDINALITY'] = u'<a href="#pp_var_{0[varname]}"><code>{varname}</code></a> has a high cardinality: {0[distinct_count]} distinct values  <span class="label label-warning">Warning</span>'
messages['UNSUPPORTED'] = u'<a href="#pp_var_{0[varname]}"><code>{0[varname]}</code></a> is an unsupported type, check if it needs cleaning or further analysis <span class="label label-warning">Warning</span>'
messages['n_duplicates'] = u'Dataset has {0[n_duplicates]} duplicate rows <span class="label label-warning">Warning</span>'
messages['skewness'] = u'<a href="#pp_var_{0[varname]}"><code>{varname}</code></a> is highly skewed (γ1 = {0[skewness]})  <span class="label label-info">Skewed</span>'
messages['p_missing'] = u'<a href="#pp_var_{0[varname]}"><code>{varname}</code></a> has {0[n_missing]} / {0[p_missing]} missing values <span class="label label-default">Missing</span>'
messages['p_infinite'] = u'<a href="#pp_var_{0[varname]}"><code>{varname}</code></a> has {0[n_infinite]} / {0[p_infinite]} infinite values <span class="label label-default">Infinite</span>'
messages['p_zeros'] = u'<a href="#pp_var_{0[varname]}"><code>{varname}</code></a> has {0[n_zeros]} / {0[p_zeros]} zeros <span class="label label-info">Zeros</span>'

message_row = u'<li>{message}</li>'
