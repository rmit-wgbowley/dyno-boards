<p align="center">
  <img src="domain-side/media/load_and_dyno_motor.png" alt="load_and_dyno_motors" style="max-width:600px;">
</p>


## Overview
![Status](https://img.shields.io/badge/Status-WIP-e01e37?style=flat-square)
![MIT License](https://img.shields.io/badge/License-MIT-FFFFFF?style=flat-square&logoColor=black)
![Electrics](https://img.shields.io/badge/Domain-Electrics-e01e37?style=flat-square&logoColor=black)
![Dyno System](https://img.shields.io/badge/System-Dyno-FFFFFF?style=flat-square&logo=speedtest)

The RMIT dyno setup consists of two systems, the dyno controller panel (DCS800) and r19e/r26 ECU. This allows for the car's powertrain system to be validated before implementation into the car. The ECU controls the motor and HV system. However, for this test setup it is also meant to transmit a `0-3.3 V @ 10 kHz` PWM signal to control the dyno RPM. This allows for a lookup table to be used to ramp up the dyno RPM in an arbitrary function.

> [!NOTE]
> ECU-side board can be found [here](ecu-side) & dyno-side board can be found [here](dyno-side).

## Why communicate? 

The 2026 dyno setup uses speed control on the dyno-side and torque control on the load motor. This allows for a lookup table to be used to ramp up the dyno RPM to model RPM vs torque. For example, the dyno-side RPM over time could be modelled as this arbitrary function:

$$ RPM(t) = \frac{A}{2B}(1-\cos(\frac{\pi t}{t_{total}})), \quad RPM(t) \in [0, dyno_{max}] $$

Where `A` is the target RPM at the load side, `B` is the gearing ratio between the dyno motor and load motor, and `t_total` is the total time to reach that requested RPM. The requested RPM then needs to be converted to duty cycle:

$$ DC(t) = (\frac{C \times RPM(t)}{2})(\frac{3.3}{5})(\frac{100}{3.3})$$
$$ DC(t) = 10C \times RPM(t), \quad DC(t) \in [0, 100]$$

And then it would simply be transformed into a simple lookup table, assuming `C` is the the dyno controller input scaling factor `(V/RPM)` after the 2× amplification stage.

> [!important]
> The dyno has a `200 kΩ` input impedance (AI1) and an analog range of `0–10 V` with a linear factor of `5 mV/RPM`. The r26 powertrain has a gearing of `1:12.81`.

| Step | Time (s) | ECU Duty Cycle (%) | Target Dyno RPM | Dyno Controller Input (V) |
| :--- | :---: | :---: | :---: | :---: |
| 0 | 0.00 | 0.00 | 0  | 0.0 |
| 1 | 0.25 | 0.26 | 5  | 0.03 |
| 2 | 0.50 | 0.98 | 20 | 0.10 |
| 3 | 0.75 | 1.95 | 39 | 0.20 |
| 4 | 1.00 | 2.93 | 59 | 0.29 |
| 5 | 1.25 | 3.64 | 73 | 0.36 |
| 6 | 1.50 | 3.90 | 78 | 0.39 |

*Figure 1: Example profile parameters configured for a real-time `1.5-second` window with time steps of `250 ms` using `A = 1000`, `B = 12.81`, and `c = 0.005`.*

> [!note]
> The program used to generate that table can be found [here](domain-side/example_profiles.py)

However, for the real system, race day data is used to model the dynamic torque loading on the load motor. 

## High-level Topology

The dyno controller and r19e ECU are approximately `2-4 meters` apart and operate at different voltage levels (`0-3.3V` vs `0-10V`). So an ECU conditioning/isolation board is used, and a dyno receiver/amplification board is used.


```
ECU PWM Source (Digital 3.3 V @ 10 kHz - PB13, tim1_CHN1, STM32F405RGT6)
                    ↓

ECU Side (3.3 V logic / 5 V domain) (conditioning / isolation)
--------------------------------------------
Schmitt trigger (Cleans up the signal edge)
    ↓
Digital Isolator (Isolates the PWM signal) ← (Isolated 5 V domain)
    ↓
RS-422 Driver (A/B differential pair)
--------------------------------------------
                    ↓

CAT 5/6 Cable
--------------------------------------------
twisted pairs: (+signal, -signal)
optional: shielded twisted for better stability
--------------------------------------------
                    ↓

DYNO Side (5/12 V domain) (receiver / amplification) 
--------------------------------------------
RS-422 receiver (Differential input, rejects noise) ← (5 V LDO)
    ↓
RC low-pass filter (50 Hz, 75 mV ripple) (PWM to DC voltage conversion)
    ↓
Op-amp 2x Gain (non inverting) (Scales to 0–10V ADC input range)
---------------------------------------------
                    ↓
DYNO Controller (Analog 10V Input)
```

> [!NOTE]
> Buck-boost converter module is used to supply the 12V on the dyno side from the dyno's 10V supply due to op-amp rail-limit (~1.5-2 V rail swing limit).

## Documentation

All internal documentation can be found within this repo's [issues](https://github.com/rmit-wgbowley/dyno-boards/issues?q=is%3Aissue%20state%3Aclosed).
