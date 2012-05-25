An implementation of Automatic Differentiation in python.

This was part of a homework assignment at the University of Havana. We had to 
choose a programming language and implement an AD library for that language. This
was my python implementation of the forward method.

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

This project implements the the Forward method through operator overloading. Each
input variable is replaced by a tracer object (named "Active"), which records the
partial derivatives as they move through the function. Each overloaded method
must call the original implementation and perform the chain rule. To reduce the
boilerplate code (call the original implementation, then compute the derivative,
then wrap the two values into a new Active), I wrote decorators that given the
derivative function, will add the rest of the boilerplate (call the original, 
wrap in a new Active).

THIS IS A TOY PROJECT

This code is published for learning purposes. You don't want to use it for  
serious projects. I wrote it in about two days ("do you remember that the AD 
project is due this week? / Ooops..."). There are higher quality AD libraries 
out there. Adolpy is simpler to use than most of them, which may make it useful to 
illustrate AD, but it is incomplete for real problems (only a few functions from 
math and the builtin abs are supported). Most importantly, it doesn't support numpy. 
You are free to use this code (GPLv3), but I advise you to check it out if you 
want to play with AD or to illustrate AD (no compilation or installation required, 
fully usable from the ipython console), and when you decide that AD is the way to go, 
find a high quality library. Of course, if you want to improve it for any reason, 
you are more than welcomed to.

See the example.py file for examples.

== About the name "adolpy":

The professor for the AD course was Andreas Griewank: 
http://www.mathematik.hu-berlin.de/~griewank/

His course was very enjoyable, even though he was teaching in English in a 
spanish-speaking unversity. He co-authored ADOL-C, an AD package for C and C++:

http://www.coin-or.org/projects/ADOL-C.xml 

I wanted to make some reference to ADOL-C in my course presentation, and that's 
where "adolpy" comes from. Not very original... but he seemed to like it, and 
I certainly did.






