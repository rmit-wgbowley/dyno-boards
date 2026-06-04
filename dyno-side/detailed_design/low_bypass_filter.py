"""
Filename: Low_bypass_filter.py

Description:
    Calculates the size of the capacitor and resistor to 
    ensure the cutoff frequency is meant and the rise time
    isn't too slow.
    
    Time constant -> R & C proportionally
    Cutoff frequency -> 1/R & 1/C
    Hence fixed R (reduces voltage drop), dynamic Cap
    
    NOTE:
    This script does use my custom framework picounits.
"""

from math import pi

from picounits import q, unit_validator
from picounits import KILO, FREQUENCY, TIME, RESISTANCE, CAPACITANCE


cutoff = 100 * FREQUENCY
r1 = 1 * KILO * RESISTANCE

@unit_validator(CAPACITANCE)
def calculate_cap_size(f: q) -> q:
    """ Calculates the size of the capacitor to get a nice cutoff """
    return 1 /  (2 * pi * f * r1)

@unit_validator(TIME)
def time_constant(c: q) -> q:
    """ Calculates the time constant of the system """
    return c * r1


cap = calculate_cap_size(cutoff)
time = time_constant(cap)

print(f"Resistor: {r1:.3f} & Cutoff frequency: {cutoff:.3f}")
print(f"Capacitance: {cap:.3f} | Time constant: {cap * r1:.3f}")
print(f"Rise time @ 5 steps: {cap * r1 * 5:.3f} (99.3%)")