import codecs

from six import text_type

from .base import describe, to_html
from .templates import template

NO_OUTPUTFILE = "pandas_profiling.no_outputfile"
DEFAULT_OUTPUTFILE = "pandas_profiling.default_outputfile"


class ProfileReport(object):
    html = ''
    file = None

    def __init__(self, df, mixed_columns_strategy='raise', **kwargs):
        """

        Parameters
        ----------
        df: pandas.DataFrame
            Dataframe for analysis
        mixed_columns_strategy: str
            Strategy on working with columns containing unorderable mixed data types.
            Acceptable values are  `raise`, `exclude`, `cast`.
            `raise` raises a TypeError if unorderable mixed data types are detected.
            `exclude` removes the columns with unorderable mixed data types.
            `cast` transform all of them to base string type.

        kwargs

        Returns
        -------

        """

        df = self.check_mixed_columns(df, strategy=mixed_columns_strategy)
        sample = kwargs.get('sample', df.head())

        description_set = describe(df, **kwargs)

        self.html = to_html(sample,
                            description_set)

        self.description_set = description_set

    def check_mixed_columns(self, df, strategy):
        for k in df.keys():
            try:
                df[k].sort_values()
            except TypeError:
                if strategy == 'raise':
                    raise TypeError(
                        'Report can not be generated with mixed type values within the column {}. Change the `mixed_columns_strategy` param or transform the column data into orderable type'.format(
                            k))
                elif strategy == 'exclude':
                    df.pop(k)
                elif strategy == 'cast':
                    df[k] = df[k].apply(text_type)
                else:
                    raise ValueError('Invalid `mixed_columns_strategy` parameter. Choose one of options: `raise`, `exclude`, `cast`')
        return df

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

    def _repr_html_(self):
        return self.html

    def __str__(self):
        return "Output written to file " + str(self.file.name)
