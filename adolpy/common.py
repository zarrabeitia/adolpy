#    Adolpy - Algorithmic Differentiation Through Operator Overloading on 
#             Python using the Forward Method.
#
#    Copyright (C) 2008  Luis Zarrabeitia
#
#       This program is free software; you can redistribute it and/or modify
#       it under the terms of the GNU General Public License as published by
#       the Free Software Foundation; either version 3 of the License, or
#       (at your option) any later version.
#       
#       This program is distributed in the hope that it will be useful,
#       but WITHOUT ANY WARRANTY; without even the implied warranty of
#       MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#       GNU General Public License for more details.
#       
#       You should have received a copy of the GNU General Public License
#       along with this program; if not, write to the Free Software
#       Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#       MA 02110-1301, USA.


"""
Common definitions for adolmath.
"""


import math
import itertools
import operator
from itertools import izip

inf, nan = float('inf'), float('nan')
zeros = itertools.repeat(0)

class Active(object):
    """
    An active instance stores a variable's value and its derivatives
    over some directions. The basic arithmethic operations are overloaded
    with functions decorated with active_operator, so they propagate the
    values of the derivatives as well as the direct computation.
    
    Attributes:
    value: The value of the variable
    dot: A vector (list, tuple) with the value of the derivatives.    
    """
    def __init__(self, value, dot=zeros):        
        self.value = value
        self.dot = dot
    def __str__(self):
        return "Active(%s, %s)"%(self.getvalue(), self.dot)
    def __repr__(self):
        return "adolpy.Active(%s,%s)"%(self.value, self.dot)
    def __getitem__(self, slice):
        res = self
        if not isinstance(slice, tuple):
            slice = (slice,)
        for index in slice:
            res = res.dot[index]
        res = getvalue(res)
        return res
    def __float__(self):
        return float(self.getvalue())
    def __int__(self):
        return int(self.getvalue())
    def getvalue(self):
        if hasattr(self.value,"getvalue"):
            return self.value.getvalue()
        else:
            return self.value
    def __cmp__(self, other): # Warning - can only compares the values
        if isinstance(other, Active):
            other = other.value
        return cmp(self.value, other)
    def __hash__(self):
        return hash(self.value)

def getvalue(act):
    if hasattr(act,"value"):
        return getvalue(act.value)
    else:
        return act        

def active_function(module=math):
    """
    Given a function's derivative and it's name, returns an active function
    that computes both the original value and the derivative of it's argument. 
    You can pass in the original function (a callable) or the module that contains it.
    If you pass a non-callable object, the original functions is assumed to be an 
    attribute of the same name as the decorated function.
    """
    def decorator(derivative):
        name = derivative.__name__
        if hasattr(module, "__call__"):
            # It wasn't a module, it was the source function. 
            original_func = module
        else:
            original_func = getattr(module,name)
        def active_function(x):
            if not isinstance(x, Active):
                return original_func(x)
            else:
                der = derivative(x.value)
                return Active(active_function(x.value), tuple(der*dotx for dotx in x.dot))
        active_function.__doc__ = original_func.__doc__
        return active_function
    return decorator


def unpack_val_dot(x):
    if isinstance(x, Active):
        return x.value, x.dot
    else:
        return x, zeros
      
import types
def active_operator(derivative):
    name = derivative.__name__
    op = getattr(operator, name)
    def active_operation(x, y):
        xval, xdot = unpack_val_dot(x)
        yval, ydot = unpack_val_dot(y)
        return Active(op(xval, yval),
                      tuple(derivative(xval,yval, dotx, doty) for dotx, doty in izip(xdot,ydot)))
    def reverse_operation(y, x): # El mismo codigo anterior... 
        return active_operation(x, y)
    setattr(Active, "__%s__"%name, types.MethodType(active_operation, None, Active))
    setattr(Active, "__r%s__"%name, types.MethodType(reverse_operation, None, Active))
    return active_operation

