## Overview

![MIT License](https://img.shields.io/badge/License-MIT-e01e37?style=flat-square&logoColor=black)
![Electrics](https://img.shields.io/badge/Domain-Electrics-e01e37?style=flat-square&logoColor=black)

The RMIT dyno setup consists of two systems, the dyno controller and the r19e ECU. This allows for the same HV system from the car to be used, avoiding validating another system. The r19e ECU is meant to primarily control the motor and HV system; however, for this test setup it also needs to transmit a voltage that controls the dyno RPM. This allows for a lookup table to be used to ramp up the dyno RPM in an arbitrary function.

> [!NOTE]
> Analysis, schematics & boards can be found [here](ecu-side) & [here](dyno-side).


## Why communicate? 

The current dyno system uses speed control on the dyno-side and torque control on the race-car's side. This allows for a lookup table to be used to ramp up the dyno RPM to model rpm vs torque.
For example the rpm over time could be modelled as this arbitrary function,

$$RPM(t) = \frac{A}{1 + e^{-b(t-c)}}$$

And then it would simply be transformed into a simple lookup table, assuming A is the dyno's max RPM:

> [!important]
> The dyno has a much higher maximum RPM than 1000 and most likely isn't linear. This was a simple example. Check calibration curves / scaling factors.

| Step | Time ($t$ in seconds) | Target RPM | r19e ECU Output (V) | Dyno Controller Input (V) |
| :--- | :---: | :---: | :---: | :---: |
| 0 | 0.00 | 7 | 0.02 V | 0.06 V |
| 1 | 1.25 | 76 | 0.25 V | 0.75 V |
| 2 | 2.50 | 500 | 1.65 V | 4.95 V |
| 3 | 3.75 | 924 | 3.05 V | 9.15 V |
| 4 | 5.00 | 993 | 3.28 V | 9.84 V |

*Figure 1: Example profile parameters configured for a real-time 5-second window using `A = 1000`, `b = 2.0`, and `c = 2.5`. There is a 3× gain between the ECU and the dyno input.*

However for the real system, race day data is used to model the dynamic torque loading on the powertrain. 

## High-level Topology

The dyno controller and r19e ECU are approximately `2-4 meters` apart and operate at different voltage levels (`0-3.3V` vs `0-10V`). So an ECU conditioning/isolation board is used, and a dyno receiver/amplification board is used.


```
ECU PWM Source (Digital 3.3V - PB13, tim1_CHN1, STM32F405RGT6)
                    ↓

ECU Side (3.3V domain) (conditioning / isolation)
--------------------------------------------
Schmitt trigger (Cleans up the signal edge)
    ↓
Digital Isolator (Isolates the PWM signal) ← (Isolated 3.3v from dc/dc)
    ↓
RS-422 Driver (A/B differential pair)
--------------------------------------------
                    ↓

--------------------------------------------
twisted pairs: (+signal, -signal)
optional: shielded twisted for better stability
--------------------------------------------
                    ↓

DYNO Side (10V domain) (receiver / amplification) 
--------------------------------------------
RS-422 receiver (Differential input, rejects noise) ← (5V LDO)
    ↓
RC low-pass filter (100hZ)  (PWM to DC voltage conversion)
    ↓
Op-amp 2x Gain (non inverting) (Scales to 0-10V)
---------------------------------------------
                    ↓

DYNO Controller (Analog 10V Input)
```

## Documentation

All internal documentation can be found within this repo's [issues](https://github.com/rmit-wgbowley/dyno-boards/issues?q=is%3Aissue%20state%3Aclosed).
