import re


def exception_exit(msg):
    t, v, tb = sys.exc_info()
    print('{}.{}: {}'.format(t.__module__, t.__name__, v), file=sys.stderr)
    sys.exit(msg)


def safe_regex(x, flags):
    try:
        return re.compile(x, flags)
    except:
        exception_exit('error parsing regex: {}'.format(x))
