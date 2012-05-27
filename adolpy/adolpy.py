#!/usr/bin/python

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


from itertools import cycle, izip
import operator
from common import Active, inf, nan, zeros, active_operator                       
   
@active_operator        
def mul(x, y, dotx, doty):
    return x * doty + y * dotx 

@active_operator
def add(x, y, dotx, doty):
    return dotx + doty

@active_operator
def sub(x, y, dotx, doty):
    return dotx - doty

@active_operator
def div(x, y, dotx, doty):
    num = (y*dotx - x*doty)
    if y == 0:
        if num < 0:
            return -inf
        elif num > 0:
            return inf
        else:
            return nan
    else:
        return (y*dotx - x*doty)/(y*y)

from admath import pow


def makevar(arg, pos, dim):
    dot = [0] * dim
    dot[pos] = 1
    return Active(arg, tuple(dot))

def ensure_active(value, dim):
    if isinstance(value, Active):
        return value
    else:
        return Active(value, (0,)*dim)
        
def derivate(func, directions=None):
    """
        Returns the directional derivatives of func over the specified 
        directions: 
        F(X) = d(func(X+t*directions))/d(t) |t=0
        res(X) = F(X)*directions. 
        The default directions are the canonical base, i.e,
        the default returned function will compute the Jacobian matrix.
        
        The returned function returns a (list of, if the original function
        had multiple return values) Active instance, its .value 
        attribute contains the function evaluation at the parameters, and
        its .dot attribute contains the derivatives. This function can be
        applied multiple times to obtain higher order derivatives, wich will
        be found as "Active" instances in the .dot attributes.
        
        Examples:
        
        >>> orig_func = lambda x,y: x**2 + y         
        >>> d1 = derivate(orig_func)
        >>> directional = derivate(orig_func, directions=[(2,2)])
        >>> d2 = derivate(d1)
        >>> orig_func(9,2)
        83
        >>> d1(9,2)
        adolpy.Active(83,(18, 1))
        >>> directional(9,2)
        adolpy.Active(83,(38,))
        >>> d2(9,2)
        adolpy.Active(83,(adolpy.Active(18,(2, 0)), adolpy.Active(1,(0, 0))))             
    """
    if directions is not None:
        directions = zip(*directions) # transpose the directions.
    def derivative(*args):
        dim = len(args)
        if not directions:
            args = (makevar(arg, pos, dim) for pos,arg in enumerate(args))
        else:             
            args = (Active(arg,tuple(v)) for arg,v in izip(args,directions))
                        
        res = func(*args)
        if isinstance(res, tuple):
            res = tuple(ensure_active(r, dim) for r in res)
        else:
            res = ensure_active(res, dim)      
        return res
    return derivative

def unpack(value):
    if not isinstance(value, Active):
        return 0 # La salida no dependio de la entrada... ??Funcion por partes?
    unpacked = []

if __name__ == "__main__":
    def p(x):
        return x**2
    def testfunc(x,y):
        return p(x)+y,0
                
    funcs = testfunc, derivate(testfunc, directions=[(0,1),(1,0)]), derivate(derivate(testfunc, directions=[(2,2)]))
    for i in xrange(-1,10):
        print "x=",i        
        print "testfunc",testfunc(i,2)
        print "derivs",funcs[1](i,-2)
    
    #print funcs[1](i,2)[0]
    
        
        

