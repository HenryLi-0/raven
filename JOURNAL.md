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

## 06-29-2025: Day 5: PCB Work!
**Does the P stand for pain?**

ok, so last night, before i went to sleep (at 4:15 AM, help my sleep schedule is progressively getting worse and worse), i remembered that i forgot to model the buck convertors in the wiring diagram! here's the updated thing (on paper this time though)

![waw](</updatelogs/images/202506/06292025 - 1.png>)

so, PCB time! currently a little after 3 PM right now! (also, just realized, how am i gonna solder this???)

ok, update! i might actually change it to 5 panels with 10 LEDs each! (turns out, i dont think i can easily solder a 2x5 panel without absolutely messing up (since i dont have a reflow plate thing), so ill do 1x10)

so i dont think i can solder 2 mm preceision... ok 5mm might work

ok, 4:12 PM now, i think the LED panel's good!

![wooo](</updatelogs/images/202506/06292025 - 2.png>)

(yes, i finally figured out how to make the holes that you can solder things through!)

oh wait i forgot to add mounting holes (M2, 2.2mm holes???)

also, just did some research, jumper wires probably arent the best idea for the LED power... just updated yesterday's list of parts! 20 AWG seems to work for power things (and data lines too), so should be good! anyways, just bumped up the track widths of the LED panel, since those skinny 0.2mm are NOT gonna handle like up to 3V, so yeah!

![v2!](</updatelogs/images/202506/06292025 - 3.png>)

~~why does it look like a stick of ram~~

anyways, gonna quickly commit now! (its 4:53 PM!) next stop... the core PCB! (yeah idk what to call it)

ok its now 6:00 PM and i got distracted by a card trick (oops), so back to PCB work!

ok found some resistors: [from aliexpress](https://www.aliexpress.us/item/3256805483786320.html?spm=a2g0o.productlist.main.3.68b125f4Dj2utb&algo_pvid=afd9f67a-3ae5-4ee2-ab52-2d1e553d8175&algo_exp_id=afd9f67a-3ae5-4ee2-ab52-2d1e553d8175-2&pdp_ext_f=%7B%22order%22%3A%222418%22%2C%22eval%22%3A%221%22%7D&pdp_npi=4%40dis%21USD%212.03%210.99%21%21%2114.45%217.06%21%402101eac917512379422191296ed7f6%2112000033959206034%21sea%21US%216405565024%21ABX&curPageLogUid=kfuQkg0ObEyF&utparam-url=scene%3Asearch%7Cquery_from%3A)

need a 10kΩ (heh alt code is Alt+234) and a 100Ω resistor! (aliexpress please stop shipping me twenty, i only need one)

found some beefy diodes (to protect motor from backpowering or anything) [from aliexpress (this gives me all of them, including the normal diodes)](https://www.aliexpress.us/item/2251832446756419.html?spm=a2g0o.productlist.main.3.2b2f28d1vkaD0d&algo_pvid=79ec799f-32cf-45e9-9fcf-b9cf38dce966&algo_exp_id=79ec799f-32cf-45e9-9fcf-b9cf38dce966-2&pdp_ext_f=%7B%22order%22%3A%222134%22%2C%22eval%22%3A%221%22%7D&pdp_npi=4%40dis%21USD%212.16%210.99%21%21%212.16%210.99%21%402103205117512386822514662ebacb%2112000016563917366%21sea%21US%216405565024%21ABX&curPageLogUid=1TofX5J4nMVF&utparam-url=scene%3Asearch%7Cquery_from%3A)

ok, its 7:18 now, heading off for dinner! oh wow its now 8:18 PM, turns out dinner was exactly one hour?

why does the STP55NF06L footprint or something keep crashing kicad.

ok i fixed the issue, but this first iteration of the core PCB looks super uhhh... ugly. it also has very bad wiring, so im gonna actually redo it!

ok, so i dont think im finishing by 12:00, which means no poster D:

however, the core PCB still looks very sad. still working on it! ok quick update, its 11:36 PM, and im enduring the pain of making a whole bunch of traces. turns out, this PCB isn't the friendliest to do this stuff.

ok, its 12:40 AM now, haven't super checked over the wiring, but DRC thinks its ok, gonna quickly run it by omniscient ai to see what it thinks! ok, its 1:03 AM now, and things look good! gonna add some vanity, then start preparing to CAD tomorrow!

ok, 1:26 AM, think its pretty good!

![tired](</updatelogs/images/202506/06292025 - 4.png>)

i added some text wrapped around the center spinning circle! hopefully it turns into a blur when spinning, sort of like a CD! (huge shoutout to Krita for doing this! put the text in krita, used some tool, wrapped it around, then imported it into KiCAD as a footprint with the image converter!)

anyways, that's basically it for me tonight! today was quite the day (tons of PCB design pain), CAD should be ~~just as painful~~ ok, so that's tomorrow! i do need to start planning out the rest of summer, since we only have like 12 days until undercity! (i very likely wont go, since no way parts arrive on time, but we'll see)

oh right, gerbers! ill quickly commit first! (oh its 1:31 AM already? interesting) ok, committed, gerber files made! JLCPCB currently says it'll be around $4.20 (or $6.20? can't really tell if that 10cm x 10cm deal stays?), but shipping is like $3 or something

however, we're still staying on budget! (technically we can go a little above $50, since this kinda is a $150 project, but yeah, staying cheap is probably the best long term)

so, we just need to write firmware, and then somehow find 50 LEDs (we might have to rob a LED strip...)

ok, good night! (i'll calculate the hours tomorrow i guess)

**Time Spent: 7.75 hrs** (wait no way, like the motor?)

## 06-30-2025: Day 6: Starting CAD Stuff!
**no way, onshape appearance?**

ok, nearing a week soon! today's CAD day! or more like tomorrow, since its actually 2 AM on 6/30/2025, and i just pushed the commit with the 6/29/2025 log (im a little too excited to work on this)

but since that's cad day, im actually gonna work on some of the firmware now! ok so its 2:37 AM now, and i got the theoretical settings and startup done, so now all the logic (predictive RPM and timing) needs to be done. gotta search this up, but hopefully it has decimal time tracking (as in, `time.time()` returns a decimal), since if it only returned whole numbers, that would make things a little less accurate!

ok, good night, see you tomorrow morning! (cad cad cad)

ok its 4:07 PM now, time to start CADing! gonna quickly export the kicad files into stl...

ok, everything imported (except that motor... do i just go hunting on aliexpress again?), lets get the CAD started! (its 4:25 PM now!) i guess we do a mastersketch (*DDS noises* (FRC reference))

ok so we need something heavy to keep the whole thing down ~~and not take off~~, so i guess we just make the top as light as possible (pocketing time) and the bottom have attachemts to put something like a weight on (or just make it heavy in general)

also turns out im actually designed it for M4 screws??? ok, wait, let me just take a break and think about this, since this CAD is not going the way i want it. what we want is a setup that looks like this:

![ms paint](</updatelogs/images/202506/06302025 - 1.png>)

and top down, something like (ok left at 5:05 PM and back at 11:20 PM!) (so uh kinda 6 hours passed and oopsie)

![ms paint again](</updatelogs/images/202506/06302025 - 2.png>)

ignoring the fact that they are very not to scale, that's the general idea we're going for! gonna quickly take a visit to the bathroom, then we continue the CAD!

ok i need to figure out what motor im using, since i dont think using amazon shipping is gonna give the best prices (but, i really need to be careful of getting scammed on aliexpress lol) (mfw i say that and the second option is 3 motors prices at $0.99)

ok, so we need a shaft that isnt a perfect cylinder, or else we will not be able to get a grip... ok, so i actually cant find any non-sketchy D-shaft 775 motor, so i guess im gonna use [this one](https://www.aliexpress.us/item/3256807114067845.html?spm=a2g0o.productlist.main.1.16cd6776Vgc891&algo_pvid=26af35e1-df73-4cc4-ac55-c5f83bc87477&algo_exp_id=26af35e1-df73-4cc4-ac55-c5f83bc87477-17&pdp_ext_f=%7B%22order%22%3A%22554%22%2C%22eval%22%3A%221%22%7D&pdp_npi=4%40dis%21USD%2116.50%210.99%21%21%21117.41%217.03%21%402101c59117513426452444616e02a5%2112000040117671201%21sea%21US%216405565024%21ABX&curPageLogUid=Umbp8PlZyzJa&utparam-url=scene%3Asearch%7Cquery_from%3A) that has a circular shaft, so ill probably use some hub or something (or just use superglue? idk)

hey, add [M4 screws (M4, 20mm)](https://www.aliexpress.us/item/3256804341271555.html?spm=a2g0o.productlist.main.2.461ac14e7BXtJq&algo_pvid=43910c63-45e0-4ecd-b9b1-ad107835e2ab&algo_exp_id=43910c63-45e0-4ecd-b9b1-ad107835e2ab-1&pdp_ext_f=%7B%22order%22%3A%225870%22%2C%22eval%22%3A%221%22%7D&pdp_npi=4%40dis%21USD%211.16%210.99%21%21%211.16%210.99%21%402101ea7117513433620995216eb46a%2112000029486656871%21sea%21US%216405565024%21ABX&curPageLogUid=FRqi06trgT20&utparam-url=scene%3Asearch%7Cquery_from%3A) to the BOM! and [these brass heat inserts (M4, OD 6mm, length 5mm)](https://www.aliexpress.us/item/3256803396040989.html?spm=a2g0o.productlist.main.2.309e5c43kJ2Kn6&algo_pvid=41f4ca04-74cd-48e3-9b75-9c71cfc4611e&algo_exp_id=41f4ca04-74cd-48e3-9b75-9c71cfc4611e-1&pdp_ext_f=%7B%22order%22%3A%2218926%22%2C%22eval%22%3A%221%22%7D&pdp_npi=4%40dis%21USD%211.88%210.99%21%21%211.88%210.99%21%40210313e917513432649813622e6066%2112000026370649721%21sea%21US%216405565024%21ABX&curPageLogUid=yV34TZUfSQd2&utparam-url=scene%3Asearch%7Cquery_from%3A) while youre at it! and [these M4 nuts (M4)](https://www.aliexpress.us/item/3256807407546447.html?spm=a2g0o.productlist.main.2.368eNuFVNuFVPm&algo_pvid=8fe920d4-ae35-4001-9942-7d798b919b5b&algo_exp_id=8fe920d4-ae35-4001-9942-7d798b919b5b-1&pdp_ext_f=%7B%22order%22%3A%2211553%22%2C%22eval%22%3A%221%22%7D&pdp_npi=4%40dis%21USD%211.56%210.99%21%21%2111.08%217.02%21%402101e07217513438147161886eaffb%2112000041426239344%21sea%21US%216405565024%21ABX&curPageLogUid=GygBYXASGNU6&utparam-url=scene%3Asearch%7Cquery_from%3A)! (ill have to look into this, but i *could* use the heat inserts as nuts... might be a bad idea, but ill look into it)

ok, gotta go to sleep now (its so early), but i do have a meeting tomorrow that i'll definitely not use to work on the CAD... no no, that would be such a terrible idea... who would ever do such thing? (*subtle foreshadowing*)

ok, just realized that the motor has some threaded m4 holes already! gotta update the PCB now, but heres the CAD so far!

![cad](</updatelogs/images/202506/06302025 - 3.png>)

ok good night now! (oops got caught being up at 12:40 AM oops)

**Time Spent: 2.5 hrs**

## 07-01-2025: Day 7: Updating PCB and CAD Work!
**While being very eepy.**

yeah i really need to stop sleeping on this cad

9:45 PM here on the first day of july, i guess lets start it off on a good step! just kidding, i fell asleep on the bed and now its 10:58 PM. oops. ok, back to CADing!

ok, so i gotta update the PCB for this, but the LED panel should be using the M4 not the M2 screws... gonna do that right now! additionally, the core PCB need motor mounting holes! ok, 11:48 PM, and just updated the core PCB! the back now has the silkscreen labels for what each hole does, and shifted stuff so that its farther from the motor hole! (we dont want shorts or funny drilling activity near the center)

ok, idk what took so long, buts its now 12:13 AM, but the PCBs are updated! here's some screenshots!

![OMG LEDS!!!](</updatelogs/images/202506/07012025 - 1.png>)

![core pcb!](</updatelogs/images/202506/07012025 - 2.png>)

ok, ill see you in the morning where i should hopefully finish the cad (yes, i had a 6.5 hour meeting this morning, unfortunately couldnt CAD during that time)

speaking of the CAD, the base will need to be split, since i cant exactly fit a 24 cm diameter disc on my A1 mini (18cm x 18cm build plate) (~~i just had a funny idea about printing a 0.1kg part on the school printers~~ (jk im not actually gonna do that, ill probably split the part into eigths and connect it with the M4 screws))

ok, so CAD, firmware, and BOM to do!

ok good night now

**Time Spent: 1.5 hrs**

## 07-02-2025: Day 8: More CAD Work!
**designing 3d printing mounts to be strong is kinda hard**

yeah this CAD really shouldve been done 2 days ago...

so its now 9:43 PM today (wait this feels a litle familiar), so lets get CADing! i was thinking about moving the PCB wit all the core stuff from the bottom to the top, but throught that this would expose the electronics a bit too much, and it might not have the stability that mounting it directly the the front would give. also, for now, the LED panels also serve as protection from when any electronics in the main board ever flies out (please no). basically, i will need a lot of filament for this one...

i just had an idea, what if we added a thing called a speaker directly into the thing? nah thats actually probably a bad idea if we're using the xiao (since, we dont exactly have lots of extra pins) also, just realized that the way we setup redundancy for the MOSFET and the sensor is probably a bad idea (for the MOSFET, both are set to OUT, meaning we could have issues, gotta add some diodes...) i'll fix that later!

ok just got jumpscared that we might not be able to trigger the STP55NF06L with the XIAO, but after sneaking around the internet, i found a [datashee](https://www.st.com/resource/en/datasheet/stp55nf06l.pdf), and it looks like we'll probably be ok! ok back to cad

ok why did yesterday's windows update steal 21 GB (mfw windows keeps spamming me with updates and install four apps of bloatware on my device including one that probably has some vulnerability that'll show up in like a month that allows it to take over peoples computers) (ok now who used 0.1 GB from the last time i looked at that screen. yeah i see you, 20.6 GB to 20.5 GB...) (WHYS IT AT 20.1 GB NOW) ok im gonna install this update and try to fix my computer

hey peeps at microsoft, small request, please stop filling my computer with random intern slop! i really dont need to be forced to have copilot or whatever this new phone UI next to my start menu is. also, please stop messing around with my desktop icons! thanks. also please give my 20 GB back. thanks! back to CAD...

ok its been 20 minutes and i think i found the issue, hopefully not bad happens when i tell windows to delete previous windows installation data... something funny... the internet just broke. i guess thats the one time onshape isnt the best cad tool! oh nvm its back now

ok so we might need some caster wheels or something for the spinning bits, since idk how a short metal shaft with 0.35 cm of clearance likes having a whole spinning system mounted on top of it, but ill just add spaces to attach on future wheels if necessary (ill probably just make them out of PLA or something)

wait a second we kinda need more clearance

ok more clearance get

ok so ive been trying to do this CAD in a way that the printed parts dont like snap from centrifigal or whatever force (basically, spin at super speed, outward things fly), so ive had an idea! the PCB is basically solid copper, so we dont have to worry about that too much (yeah, try snapping one in half with your hands (or maybe dont)). its also in the center, so it doesnt experience too much, we just have to make sure we solder our connections well!

so its been like 10 minutes, and i just realized this idea isnt perfect, so im gonna keep paying around with configs

actually yeah, this idea does really work at all, either something can break or something is weirdly/impossibly mounted, ive ran through like 3 configs already

WAIT! THE SOLUTION IS JUST KISS (KEEP IT SIMPLE, SILLY!)! THE SOLUTION IS JUST A BRACKET WITH OPPOSING SUPPORTS THAT HAS SPACERS!

![what is that](</updatelogs/images/202506/07022025 - 1.png>)

so, what are you even looking at? yeah, probably shouldnt have drawn it with pen, but it was first thing i could grab, so so be it. basically, you can see the bracket there, with the clean surface being the on point bottom right (clean surface, as in, the face that isnt covered with layer lines). then we have these four other "caps" that wrap around the bracket, with the clean surface facing up. then, we have a spacer that's just solid PLA that goes on the bases of each screw, with the clean surface being the surface that, when you look at top down, you see the screw hole. then, we can wrap this around the sides, allowing us to make sure the "caps" dont move. (we can also just super glue just to be super sure!) and thats the solution! the screws then go in, and it stays! nice! ok, time to CAD this! (wow, that was a lot of thinking...)

yeah i guess i gotta CAD this upside down, we're actually kinda getting really high in the air already...

ok, being forced to go to sleep again (but its only 12:30 AM???), so here's the CAD update! 

![onshape mention](</updatelogs/images/202506/07022025 - 2.png>)

anyways, that's it! hopefully more progress tomorrow, but yeah, gotta update the PCB too! (maybe i wake up early tomorrow and grind? idk)

**Time Spent: 2.75 hrs**

