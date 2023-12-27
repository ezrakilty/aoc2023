#!/usr/bin/python

import math

# hold for x, run for t-x, speed is x, distance xt-x^2
# have to beat d
# looking for points where xt-x^2-d > 0
# roots of xt-x^2-d = 0 are (-b +- √(b^2 - 4ac)) / 2a
# or (-t +- √(t^2 - 4d)) / -2
# substracting one from the other, we get 
# √(b^2 - 4ac)) / a
# = √(t^2 - 4d) / -1

def low(time, distance):
    return time/2 - math.sqrt(time * time - 4 * distance)/2

def span(time, distance):
    return math.sqrt(time * time - 4 * distance)

def doit(time, distance):
    a = low(time, distance)
    s = span(time, distance)
    b = a + s
    result = math.floor(b) - math.ceil(a) - 1
    if b > math.floor(b):
        result += 1
    if a < math.ceil(a):
        result += 1
    return result