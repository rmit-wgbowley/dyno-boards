### ECU-sides Topology & Components

```
Interface (2.54mm Pitch Male Header)
ECU PWM Source (Digital 3.3 V @ 10 kHz - PB13, tim1_CHN1, STM32F405RGT6)
                    ↓
Interface (jst xh 4 pin 2.5mm)
ECU Side (3.3 V logic / 5 V domain) (conditioning / isolation)
--------------------------------------------
Schmitt trigger (Cleans up the signal edge) (SN74LVC1G17) (x)
    ↓
Digital Isolator (Isolates the PWM signal) (iso7720) (x) <- RFM-0505S (isolated 5v) (x)
    ↓
RS-422 Driver (A/B differential pair) (am26ls31) (x)
--------------------------------------------
Interface Socket (RJ45)
                    ↓

DYNO Side
```

