

def gradient_format(value, limit1, limit2, c1, c2):
    def LerpColour(c1,c2,t):
        return (int(c1[0]+(c2[0]-c1[0])*t),int(c1[1]+(c2[1]-c1[1])*t),int(c1[2]+(c2[2]-c1[2])*t))
    c = LerpColour(c1, c2, (value-limit1)/(limit2-limit1))
    return fmt_color(value,"rgb{}".format(str(c)))


def fmt_color(text, color):
    return('<span style="color:{color}">{text}</span>'.format(color=color,text=str(text)))

def fmt_class(text, cls):
    return('<span class="{cls}">{text}</span>'.format(cls=cls,text=str(text)))

def fmt_bytesize(num, suffix='B'):
    for unit in ['','Ki','Mi','Gi','Ti','Pi','Ei','Zi']:
        if abs(num) < 1024.0:
            return "%3.1f %s%s" % (num, unit, suffix)
        num /= 1024.0
    return "%.1f %s%s" % (num, 'Yi', suffix)

def fmt_percent(v):
    return  "{:2.1f}%".format(v*100)

formatters={
            u'freq': (lambda v: gradient_format(v, 0, 62000, (30, 198, 244), (99, 200, 72))),
         u'p_missing': lambda v: fmt_class("0%", "notimportant") if v == 0 else "{:2.1f}%".format(v*100),
        u'p_unique': fmt_percent,
        u'p_zeroes': fmt_percent ,
        u'memorysize': fmt_bytesize,
        u'total_missing': fmt_percent,
        }