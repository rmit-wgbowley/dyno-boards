### ECU-sides Topology & Components

```
ECU PWM Source (Digital 5V - PB13, tim1_CHN1, STM32F405RGT6)
                    ↓

ECU Side (5v domain) (conditioning / isolation)
--------------------------------------------
Schmitt trigger (Cleans up the signal edge) (SN74LVC1G17) (x)
    ↓
Digital Isolator (Isolates the PWM signal) (iso7720) (x) <- RFM-0505S (isolated 5v) (x)
    ↓
RS-422 Driver (A/B differential pair) (am26ls31) (x)
--------------------------------------------
                    ↓
                DYNO Side
```

