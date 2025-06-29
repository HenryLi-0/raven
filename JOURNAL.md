---
title: "Raven"
author: "HenryLi-0"
description: "An open source sticker machine, requiring only everyday items!"
created_at: "2025-06-25"
---

# Raven

*Note: This is the accumulated (and condensed) version of the documenting and logging I typically do! Check out [the repository](https://github.com/HenryLi-0/raven) for [more organized files and full logs](</updatelogs/>)!*

## 06-24-2025: Day 0: Or Day One? Who knows!
**Setup!**

Nothing much today, just simple repository setup and a silly idea! In fact, the silly idea came a bit before and is a little fleshed out, but it's time to actually start progress on this!

**Total time spent: 0.5 hrs**

## 06-25-2025: Day 1: The Idea! On paper!
**So what's this raven thing? Is it like some bird...?**

anyways, raven! what is it? well basically...

imagine 49 LEDs, or 50. now, imagine it spinning. like really fast. what does that do? it lets us flash sections of the room with specfic light patterns, so that we can "color" parts of the room different colors! imagine the left side of a room red, and the right side blue. but we need accurate measurements of the position, don't we? yes, but an encoders and beambreaks are too expensive, for the price we're aiming for! instead, we'll detect the peak (or rising, who knows, thats for the future programming me to fix) of the sensor, then measure RPM that way! we can model and predict the future RPM, then sequence the LEDs to flash a pattern when it is thinks it's at the right position! The code should be able to run really fast, which should allow for accurate timings!

(yes, i spent quite a while debating with omniscient chatbots about the best way to approach this and it's pretty satisfied with this idea!)

And yeah, that allows for super cool lights! see ya next time!

**Total time spent: 1 hrs**

## 06-26-2025: Day 2: The Refined Idea!
**Tests! As in, not exams!**

ok, so we're back! so, did a couple tests today...

**Test 1!**

firstly (sorry, this first one has no pictures), how fast do the LEDs have to flash before I can't see them changing? Turns out, around a wait time of `0.01` seconds was roughly the point where the colors seemed to start to seamlessly merge! Here's the example code:

```
import board
import neopixel
import time

led = board.D6
pixels = neopixel.NeoPixel(led, 9)
buffer = lambda ie: [ie for i in range(9)]

t = 0
while True:
    pixels[:] = buffer((255,0,0)) if t % 2 == 0 else buffer((0,0,255))
    t += 1
    time.sleep(0.01)
```

and after tuning the last line, we start to see purple! of course, the LEDs are still flashing the correct colors, as can be told by the fact that they are always red or blue when it "pauses" when you save firmware onto it. this means that, neopixels can, in fact, blend colors through pulsing colors faster than human detection! of course, we can't exactly test how fast they can update, but i do have an idea for later.

**Test 2!**

but now, a problem seems apparent. since we're spinning it round and round, for a certain period of time, one side does not recieve any light. basically, it acts sort of like PWM (you know, pulse width modulation), a strategy where "flickering" a device (such as an LED) is used to safely create an effect of percentage (so a half bright LED is powered 50% of the time). search it up, it'll explain better!

simply, we have to look at the effects of reduced light on the total brightness! of course, there is obviously an effect, but here's a comparison (LED flickering at max speed)

![waw](</updatelogs/images/202506/06262025 - 1.png>)

no difference? try looking at the top right of each photo! the camera seems to catch the right photo with a bit more light! simply, the effect in person wasn't too much, it was noticably dimmer, but this shouldnt be an issue once we have nearly x5 the LEDs we currently have (49 outwards LEDs is crazy!)

and yeah, so interesting tests today! i'll be pretty busy tomorrow, but the plan is to find specifics (motor power, good motor speeds, battery stuff, etc.)! also, yes, i used my hackpad for this! ok, that's all for today, good night!

**Total time spent: 2 hrs**

## 06-27-2025: Day 3: Really Refining The Idea!
**What in the chemistry?**

so i havent check the slack in a while, an i really want to do the poster thing (looks pretty cool!), so we need to get this in by 6/29/2025, or at least the poster, to my understanding. ok, so whats on the todo list?

- parts and materials
    - motors
    - batteries
- placement
    - LED PCB
    - weight distribution (and ability to tune it in the future)
    - safety shell (since, its kinda spinning really fast)
- firmware
    - timing and stuff
    - calculations for light flow
    - figure out bluetooth stuff
- editor
    - figure out how to make this easily editable
        - might use a text file (probably shouldnt make a tape clone for this)
    - figure out how to store this data (and load it onto the microcontroller)

so yeah, lots of things to do! in like, three days!

yeah so now its 10:30 PM at night and i havent done like anything, so i guess time to turn on some music and start hackin! (had to take a blood test thing today, flowed much better than last year! anyways, back to this!)

1. the diameter (and display ig)
    - in order to have a spinning wheel of ~~death~~ LEDs be effective in actually showing light in sections of the room, we have to take into account the size of the LED "panel" (like, the physical dimensions of the LED matrix)!
    - for the rest of this point, ill take about the diameter, NOT the radius!
    - $>30 cm$ is a little sus, since at that point it could get hard to control, as it seems a little large for a small motor to handle. additionally, that's like... the size of like a large plate. like its kinda big.
    - $<15 cm$ might be a bit tiny, which would make attaching our panel a little silly (and we need to make a case anyways, so it wouldnt really work?)
    - but first, we need to note the PCB? since, of course, the necessary raidus really depends on the distance between the LEDs and thus the size of the PCB!
        - neopixels have a $120\degree$ beam angle, which is *kinda* really wide for our purposes (tons of overlap between LEDs!)
        - this means that things WILL blend, which is *really* bad for our purposes (we want to be able to cleanly split sections of the room!)
        - ideally, we need the LEDs to have like $10\degree$ of spread, or *less*, which means we probably need to do something with lenses, cones, and walls
        - so, how? probably block walls on the side that slope inwards. but wastes tons of light! so next idea...
        - TALL PCB! instead of a 7x7 matrix, a 2x25 matrix with this inwards slope would be MUCH better, as it's way less obstructive. but unfortunately, thats TALL. like, if we smack each LED next to each other, each one is like 0.5cm, thats 25 cm tall, which would be really not compact
        - it would be way better to split it into 5 pcb, so its portable, and we also utilize all the PCBs JLCPCB sends over, so we're also not wasting things! that makes it roughly 5-7cm per side! it also lets us increase exposure time for each side, so the lighting should be the same! (less lights, but more times exposed per revolution)
        - so whats the PCB size? dunno. like 1 cm wide per segment, with walls that can be tuned in the future!
    - so, in conclusion, i have no clue. through some experiments involving using a single LED on my hackpad to see the effects (sorry no pictures, i was kinda using both hands at once), it seems that this angle for the walls probably will have to be tuned in the future!
    - just played around surrounding my macropad with filament boxes and learned this: light likes to spread. like alot. at least when it coems to these LEDs. (see photo below!)
    - so what did we determine? nothing, but we learned a lot! so for now, roughly $25 cm$ seems like a reasonable diameter, so let's stick with that until we get more things understood!

![lights!](</updatelogs/images/202506/06272025 - 1.png>)

2. balance
    - the LED PCB will have to be balanced, but the heaviest thing (other than the motor likely), are the batteries! we aim for wireless, since we cant exactly tether it when its spinning really fast. well, you could use a slip ring, but thats not exactly inside budget.

3. positioning
    - we plan on using a hall effect sensor for stuff, since we're going fast enough anyways! additionally, its cheap! since we're assuming a $25 cm$ diameter, we should use some wires to connect it to a placement near the center. this is because we REALLY want to clear out the noise that could occur when its near stuff!
    - since we're using bluetooth, is making the microcontroller spin gonna cause issues? in theory... no? but we'll try to keep it close to the center of the PCB, of course only to a certain extent!
    - of course motor in the center, battery to offset weight, the COG near the center bottom
    - we'll have locations where we can attach weights (sand ig? or like liquid glue? idk) and tune our system!
    - to figure anything else out, WE NEED PARTS!!!
    - ~~for the safety shell, say hello to my buddy plastic wrap~~ (this is for future concern!)

4. code
    - firmware and control algorithms should be hopefully written tomorrow?
    - editor is kinda a future thing at this point, since its kinda a LOT, and kinda depends on how the system acts! (after microcontroller firmware)

5. conclusion
    - we need part specifics!
    - we need a design!
    - we need code!

so, narrowed down our focus today, so we'll hopefully get things up and running tomorrow! first will be PCB design! here's my plan for BOM

| Item                   | Price  (USD) |
|------------------------|--------------|
| Microcontroller        |   $ 5 -  7   |
| Motor                  |   $10 - 15   |
| PCBs (both)            |   $ 8 - 12   |
| LEDs (all)             |   $ 3 -  5   |
| Sensors/Wires          |   $ 2 -  5   |
| Printed Parts          |   $ 0 -  0   |
| Shell ~~plastic wrap~~ |   $ 0 -  0   |
| Total                  |   $28 - 44   |

so, we should be able to stay within our budget! of course, those $6 might be used in random stuff as we flesh out our exact parts, but thats decent headroom! Turns out... I already have an idea for the microcontroller!

The [seeedstudio XIAO ESP32-C3](https://www.seeedstudio.com/Seeed-XIAO-ESP32C3-p-5431.html), including bluetooth and wifi capabilities, with other specs being actually kinda bettter than the XIAO RP2040! best yet, its only $5, within the budget!

before i look at a bunch of memes before sleeping tonight, ill do some research with motors! ideally, pretty light, can achieve 1k-3k RPM, (so like 16-50 rotations per second)! of course, we should aim to make the spinning part as light as possible, but we'll see! ok, see ya tomorrow! good night! (also, i wanna draw some art for this release... might not come out in time, who knows!)

**Time spent today: 2.5 hours**

## 06-28-2025: Day 4: Parts Finding and Start PCB!
**Pathfinding? FRC Reference?**

back again! its 3 PM on saturday! first thing: part search! we need:

- Microcontroller
- LEDs
- Battery stuff
    - Battery itself
    - Charging bits
    - Buck convertors or anything
- Motor
- Materials (for parts and stuff)
- Hall Effect Sensor
    - (and magnet!)
- Jumper Wires

also, not related, but new ivycomb album!!!!! anyways, im gonna listen to it in the background while searching for parts! (so far, sounding really good!)

after reviewing the project guidelines, i *think* this could really be a 6 point project, with up to $150 in funding, but i'll realistically aim to keep it less than $50 (or $100) if i can, since if i break any parts, i should be able to get them myself without going too broke! realistically, shipping may cause us to poke a little bit above (ahem ahem, certain person, ahem), but yeah

- Microcontroller:
    - SeeedStudio XIAO ESP32-C3: as said yesterday, fills features nicely!
        - SeeedStudio: [yippee](https://www.seeedstudio.com/Seeed-XIAO-ESP32C3-p-5431.html)
        - Firmware: [circuitpython is amazing!](https://circuitpython.org/board/seeed_xiao_esp32c3/)
- LEDs
    - WS2812B (Neopixels): classic led, pretty efficient (60 mA draw, worse case (20 mA is more realistic))
        - Digikey: aint no way that 50 neopixels are $34
        - AliExpress: [wow they sell individual leds? gotta do a little background check first](https://www.aliexpress.us/item/2251832590417125.html?spm=a2g0o.productlist.main.32.600a5d3b1yP1iM&algo_pvid=c5f6ef35-37ce-4857-bcf3-4a71905f647e&algo_exp_id=c5f6ef35-37ce-4857-bcf3-4a71905f647e-32&pdp_ext_f=%7B%22order%22%3A%2238%22%2C%22eval%22%3A%221%22%7D&pdp_npi=4%40dis%21USD%215.89%213.53%21%21%215.89%213.53%21%402101e7f617511386739062844eafa4%2112000035383967669%21sea%21US%216405565024%21ABX&curPageLogUid=oTkc8tOCmXek&utparam-url=scene%3Asearch%7Cquery_from%3A)
            - sketchy, might need to buy an LED strip and just steal the neopixels from there
- Battery Itself
    - Samsung INR18650-25R: seems to be good, hold charge for a while
        - im trying not to get scammed by some sketchy companies
        - IMR Batteries: [seems legit from what ive seen?](https://imrbatteries.com/products/samsung-25r-18650-2500mah-20a-battery?_pos=1&_sid=150b0caf3&_ss=r)
- Charging Module
    - TP4056 (with safety)
        - AliExpress: [seems pretty trustworthy](https://www.aliexpress.us/item/3256807959506419.html?spm=a2g0o.productlist.main.3.3b635853RjHF9a&algo_pvid=7fb60844-e3e3-4a4f-96c7-897a3b00b699&algo_exp_id=7fb60844-e3e3-4a4f-96c7-897a3b00b699-2&pdp_ext_f=%7B%22order%22%3A%221177%22%2C%22eval%22%3A%221%22%7D&pdp_npi=4%40dis%21USD%212.47%210.99%21%21%2117.61%217.06%21%402103146f17511506194958391e7fef%2112000044264539066%21sea%21US%216405565024%21ABX&curPageLogUid=gSqGfju7UfXL&utparam-url=scene%3Asearch%7Cquery_from%3A) (choose type c!) (mfw lead warning)
        - i think that ones protected? nearly got one that was unprotected
- Buck convertor
    - MT3608
        - AliExpress: [looks good](https://www.aliexpress.us/item/3256806175499915.html?spm=a2g0o.productlist.main.1.74ef6433JXc5jv&algo_pvid=a6aa944f-5777-4952-9073-caa6a39f0688&algo_exp_id=a6aa944f-5777-4952-9073-caa6a39f0688-0&pdp_ext_f=%7B%22order%22%3A%225088%22%2C%22eval%22%3A%221%22%7D&pdp_npi=4%40dis%21USD%211.43%210.99%21%21%2110.19%217.05%21%4021030ea417511512431732865e7423%2112000036895232308%21sea%21US%216405565024%21ABX&curPageLogUid=ZKZczbJpqT9P&utparam-url=scene%3Asearch%7Cquery_from%3A) (probably best to use the welcome deal and stuff, might be more worth it to get 3 instead of 2 pieces)
        - need to look into this! not exactly sure how they allow the user to change voltages?
- Motor
    - 775 motor
        - was gonna buy from vex robotics but shipping is atrocious
        - Amazon: [pwease gimme ur amazon pwime account](https://www.amazon.com/Torque-Bearings-Wheels-Upgrade-Bracket%EF%BC%89/dp/B0BW73LMP7?source=ps-sl-shoppingads-lpcontext&ref_=fplfs&smid=A1NVF2KXHRYMP6&utm_source=chatgpt.com&th=1)
- Transistor/MOSFET
    - STP55NF06L
        - alright
        - DigiKey: [shipping might be scary](https://www.digikey.com/en/products/detail/stmicroelectronics/STP55NF06L/1039551)
- Materials
    - Likely PLA from my 3D printer (thanks arcade!) for a majority of structural parts!
    - Likely need a couple screws (maybe nuts?) to screw it into the structure
- Hall Effect Sensor
    - A3144
        - AliExpress: [its called A3144E but seems to be ok](https://www.aliexpress.us/item/3256805644436949.html?spm=a2g0o.productlist.main.3.7539tznWtznWkZ&algo_pvid=7173316d-07ab-495c-89fb-293d7414fb92&algo_exp_id=7173316d-07ab-495c-89fb-293d7414fb92-57&pdp_ext_f=%7B%22order%22%3A%22828%22%2C%22eval%22%3A%221%22%7D&pdp_npi=4%40dis%21USD%214.69%210.99%21%21%2133.40%217.05%21%402101ea7117511403107531206eb465%2112000034504336157%21sea%21US%216405565024%21ABX&curPageLogUid=VaieOt5mf26T&utparam-url=scene%3Asearch%7Cquery_from%3A)
- Magnet
    - some random small neodymium disc magnet (all mine have like chipped into pieces)
        - AliExpress: [i dont need 50 pieces, i need like one or two!](https://www.aliexpress.us/item/3256808695821393.html?spm=a2g0o.productlist.main.9.5b3334f915BtSZ&algo_pvid=aee2dc40-9ab5-42d2-8f9e-716258dc3d6e&algo_exp_id=aee2dc40-9ab5-42d2-8f9e-716258dc3d6e-45&pdp_ext_f=%7B%22order%22%3A%223931%22%2C%22eval%22%3A%221%22%7D&pdp_npi=4%40dis%21USD%213.71%210.99%21%21%2126.45%217.06%21%402103244b17511406317204415e0629%2112000047073358390%21sea%21US%216405565024%21ABX&curPageLogUid=3egb4bJCmrQb&utparam-url=scene%3Asearch%7Cquery_from%3A)
- Jumper Wires
    - realistically, cheapest one that rated nicely would probably work
        - AliExpress: [eh](https://www.aliexpress.us/item/3256801814340687.html?spm=a2g0o.productlist.main.4.2141p0mFp0mF7u&aem_p4p_detail=202506281747233414044354293600001787464&algo_pvid=fc09a167-a6c0-456c-a4b2-1ec021cc4bba&algo_exp_id=fc09a167-a6c0-456c-a4b2-1ec021cc4bba-3&pdp_ext_f=%7B%22order%22%3A%222580%22%2C%22eval%22%3A%221%22%7D&pdp_npi=4%40dis%21USD%212.30%210.99%21%21%212.30%210.99%21%402101eac917511580431171509ed7f6%2112000018371624180%21sea%21US%216405565024%21ABX&curPageLogUid=DscDSYJKQj0M&utparam-url=scene%3Asearch%7Cquery_from%3A&search_p4p_id=202506281747233414044354293600001787464_1)
    
hey, so ive been doing some thinking... it might actually be smarter to split the systems and have two systems thats powered by the xiao! let me break it down! the original idea was this: single battery, powers everything. but this is kinda bad, since we only have a single battery (the tp4056 doesnt really get charging multiple at once, or at least in a safe way, as far as i know). this means low battery life, and possible struggles in keeping things spinning. additionally, brownouts would affect the ENTIRE system. the new idea is to have two systems, each with its own battery (and therefore charging module). one is solely dedicated to the motor, and one is dedicated to the logic and LEDs. this makes sure that any brownouts (battery running low or anything) would be isolated. the xiao will control some transistor/MOSFET on the motor side, which will command the motor to spin or not! (this does mean the GND on both sides need to be connected at some point, probably by connecting the `BAT-` of both TP4056)

woo, that was some typing! somehow part searching took three and a quarter hours of hunting on aliexpress and across the internet! gonna quickly sketch a wiring diagram (of course, not with the actual electronics symbols, but you get it)

![wiring!](</updatelogs/images/202506/06282025 - 1.png>)

ok, time to start making the circuit! (that drawing took like twenty minutes!)

suprise suprise, i need to find footprints and symbols for like everything!

ok, just found the ones for the XIAO ESP32-C3, just need to find how to install them... wow, success!

huge thanks to https://github.com/ccadic/TP4056-18650 for the TP4056 footprints!

ok, still working on the PCB, hopefully gonna finish it tomorrow! got lots of research done today, just lots of designing tomorrow! ok good night

**Time Spent: 4.75 hours**