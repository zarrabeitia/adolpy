
import math
from math import pi, e
from common import active_function, active_operator, inf, nan, Active



@active_function(math)
def sin(x):
    return cos(x)

@active_function(math)
def cos(x):
    return -sin(x)

# first, lets redefine log, so it has a less 'exceptional' meaning
def log(x):
    if x == 0:
        return float('-inf')
    elif x < 0:
        return float('nan')
    else:
        return math.log(x)

# and now lets make it active        
@active_function(math)
def log(x):
    if not isinstance(x, Active) and x <= 0:
        return nan
    return 1/x 

@active_function(math)
def sqrt(x):
    if not isinstance(x, Active) and x <= 0:
        return nan
    return 0.5/sqrt(x)


@active_function(math)
def tan(x):
    return 1/cos(x)**2


@active_operator
def pow(x, y, dotx, doty):
    partial = y*(x**(y-1))*dotx
    if doty == 0:       # Necesario para poder derivar x**cte con x <= 0
        return partial  # ??Que tanto problema trae? ??Que pasa con las der. de segundo orden?
    else:
        return partial + (x**y)*log(x)*doty

@active_function(math)
def log10(x):
    return log10(e)/x

@active_function(math)
def exp(x):
    return exp(x)






