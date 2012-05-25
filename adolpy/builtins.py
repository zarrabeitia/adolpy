
from common import active_function, active_operator, inf, nan, Active

import __builtin__

@active_function(__builtin__)
def abs(x):
    if x > 0:
        return 1
    if x < 0:
        return -1
    else:
        return nan
