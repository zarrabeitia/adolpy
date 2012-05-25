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


import adolpy
import adolmath

def log(x):
    return adolmath.log(x)

dlog = adolpy.derivate(log)

#print log(2.0), dlog(2.0)
print repr(dlog(0)), repr(dlog(-1))
