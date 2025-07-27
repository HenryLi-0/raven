<div align="center">
    <h2>Raven</h2>
    ![](/raven_banner.png)
</div>

---

[Raven](https://github.com/HenryLi-0/raven/) is an open source spinning LED light display (like a disco party light of sorts), built for Hack Club's [Highway](https://highway.hackclub.com/)! 



## Introduction
Since being introduced to an LED strip during FRC at the start of 2024, I realized I really like LEDs. Like a little too much. This could also be seen with the 10 LEDs from my [Hackpad](https://github.com/hackclub/hackpad/pull/224) back in October 2024 and when I brought it on a robotics trip to BattleCry in June 2025 (iykyk). Simply, I kinda like LEDs a lot. 

Now inspired by the lights at the venue of the aforementioned robotics trip (and the lights show that occured near the end of the event), that brings us here! Introducting Raven, a spinning LED display that uses 50 LEDs spread across 5 panels, spinning *really* fast. Using a Hall Effect Sensor for speed measurement, the measured values for angular prediction, and wireless control for wireless communications, Raven is capable of producing sector-based effects, rainbow gradients, strobes, and more, with a full 360 degree range of the room, or any sector of it! This project took over a hundred hours to make (with tons of redesigns!), and, retrospectively, I guess it's just because I think LEDs look pretty cool. The idea of replicating what happened in the venue really kept me going, and, now staring at what's been created, I think those hours were worth it.


## More Pictures!



## Directory

Wanna know more? Here's some quick places to get started!

- [CAD](</CAD/README.md>)
    - We used OnShape for this, but you can grab files here too! (Although, poking around the CAD is probably better to have an idea of what things look like!)
- [PCB](</PCB/README.md>)
    - We have three different PCBs, have a look at them! They were created in KiCad v8.0.8 (yeah I know I'm a whole major version behind.)
- [Firmware](</firmware/README.md>)
    - We have two firmwares, one for each subsystem! (These firmwares are written for CircuitPython! Look here for deeper instructions!)
- [Journal](</JOURNAL.md>)
    - Wanna know the thought process behind stuff? Or just a really long read? Check out the journal! (or the [`updatelogs`](/updatelogs/) for everything in different files...)
- [BOM](</BOM.csv>)
    - Wanna make your own copy of Raven? Here's the BOM in CSV format! (You can look at [`BOM.md`](</BOM.md>) for a markdown version of it, but it won't be too descriptive!) (Or just scroll down.)



## BOM
*The Bill of Materials for x1 unit of Raven!*

Note: For this list, the prices are as of July 2025. Depending on certain actions on certain people, this may fluctuate over the next couple months/years. Additionally, the price listed will be the one of the **ABSOLUTE WORST** case scenario, for instance, a coupon or deal not going through. Therefore, the total price listed is likely higher than the amount it actually costs. To see how much it actually cost (shipping and tax included), look out for `updatelogs` during construction time! Things will be grouped up by source and bolded with the sum of all the prices under group. Stuff in italics are added up in the bolded prices, so don't count it twice!

### Structure
*structural bits*

| Part                          | Price         | Link          |
|-------------------------------|---------------|---------------|
| **STRUCTURAL ALIEXPRESS**     | **$22.75**    | AliExpress    |
| *M4 Screws (x20, 40mm)*       | *$2.85*       | [AliExpress](https://www.aliexpress.us/item/3256804341271555.html) |
| *M4 Screws (x20, 30mm)*       | *$2.49*       | ^^^           |
| *M4 Screws (x80, 16mm)*       | *$7.96*       | ^^^           |
| *M4 Nuts (x125)*              | *$9.45*       | [AliExpress](https://www.aliexpress.us/item/3256807407546447.html) |
| *Shipping (to NYC)*           | *$0.00*       | (AliExpress)  |
| **3D Printed Parts**          | **$0.00**     | (self print)  |


### PCBs
*pcbs*

| Part                          | Price         | Link          |
|-------------------------------|---------------|---------------|
| **ALL PCBS FROM JLCPCB**      | **$20.30**    | JLCPCB        |
| *LED Panels (min 5)*          | *$2.10*       | ^^^           |
| *LED Subsystem (min 5)*       | *$4.00*       | ^^^           |
| *Motor Subsystem (min 5)*     | *$4.00*       | ^^^           |
| *Shipping (to NYC)*           | *$10.20*      | ^^^           |


### Small Electronics
*small stuff like microcontrollers and resistors*

| Part                          | Price         | Link          |
|-------------------------------|---------------|---------------|
| **ALL MICROCONTROLLERS**      | **$19.00**    | [Seeed Studio](https://www.seeedstudio.com/Seeed-XIAO-ESP32C3-p-5431.html) |
| *XIAO ESP32-C3 (x2)*          | *$10.00*      | ^^^           |
| *Shipping (to NYC)*           | ~*$9.00*      | ^^^           | (need to find better options)
| **LCSC Parts**                | **$21.29**    | LCSC          |
| *A3144 (min 5)*               | *$1.18*       | [LCSC](https://lcsc.com/product-detail/Hall-Switches_JSMSEMI-A3144EUA-T-JSM_C18188954.html) |
| *30SQ045 (x3)*                | *$1.76*       | [LCSC](https://lcsc.com/product-detail/Schottky-Diodes_LGE-30SQ045_C2903878.html) |
| *WS2812B (x65, mul 5)*        | *$4.28*       | [LCSC](https://lcsc.com/product-detail/RGB-LEDs-Built-in-IC_Worldsemi-WS2812B-B-W_C114586.html) |
| *1N4148 (x2, min 20)*         | *$0.51*       | [LCSC](https://lcsc.com/product-detail/Switching-Diodes_onsemi-1N4148_C258182.html) |
| *PR01000101002JA100 (min 5)*  | *$0.60*       | [LCSC](https://lcsc.com/product-detail/Through-Hole-Resistors_VISHAY-PR01000101002JA100_C1366567.html) |
| *MF1W-100Ω±1% T (min 10)*     | *$0.45*       | [LCSC](https://lcsc.com/product-detail/Through-Hole-Resistors_CCO-Chian-Chia-Elec-MF1W-100-1-T_C119469.html) |
| *1N5822 (x2, min 5)*          | *$0.51*       | [LCSC](https://lcsc.com/product-detail/Schottky-Diodes_MDD-Microdiode-Semiconductor-1N5822_C2476.html) |
| *Handling Fee*                | *$3.00*       | LCSC          |
| *Shipping (to NYC)*           | ~*$9.00*      | LCSC          |


### Big Electronics
*big stuff like motors and batteries*

Note: Try to use the AliExpress Welcome Deal on the 775 Motor and take advantage of a current sale on the batteries (drops all the batteries down to ~$26, including shipping and taxes)! (Batteries are currently calulated with the discount.)

| Part                          | Price         | Link          |
|-------------------------------|---------------|---------------|
| **ELECTRICAL ALIEXPRESS**     | **$40.18**    | AliExpress    |
| *775 Motor (288W, 12k)*       | *$17.65*      | [AliExpress](https://www.aliexpress.us/item/3256807114067845.html) |
| *Overdischarge (1S 16A)*      | *$1.26*       | [AliExpress](https://www.aliexpress.us/item/3256805852468677.html) |
| *Overdischarge (4S 20A std.)* | *$5.89*       | [AliExpress](https://www.aliexpress.us/item/3256806720463818.html) |
| *LM2596 (x1, Step Down)*      | *$1.76*       | [AliExpress](https://www.aliexpress.us/item/3256805963034065.html) |
| *XL6019 (x1, Step Up)*        | *$2.04*       | [AliExpress](https://www.aliexpress.us/item/2255800011462620.html) |
| *TP4056 (x5, USB-C, safety)*  | *$2.70*       | [AliExpress](https://www.aliexpress.us/item/3256807959506419.html) |
| *22 AWG wire (5m, 1 roll)*    | *$2.02*       | [AliExpress](https://www.aliexpress.us/item/3256807263561521.html) |
| *10 AWG wire (1m, Black)*     | *$6.86*       | [AliExpress](https://www.aliexpress.us/item/3256807572728671.html) |
| *Shipping (to NYC)*           | *$0.00*       | (AliExpress)  |
| **BATTERIES**                 | **$26.23**    | IMR Batteries |
| *Samsung 25R 18650...*        | *$15.00*      | [IMR Batteries](https://imrbatteries.com/products/samsung-25r-18650-2500mah-20a-battery) |
| *Shipping (to NYC)*           | *$9.13*       | ^^^           |
| *Taxes*                       | *$2.07*       | ^^^           |


### Total
*a + b = c*

| Group                         | Price         |
|-------------------------------|---------------|
| STRUCTURAL ALIEXPRESS         | $22.75        |
| 3D Printed Parts              | $0            |
| ALL PCBS FROM JLCPCB          | $20.30        |
| ALL MICROCONTROLLERS          | $19.00        |
| LCSC Parts                    | $21.29        |
| ELECTRICAL ALIEXPRESS         | $40.18        |
| BATTERIES                     | $26.23        |
| BUFFER                        | $5.00         |
| **TOTAL**                     | **$154.75**   |
