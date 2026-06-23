### Dyno Side Topology & Components

```
Interface (RJ45) 
DYNO Side (5/10 V domain) (receiver / amplification) 
--------------------------------------------
<- (TPS7A4901 14ms start up, 0.1-0.5 Watts | r1=10kOhm & r2=33kOhm) (x)
RS-422 receiver (Differential input, reject noise) (AM26LS32AIN)
    ↓
RC low-pass  (50 Hz, 75 mV ripple) (PWM to DC voltage conversion) (x)
    ↓
Op-amp 2x Gain (Scales to 0-10V) (TLV272) (x) 
---------------------------------------------
Interface (jst xh 4 pin 2.5)

                    ↓
DYNO Controller (Analog 10V Input)
```