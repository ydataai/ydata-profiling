
import codecs
from .templates import wrapper_html
from .base import describe, to_html

NO_OUTPUTFILE = "pandas_profiling.no_outputfile"
DEFAULT_OUTPUTFILE = "pandas_profiling.default_outputfile"


class ProfileReport(object):
    html = ''
    file = None

    def __init__(self, df, **kwargs):

        sample = kwargs.get('sample', df.head())

        description_set = describe(df, **kwargs)
        self.html = to_html(sample,
                            description_set)

    def to_file(self, outputfile=DEFAULT_OUTPUTFILE):

        if outputfile != NO_OUTPUTFILE:
            if outputfile == DEFAULT_OUTPUTFILE:
                outputfile = 'profile_' + str(hash(self)) + ".html"

            self.file = codecs.open(outputfile, 'w+b', encoding='utf8')
            self.file.write(wrapper_html % self.html)
            self.file.close()

    def _repr_html_(self):
        return self.html

    def __str__(self):
        return "Output written to file " + str(self.file.name)



