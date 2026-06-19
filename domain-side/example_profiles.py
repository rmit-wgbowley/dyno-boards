"""
Filename: example_profiles.py

Description:
    Generates an example input curve with duty cycle and 
    example rpm ramp up based on the dyno's 5mv per 1 RPM
    and the 3.3v to 10v amplification.

    NOTE:
    This script does use my custom framework picounits
"""

from math import e
from picounits import VOLTAGE, MILLI


# Parameters
c=0
b=1/100
c=0

# script control
ecu_side = 3.3 * VOLTAGE
dyno_scale = 5 * MILLI * VOLTAGE

dyno_pre_amplification = dyno_scale / 2
ecu_pre_isolation = 3.3 * dyno_pre_amplification / 5

def ramp_profile(t, a, b, c):
    """ Arbitrary example function"""
    return a / (1 + e ** (-b*(t-c)))
