import codecs
from .templates import template
from .base import describePandas, describeSQL, to_html
import pandas as pd

NO_OUTPUTFILE = "pandas_profiling.no_outputfile"
DEFAULT_OUTPUTFILE = "pandas_profiling.default_outputfile"


class ProfileReport(object):
    html = ''
    file = None

    def __init__(self, df, **kwargs):

        sample = kwargs.get('sample', df.head())

        description_set = describePandas(df, **kwargs)

        self.html = to_html(sample,
                            description_set)

        self.description_set = description_set

    def get_description(self):
        return self.description_set

    def get_rejected_variables(self, threshold=0.9):
        """ return a list of variable names being rejected for high
            correlation with one of remaining variables

            Parameters:
            ----------
            threshold: float (optional)
                correlation value which is above the threshold are rejected
        """
        variable_profile = self.description_set['variables']
        return variable_profile.index[variable_profile.correlation > threshold].tolist()

    def to_file(self, outputfile=DEFAULT_OUTPUTFILE):

        if outputfile != NO_OUTPUTFILE:
            if outputfile == DEFAULT_OUTPUTFILE:
                outputfile = 'profile_' + str(hash(self)) + ".html"
            # TODO: should be done in the template
            with codecs.open(outputfile, 'w+b', encoding='utf8') as self.file:
                self.file.write(templates.template('wrapper').render(content=self.html))

    def to_html(self):
        """ return complete template as lengthy string
            for using with frameworks
        """
        return templates.template('wrapper').render(content=self.html)

    def _repr_html_(self):
        return self.html

    def __str__(self):
        return "Output written to file " + str(self.file.name)


class ProfileReportSQL(object):
    def __init__(self, cur, schema, table, **kwargs):

        sample = pd.DataFrame(cur.execute("""select * from {}.{} limit 5""".format(schema, table)).fetchall())
        # print(sample)

        description_set = describeSQL(cur, schema, table, **kwargs)

        self.html = to_html(sample,
                            description_set)

        self.description_set = description_set
