import glob
import re
import sys


def exception_exit(msg):
    t, v, tb = sys.exc_info()
    print('{}.{}: {}'.format(t.__module__, t.__name__, v), file=sys.stderr)
    sys.exit(msg)


def listglob(globs):
    l = []
    for x in globs:
        g = glob.glob(x)
        if len(g) == 0:
            sys.exit('pattern does not match any file: {}'.format(x))
        l += g
    return l


def safe_regex(x, flags):
    try:
        return re.compile(x, flags)
    except:
        exception_exit('error parsing regex: {}'.format(x))


def try_search(re, w, i):
    if re is None:
        return None
    else:
        return re.search(w, i)


def exact_match(re, w):
    m = re.match(w)
    return m is not None and m.start() == 0 and m.end() == len(w)


def try_exact_match(re, w):
    return re is not None and exact_match(re, w)


