### Dyno Side Topology & Components
Schematic available at Projects/RnD/Dynamometer Interface on Altium 365

```
DYNO Side (5/12 V domain) (receiver / amplification) 
--------------------------------------------
RS-422 receiver (Differential input, reject noise) (AM26IS32) <- (AP2205-50W5-7) (x)
    ↓
RC low-pass  (50 Hz, 75 mV ripple) (PWM to DC voltage conversion) (x)
    ↓
Op-amp 2x Gain (Scales to 0-10V) (LM358) (x)
---------------------------------------------
                    ↓
DYNO Controller (Analog 10V Input)
```