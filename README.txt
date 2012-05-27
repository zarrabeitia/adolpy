An implementation of Automatic Differentiation in python.

BACKGROUND
==========

Briefly, Automatic (or Algorithmic) Differention are techniques to obtain the
"symbolic" derivative of a piece of source code, i.e, given the code of a 
function, produce a function that will compute the exact derivative (up to
rounding and truncation errors) of the original function. Commonly used 
alternatives to AD are numerical differentiation (through finite differences), 
which is ill-conditioned and subject to catastrophic cancellation, and symbolic
differentiation, which requires the algebraic expression of the function and is 
unpractical for large problems.

AD does its black magic by tracing the execution of the target function, analyzing
each transformation of the input values all the way to the outputs. In the 
"forward" method, each operation is replaced by the chain rule, such that both
the value and the derivative are computed simultaneously. In the "backward" 
method, each operation is used to build the expression tree relating each
output with each input variable.

This project implements the the Forward method through operator overloading. 
Tracer objects, called "Active"s in this implementation, are used to trace the 
execution of the function for a given input and store the partial derivatives
at each step. Routines used by the target function must be prepared to deal
with Active objects. Currently, "activated" versions for some of the functions 
in math.* and the builtin abs(x) function are supplied in the modules 
adolpy.admath and adolpy.builtins, respectively.

INSTALLATION INSTRUCTIONS
=========================

1) Check out the source code.
2) Place the adolpy directory in your PYTHONPATH.

OR

1) pip install -e git+https://github.com/zarrabeitia/adolpy.git#egg=adolpy

USAGE (BASIC)
=============

Define your target function as you normally would, using the adolpy functions 
instead of the builtin math / __builtins__. You can call extra functions, as long 
as they are "activated". You can also use conditionals, closures and loops.

    >>> from __future__ import division # Always a good thing to do
    >>> import adolpy
    >>> from adolpy import admath as math
    >>> from adolpy.builtins import *

    >>> def myfunction(a, b, c, d):
    ...     r1 = a*b + c*d
    ...     z = 1
    ...     for i in xrange(5):
    ...         z *= a
    ...     r2 = z + d/c + math.cos(d)
    ...     return r1, r2 # and so on ...

To evaluate the function, proceed as usual:

    >>> r1, r2 = myfunction(1, 2, 3, 4)
    >>> print r1, r2
    14 1.34635637914

To evaluate the derivatives, use the adolpy.derivate method:

    >>> derivative = adolpy.derivate(myfunction)

    >>> a1, a2 = derivative(1, 2, 3, 4)

The return values of the derivative are "Active" (tracer) objects.
Active.value contains the value of the function at its input, 
Active.dot contains the gradient vector.

    >>> print a1.value  # r1 = myfunction(1, 2, 3, 4)[0]
    14
    >>> print a2.value  # r2 = myfunction(1, 2, 3, 4)[1]
    1.34635637914
    >>> print a1.dot    # Gradient of r1: [dr1/da, dr1/db, dr1/dc, dr1/dd] (1, 2, 3, 4)
    (2, 1, 4, 3)
    >>> print a2.dot    # Gradient of r2: [dr2/da, dr2/db, dr2/dc, dr2/dd] (1, 2, 3, 4)
    (5.0, 0.0, -1.0, 0.7568024953079282)

The "derivative" wrapper is designed for multivariate functions. It will, of course,
work for univariate functions, but the returned Active will always contain a gradient
vector for API consistency, i.e,

    >>> import adolpy
    >>> def f(x):
    ...     return x**2

    >>> df = adolpy.derivate(f)
    >>> a = df(5)
    >>> print a.value
    25
    >>> print a.dot
    (10,)
    >>> print a.dot[0]
    10

You can compute higher order derivatives by repeatedly applying the adolpy.derivate 
transformation, with a higher computational cost (both cpu and memory), and
a more complex return value. For higher order derivatives, it is probably better to
use the backwards method (not implemented by this library)

    >>> ddf = adolpy.derivate(df)
    >>> dddf = adolpy.derivate(ddf)
    >>> a = dddf(5)
    >>> print a
    Active(25, (adolpy.Active(Active(10, (2,)),(adolpy.Active(2,(0.0,)),)),))
    >>> print a.value.value.value   # f(5)
    25
    >>> print a.value.value.dot[0]  # f'(5)
    10
    >>> print a.value.dot[0].dot[0] # f''(5)
    2
    >>> print a.dot[0].dot[0].dot[0] # f'''(5)
    0.0

It is therefore not advisable to compute higher order derivatives with the current
implementation.

See the example.py file for examples.

Usage (Advanced: activating new functions)
------------------------------------------

All functions directly or indirectly used by the target function must be "activated".
To activate a function means to rewrite it, such that it accepts an Active instance,
and returns a new Active containing the value of the function and the partial 
derivatives (as obtained by applying the chain rule).
Due to python's dynamic nature, no extra work is required to activate most pure python
functions. However, native functions can't process Active objects, and thus, they must
be activated manually.

    >>> import __builtin__
    >>> from __builtin__ import abs # Using the non-activated "abs(x)" function
    >>> def g(x):
    ...     return abs(x)
    >>> print adolpy.derivate(g)(5)
    Traceback (most recent call last):
        ...
    TypeError: bad operand type for abs(): 'Active'

    >>> from adolpy.common import Active, nan
    >>> def abs(x):
    ...     """ Active version of __builtin__.abs(x) """
    ...     if not isinstance(x, Active):
    ...         # No derivatives were requested,
    ...         # pass it through to the original function
    ...         return __builtin__.abs(x)
    ...     else:
    ...         # Compute the derivative. If undefined, use NaN
    ...         if x < 0:
    ...             der = -1
    ...         elif x > 0:
    ...             der = 1
    ...         else:
    ...             der = nan
    ...         # Apply the chain rule and return the new active
    ...         return Active(abs(x.value), tuple(der*dotx for dotx in x.dot))    

Now you can use the new function:

    >>> print adolpy.derivate(g)(5).dot[0]
    1

However, explicitly writing the active overload is cumbersome: the boilerplate code for
applying the chain rule, evaluating the original function and returning the new Active
value is independent of the function being activated. Only the section to compute the 
derivative depends on the target function. For univariate functions, Adolpy provides a
decorator to simplify function activation:

    >>> from adolpy.common import active_function, nan
    >>> @active_function(__builtin__.abs)
    ... def abs(x):
    ...     """ Active version of __builtin__.abs """
    ...     # We only need to define the derivative, the decorator takes care of the rest
    ...     if x < 0:
    ...         return -1
    ...     if x > 0:
    ...         return 1
    ...     return nan

    >>> print adolpy.derivate(g)(5).dot[0]
    1


LIMITATIONS
===========

THIS IS A TOY PROJECT

This project was the final assignment for an Active Differentiation course I took
several years ago. I believe the interfaces are very simple, compared to other AD 
packages, which makes it a good choice for learning/teaching what AD is and for 
simple projects.

However, it has serious limitations, most importantly, numpy is not supported at
all (and I don't know if it can even be supported with the current design). It is
also not particularily optimized. I don't recommend it for big problems. You are,
of course, welcomed to use it (GPLv3) and contribute back any improvements.

For serious projects, I suggest you use a higher quality AD library. In particular,
if you are interested on solving non-linear least squares problems, check out 
Google's Ceres solver at http://code.google.com/p/ceres-solver/, which also includes
an AD module. A list of AD libraries can be found at 
http://en.wikipedia.org/wiki/Automatic_differentiation

ACKNOWLEDGMENTS (and the reason for the name "adolpy")
======================================================

The AD course that gave rise to this project was taught by Professor Andreas Griewank
(http://www.mathematik.hu-berlin.de/~griewank/) at the University of Havana 
(http://www.uh.cu). His course was very enjoyable, even though he was teaching in
English at a spanish-speaking university. Thank you, professor Griewank.

He also co-authored ADOL-C, an AD package for C and C++:
http://www.coin-or.org/projects/ADOL-C.xml

When I was preparing the final presentation, I wanted to give tribute to professor
Griewank's work, so I used the name "adolpy". Not very original... but he seemed 
to like it, and I certainly did.


