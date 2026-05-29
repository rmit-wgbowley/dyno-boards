## Overview

![MIT License](https://img.shields.io/badge/License-MIT-e01e37?style=flat-square&logoColor=black)
![Electrics](https://img.shields.io/badge/Domain-Electrics-e01e37?style=flat-square&logoColor=black)

The RMIT dyno setup consists at a high level of two systems, the dyno controller and the r19e ECU. This allows for the same HV system from the car to be used, avoiding validating another system. The r19e ECU is meant to primarily control the motor and HV system; however, for this test setup it also needs to transmit a voltage that controls the dyno RPM. This allows for a lookup table to be used to ramp up the dyno RPM in an arbitrary function.

However, the dyno controller and r19e ECU are approximately `3-4 meters` apart and operate at different voltage levels (`0-3.3V` vs `0-10V`). So an ECU conditioning board is used, and a dyno receiver/isolator is used.

## Circuit Topology

The r19e ECU sends a `0-3.3V` PWM signal to the conditioning board where it is first filtered through an RC filter to remove any line transients. Then a Schmitt trigger (74HC14) boosts the signal to `5V` while also cleaning the leading edge. The signal is then passed to the AM26LS31AC which transmits it as (+signal, -signal).

The differential signal then reaches the dyno receiver/isolator, where the differential signal is first passed through two 6n137 (one for each signal). After which, the signal is processed by the AM26LS32AC which returns a single signal that is boosted from `5V to 10V` using a UA741 and then sent to the dyno controller.

> [!note]
> To produce 5V on the dyno board, the l78050V linear regulator is used.

Analysis, schematics & boards can be found [here](ecu-side) & [here](dyno-side).

## Documentation

All internal documentation can be found within this repo's [issues](https://github.com/rmit-wgbowley/dyno-boards/issues?q=is%3Aissue%20state%3Aclosed).