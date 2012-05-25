from __future__ import division
import adolpy

# Replace the math module
from adolpy import math
# Replace the builtin function (currently, only abs)
from adolpy.builtins import *


# Obviously not the best way of defining a pow function
def pow(a, exponent):
    r = 1
    for i in xrange(exponent):
        r *= a
    return r


# A weird way of expressing x**5 + x*sqrt(y), x+y
def f(x,y):
    # We can call other user defined functions
    z = pow(x,5)
    # and return more than one parameter
    return z + x*math.sqrt(y), x+y 

x,y = 3,6

print "value: ", f(x,y)

der = adolpy.derivate(f)

derivative = der(x,y)

print
print "Automatic derivatives"
for i in derivative:
    print i.dot

print "Manually computed jacobian"
print [5 * x**4 + math.sqrt(y), x/(2*math.sqrt(y))]
print [1,1]

step = 1e-5
print "Numerically computed by central differences for step=", step

print [(f(x+step,y)[0] - f(x-step,y)[0])/(2*step), (f(x,y+step)[0] - f(x, y-step)[0])/(2*step)]
print [(f(x+step,y)[1] - f(x-step,y)[1])/(2*step), (f(x,y+step)[1] - f(x, y-step)[1])/(2*step)]



print
print "Now, a function defined by parts (huber loss), delta = 3"
print "For a < delta, huber(a) = .5 * a**2"
print "For a = delta, huber(a) = .5 * a**2 == delta * (abs(a) - delta/2)"
print "For a > delta, huber(a) = delta * (abs(a) - delta/2)"
print

# Trying with closures
def huber(delta):
    def huber_loss(a):
        if abs(a) <= delta:
            return .5 * a**2
        else:
            return delta * (abs(a) - delta/2.)
    return huber_loss

delta = 3
loss = huber(delta)

huber_der = adolpy.derivate(loss)

params = [-6, -3.00001, -2.9999, 0, 2.99999, 3, 3.00001, 6]
print "Automatic derivative for a = ", params 
for a in params:
    print huber_der(a).dot[0], 
print

print "Actual derivatives: -delta if a =< -delta, a if -delta <= a <= delta, delta if a >= delta"
for a in params:
    if abs(a) < delta:
        print a,
    else:
        print a/abs(a)*delta,
print

print "Numerical derivatives, step = ", step
for a in params:
    print (loss(a+step) - loss(a-step))/(2*step),


print 
print
