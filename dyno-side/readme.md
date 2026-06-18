### Dyno Side Topology & Components

```
DYNO Side (10V domain) (receiver / amplification) 
--------------------------------------------
RS-422 receiver (Differential input, reject noise) (AM26IS32) <- (AP2205-50W5-7) (x)
    ↓
RC low-pass  (PWM to DC voltage conversion) (x)
    ↓
Op-amp 2x Gain (Scales to 0-10V) (LM358) (x)
---------------------------------------------
                    ↓
     DYNO Controller (Analog 10V Input)
```