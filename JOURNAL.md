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

![OMG LEDS!!!](</updatelogs/images/202507/07012025 - 1.png>)

![core pcb!](</updatelogs/images/202507/07012025 - 2.png>)

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

![what is that](</updatelogs/images/202507/07022025 - 1.png>)

so, what are you even looking at? yeah, probably shouldnt have drawn it with pen, but it was first thing i could grab, so so be it. basically, you can see the bracket there, with the clean surface being the on point bottom right (clean surface, as in, the face that isnt covered with layer lines). then we have these four other "caps" that wrap around the bracket, with the clean surface facing up. then, we have a spacer that's just solid PLA that goes on the bases of each screw, with the clean surface being the surface that, when you look at top down, you see the screw hole. then, we can wrap this around the sides, allowing us to make sure the "caps" dont move. (we can also just super glue just to be super sure!) and thats the solution! the screws then go in, and it stays! nice! ok, time to CAD this! (wow, that was a lot of thinking...)

yeah i guess i gotta CAD this upside down, we're actually kinda getting really high in the air already...

ok, being forced to go to sleep again (but its only 12:30 AM???), so here's the CAD update! 

![onshape mention](</updatelogs/images/202507/07022025 - 2.png>)

anyways, that's it! hopefully more progress tomorrow, but yeah, gotta update the PCB too! (maybe i wake up early tomorrow and grind? idk)

**Time Spent: 2.75 hrs**

## 07-03-2025: Day 9: Even More CAD Work!
**cad cad cad**

henry did not wake up early.

oh wait i just realized todays the first day of a certain convention in pittsburg! guess ill see a couple videos coming out in a couple days... **NO WAY! [ITS WATER THEMED!](https://en.wikipedia.org/wiki/Anthrocon)** (water game?) (scroll to the bottom)

anyways, its 9:02 PM (this feels a bit way too familiar...) and its now CAD time! also, i just remembered LCSC was a thing, and since desoldering LEDs off an LED strip (where, the LEDs could have a strong adhesive, LEDs could be sketchy, i could melt one again, etc.) is a bad idea, LCSC probably is a smarter idea (for a lot of our electronics, in fact) (might be a bit more expensive, but honestly cheaper and more reliable in the long run, just need to make sense of these aprt nubmers...)

anyways, back to the CAD! (reminder for myself that i also need to update the PCB with some diodes)

![interesting color choice...](</updatelogs/images/202507/07032025 - 1.png>)

but yeah, something like that! probably should make the bottom a bit shorter though... ok, done! (parametric cad!!!)

![hmm](</updatelogs/images/202507/07032025 - 2.png>)

hmm, someones (probably me) is gonna get punched real hard by these two protruding screws, might make a big fat long spacer in the back (maybe not too much of a problem, but we'll see later) also, the nuts might touch the power and ground of the LED panels, so we need to take note of that

ok, currently simulating the load and stuff, had to replace the LED and PCB material with plantinum because FR-4 doesnt have some ratio or constant or something so onshape cant simulate it

oh wow whys it taking so long... is onshape like doing a blender render or something

oh its done! took like 7 minutes, but its ready! oops i did a modal simulation instead of linear static... guess its another wait? oh wow, much faster! ~~wait a second why does that look so sus~~

ok, putting 2 pounds of force is unrealistic, but its not gonna do it any good. anyways, heres a more realistic 0.2 pound load on it

![hmm](</updatelogs/images/202507/07032025 - 3.png>)

in the end, the top structure would probably keep it all together! ill probably just keep onshape on overnight and simulate when the cad is actually done! right, back to cad!

just had an idea, what if we make our base heavier by just filling it with sand? it would make it essentially heavier than 100% infill PLA, and it would probably be way cheaper? wait a second i dont even need to buy it, i have a beach like a kinda far away (maybe gravel will also do?)

ok, silly CAD activities, this might be the worst quality CAD i made in a while, but ill clean it up in a bit

i just remembered that we need to do the light thingy (you know, the thing where we decrease the angle of exiting light?)

wait we might actually need all the screws they give (so far using like 75 screws) this reminds me of that one time we spammed rivets on one robot cad

ok, gonna go to sleep now, here's the current state of the CAD! i guess ill use the extra screw space on the LED pannels to screw on the light blocking thingy, and yeah, we're getting there! still lots of other things to do (PCB update and code and BOM), but we're getting there!

![cad!](</updatelogs/images/202507/07032025 - 4.png>)

ok, good night!

**Time Spent: 3.5 hrs**

## 07-04-2025: Day 10: PCB and Electronics
**pcb funny, and electronics too**


ok, starting today at 2:20 PM instead of the previous couple days! fist things first, im gonna update the PCBs!

ok, been doing some work, then just remembered that i needed to update the license (since, GNU GPL v3 is kinda a more software thing). just updated it, with `CERN-OHL-S v2` for the hardware and `GNU GPL v3` for the software! that should keep everything open source! ok, quick commit, PCB work is still being done!

ok, board should be ready! 

![waw](</updatelogs/images/202507/07042025 - 1.png>)

ok, kicad wont stop telling me in DRC that theres errors, since the `A3144E GPIO` isn't connected (since, connecting both GPIO to listen to the A3144 would probably end badly). im gonna have to write this down somewhere, but we have to connect those two pins!

ok, we need to update the LED ones now...

also, dont remembered if i mentioned this, but the LED panel needs updates because... a nut kinda crushes one of the LEDs, and the bottom ones might be a *little* too close to the pads (ill do the LCSC stuff later)

wait its 3:45 PM now, im gonna take a quick break... back at 4:04 PM! (not found)

since the LED panel is 99.8827mm tall, we're getting really close to the 10cm mark, so we might actually have to make the ~~RAM stick~~ LED panel a bit wider, which should, in theory, not really change the price? this quote is taking a while... yeah, still $2.10! ok gonna work on it...

LED PCB now updated! updating the cad now...

![ram stick](</updatelogs/images/202507/07042025 - 2.png>)

ok, exported, importing into onshape! (also, quick commit)

uh why is the xiao made of solid gold now (yes, i know that its just the color, but it looked really funny)

![gold microcontroller](</updatelogs/images/202507/07042025 - 3.png>)

wait i might actually need to revisit the idea of putting the boards electronics on top since... er...

![whaaa](</updatelogs/images/202507/07042025 - 4.png>)

yeah we might have a bit of a problem... yeah, mounting it on top might be the move... also, we have a LOT of collision issues

so we might have to solder the wires upside down for the main part, which is probably a smart move if we incorporate a couple zip ties, since that should keep all the wiring safe and tucked inside the machine (we dont want a flying whip of sorts) we also need to have a safety off switch, which i kinda forgot to add to the BOM, but that'll probably be ziptied somewhere too

![hmm](</updatelogs/images/202507/07042025 - 5.png>)

played around with how wire length can impact singal strength, and it seems that sus wiring that goes back and forth for very long doesnt mess with the signals *too* much, we'll have to see with the neopixels (right now, its just GPIO value determines on/off, unlike neopixels that have to send the info)

ok, its 5:06 PM and im gonna be back in a bit! as for CAD work, planning on starting to do the right side (with the batteries and chargers) now!

ok, back at work at 8:15 PM, and did a bit more playing around with those LEDs...

![leds leds leds](</updatelogs/images/202507/07042025 - 6.png>)

basically, doubled or tripled the amount of wires going back and forth, so this is like seriously an overestimate of what the actual leds will experience, but theres no really difference in brightness, so i think we're ok! gonna write a letter real quick, currently 8:45 PM!

ok so now its 10:33 PM, and the neighbors somewhere are really playing around with fireworks, or at least someone in like a 1 mile radius is. anyways, since it sounds like something more violent, im gonna try to focus (while im like the closest to the window)

whys the floor shaking

hey so im back, thinking about it, is a 775 overkill for our system? given the battery, TP4056 output, and converting it to 5V, we might have like, very little amps to deal with for the motor, which might just not spin. basically, we dont need industrial motors, just motors than can spin the roughly 2 (lets say 3 for headroom) pound thing at 1k or 2k RPM, gonna do some research now...

wheres the search bar in here rdfjpasdjvksdnfaksdfasdfas found a good RS550 motor, except for the fact that it leads me to whatever dollar express is and THERES NO SEARCH BAR ADKLASKLDFALSKDJ (i dont need a usb air humidifier, i just want my motor)

yeah so its now 11:50 PM, and im still trying to research what motors work and dont, and if my wiring idea sucks, since research really conflicts with itself. im looking at TP4056 wiring on youtube, and 3 of Orbit (FRC 1690)'s videos show up in a row in "Explore More" (2022-2024).

ok, so we've had some changes! instead of running everything through the TP4056 modules to control the voltage and what not, we're actually gonna use the battery directly connect to the MT3608 to get power to the logic circuit, then we have some other convertor for the motor, which also has battery directly, basically we dont have the TP4056 on the spinning bit itself, but just the batteries. then connect it to the ground of the MOSFET, since we need to do the whole electron thing

ok, so its 12:40 AM now, and ive been doing a ton of researching and might need to make a ton of changes. basically, today was very confusing, and i really need to rethink the power system. kinda tired, hopefully waking up at a reasonable time tomorrow!

ok good night

**Time Spent: 4.75 hrs**

## 07-05-2025: Day 11: Further Confusion
**electronics are confusing**

ok, first things first. electronics.

4:36 PM right now, gonna search in the depths of youtube videos to find any wiring example with the battery!

yeah so im kinda super confused right now. so ignore what i said last night, we should definitely not connect the raw battery straight to the circuit (we need overdischarge protection). so, apparently the TP4056 does and does not have overdischarge protection? video and research is conflicting, but im gonna assume not. a battery management systems is *kinda* a bit up there in pricing, so im gonna research overdischarge protection now

oh its 5PM theres some mosim announcement stream right now, guess ill leave the 5 minutes youtube premiere timer in the background?

ok, turns out i forgot we had discharge protection oops

ok so that was 5:30 PM, organized my stuff, did a little art for the preview image (does that count for time? i guess not...), so here's the idea! basically, we charge the batteries serperately, then plug it into the machine, where we will NOT BE CONNECTING IT RAW, but instead, have an over-discharge module (that im still trying to find :D), which should give us a ton of amps! also, this means that we need big fat beefy traces all over the place (since, 20A max discharge rate is kinda a lot, since we designed with 3A max in mind)

heh i just drew some art (oops its 11:50 PM now) oops now its 12:39 AM, ill continue this on my phone!

ok its 1:36 AM and im on my phone now with github mobile, so dont be expecting any pictures! trying to do some research in the safer metoeds while still getting reasonable power, and i think what we said before (over discharge module thing), is ok! gonna hunt on aliexpress now...

found this [over discharge protection module](https://www.aliexpress.com/item/1005006160741067.html)! instructions on how to use it unclear, but another one that looks similar also has instructions so its *probably* the same right (please be)

yeah i fell asleep typing that, so thats it for 7/5/2025! good night!

**Time Spent: 1.5 hrs**

## 07-06-2025: Day 12: Hunting
**lcsc watch out WAIT ARE THOSE LEDS**

yeah so we kinda gotta finish this...

just did a little research on the reviews of yesterday's overdischarge stuff, and it seems good! only downside is that its a *little* expensive (dont worry, welcome deal here! not sure how many deals i can get...) so, i guess we need to redraw the wiring diagram! (its 9:30 PM right now) wait a second, why does it say supply voltage 12V to 36V, guess this isnt the product for that!

so we need the entire battery output, but overdischarge protection to stop lower battery sus activity, so the battery should be able to deliver its stated 20A, but not get restrictied by the TP4056's 1A dishcharge thing (which is also one reason we arent including it on the spining bit now)

ok i gotta go for a second (its 10 right now), since my cousin is currently doing something in texas (i have no clue whats going on) ok three minutes later, and i guess they just diappeared off the face of the earth? i dont really know, gonna go back to search on aliexpress and LCSC, oh looks like theyre back

also the MT3608 that we had earlier does 2A max, which isnt enough... however, heres a [battery charger protection thing](https://www.aliexpress.us/item/3256807120302984.html?spm=a2g0o.productlist.main.1.11115eb9tU5tMV&algo_pvid=17b15dd3-c056-4c08-8b4d-3a71811ebffa&algo_exp_id=17b15dd3-c056-4c08-8b4d-3a71811ebffa-0&pdp_ext_f=%7B%22order%22%3A%2212577%22%2C%22eval%22%3A%221%22%2C%22orig_sl_item_id%22%3A%221005007306617736%22%2C%22orig_item_id%22%3A%221005007296858433%22%7D&pdp_npi=4%40dis%21USD%213.27%211.64%21%21%2123.30%2111.65%21%402103277f17518531947346287e3da2%2112000040176986833%21sea%21US%216405565024%21ABX&curPageLogUid=Ibhrdg7VpNy4&utparam-url=scene%3Asearch%7Cquery_from%3A) (choose 2S 20A Balanced)! (uh idk if running this on only one battery would work?) yeah idk if this is the move, its layout looks super cursed, and im not exactly sure buying 4 batteries is the move. looking into making my own overdischarge protection circuit (bad idea), and i see a minecraft comparator reference

theres no way im soldering that

![what the](</updatelogs/images/202507/07062025 - 1.png>)

anyways, heres some things i found:
- [1S 24A, might be the one! little sus, but should be good](https://www.aliexpress.us/item/3256805852468677.html?spm=a2g0o.productlist.main.9.302f5e3czX8KX7&algo_pvid=25c9b235-06aa-403b-ad23-0fdd63fde68e&algo_exp_id=25c9b235-06aa-403b-ad23-0fdd63fde68e-8&pdp_ext_f=%7B%22order%22%3A%22570%22%2C%22eval%22%3A%221%22%7D&pdp_npi=4%40dis%21USD%210.88%210.88%21%21%216.26%216.26%21%402101e9a217518566248628615e1e4a%2112000035437067506%21sea%21US%216405565024%21ABX&curPageLogUid=mvB8T0ck0sas&utparam-url=scene%3Asearch%7Cquery_from%3A)
- [1S 10A, ok, less sus, but not enough amps!](https://www.aliexpress.us/item/3256806617397129.html?spm=a2g0o.productlist.main.3.302f5e3ceqAYR7&algo_pvid=abc4450d-26db-481b-8f75-b82ffec1d72d&algo_exp_id=abc4450d-26db-481b-8f75-b82ffec1d72d-2&pdp_ext_f=%7B%22order%22%3A%22496%22%2C%22eval%22%3A%221%22%7D&pdp_npi=4%40dis%21USD%211.37%210.99%21%21%219.79%217.08%21%402103201917518565855054326e5bf8%2112000038357512404%21sea%21US%216405565024%21ABX&curPageLogUid=VgW5fFPmZzZJ&utparam-url=scene%3Asearch%7Cquery_from%3A)
- [some 18650 format battery holder of sorts](https://www.digikey.com/en/products/detail/keystone-electronics/1044/5057795)

ok anyways its 11PM and im off to watch frozen 2 for like the fifteenth time ok see ya

ok its 12:13 AM and i just finished reading all the FRC servers im in (lurking behavior), anyways back to aliexpress! the `1S 24A` one (the first link) seems pretty ok, a little sketchy (not too many reviews) and one picture has a chip without a part marking in the photo, but reviews seem alright and the pictures. also, just realized, these will take a LONG time to ship. like it says july 19-22. eh, i guess trade off for being so cheap.

ok, so thats good! time to hunt LCSC for an A3144 and the MOSFET

hmm you need to by 5 A3144 at once, but i guess LCSC is better since its like $4 on aliexpress for also 5 (also, LCSC is probably more reputable) [here's](https://lcsc.com/product-detail/Hall-Switches_JSMSEMI-A3144EUA-T-JSM_C18188954.html?s_z=n_a3144) the link! also, whys the datasheet only in chinese

also, AP scores dont appear out yet? guess ill check in the morning

ok, since the pdf didnt allow copy pasting, i just downloaded it, went to google drive, uploaded it, and now i can copy and paste. yeah it just works like that. anyways, looks good! gonna hunt for the mosfet now, we also need leds...

yep, [here's](https://lcsc.com/product-detail/MOSFETs_STMicroelectronics-STP55NF06L_C77582.html?s_z=n_STP55NF06L) the STP55NF06L, cheaper than digikey!

ok, WS2812B now, shouldnt be too hard... oh yeah, nvm, since theres apparently 46 different ones, guess i spoke too soon... also thats crazy, 983885 and 1010610 leds in stock, how many do they mass produce at once?

waa who makes this many leds? (please send me your secret led stash)

![leds leds leds](</updatelogs/images/202507/07062025 - 2.png>)

wait i need to find what footprint or at least what the LEDs i have look like... ok, whatever `LED_WS2812B_PLCC4_5.0x5.0mm_P3.2mm` means (probably 5mm by 5mm base and 3.2mm tall?) reading through [this datasheet](https://lcsc.com/datasheet/lcsc_datasheet_2506031657_XINGLIGHT-XL-5050RGBC-WS2812B_C2843785.pdf) for [these leds](https://lcsc.com/product-detail/RGB-LEDs-Built-in-IC_XINGLIGHT-XL-5050RGBC-WS2812B_C2843785.html?s_z=n_ws2812b) and dont really get whats 500 euros?

![wha](</updatelogs/images/202507/07062025 - 3.png>)

wait this is funny

![oops](</updatelogs/images/202507/07062025 - 4.png>)

anyways, im gonna continue research on the phone, currently 1:02 AM! (lots of things start tomorrow, guess i should try sleeping earlier today? probably not)

**Time Spent: 3.5 hrs**

## 07-07-2025: Day 13: More Hunting (and LEDs!)
**did someone say leds**

yeah its 12:52 PM and im forcrd to touch grass to earn money

turns out the middle achool has the same internet password as the other schools across NYC so it appears that i maybe can hunt for more LCSC parts

yeah so last night i fell asleep (oops) so i guess heres the summary

basically, the one i was looking at had weird funny funny, basically i had no clue what that extra characters on that text mean. also, the marking on the LED itself (like the lines) were different so i went back on LCSC and found [this thingy](https://lcsc.com/product-detail/RGB-LEDs-Built-in-IC_Worldsemi-WS2812B-B-W_C114586.html), looks pretty close to the actual thing (i have to make sire the markings match when i get back home), but it has a 5.0mm x 5.4mm, wait nvm actually the base is 5.0mm x 5.0mm, 5.4mm is just counting the pads! ok, this should be the one!

yeah its now 3:14 PM (last thing was from 1:20 ish) getting bored now (we're all done with our stuff), kinda miss my computer right now, but we'll do with what we have. 

60 of [these LED](https://lcsc.com/product-detail/RGB-LEDs-Built-in-IC_Worldsemi-WS2812B-B-W_C114586.html) (same as the ones up there) cost $3.95 (FRC 395? two train robotics?) anyways, within our budget! (wonder what shipping costs are?)

ok, i guess we have to calculate trace width at home (and figure out and **finalize** the power system), so its 3:18 PM, i need to find the bathroom in this school, so see ya!

yeah bathroom was in a very cursed spot and the bathroom itself was very cursed. anyways, its 9:15 PM at night, and i decided to do a little something for the last 15 minutes!

![woa](</updatelogs/images/202507/07072025 - 1.png>)

yeah, i also didnt expect to see the insides of my hackpad tonight, but i just decided to do a little cleaning! while it was out however, i decided to snag some data on its light spread! unfortunately, my measurements tell me that its more than 180 degrees, since it somehow lit areas below the PCB, but that's also probably since we're in a white room with a couple reflective surfaces here and there. anyways, the aforementioned LEDs seem good! anyways, finalizing the power system time!

wait research is telling me we need like 1 or 2 cm thick traces for 5V @20A... anyways, lets ignore that for now, and draw this diagram!

why does going outside make me so tired (i just laid in bed from 9:30 PM to 10 PM) ok now im being forced to sleep, i guess you get a wiring diagram tomorrow? just kidding, took like 45 minutes, but here's the drawing!

![diagram!](</updatelogs/images/202507/07072025 - 2.png>)

ok good night! (yeah i need to update the journal for today and yesterday, ill do it sometime!)

**Time Spent: 1.5 hrs**

## 07-08-2025: Day 14: Traces and Confusion
**what is going on**

no way its taking this long, lets finish this! so, its 6PM right now (started updating the journals at 5:45 PM)! realized that yesterday's diagram isnt *super* clear (as in, image quality, its a little blurry), so here's a better image!

![diagram!](</updatelogs/images/202507/07082025 - 1.png>)

ok, first thing, lemme double check that the MT3608 can actually support our amperage (and volts too), so lets do some math... ok, so if we can support 3.7-4.2V @20A, we can do 5V @14.8-16.8A, which is ok? also, for the motor, if we need, we can run it at 14V @5.29-6A (lower limit is roughly 5.28571A), which should be able to power the 775 motor? it might actually be ok for this! (we're feeding a total of 74-84W)

ok, just ran through this idea with an omniscient ai, and it says its pretty much ok, just have a shared ground for everything and the buck convertors, so yeah, thats what im gonna do! well, after dinner, its 6:30 right now!

ok, back, its 7:45 PM now! i guess its time to do the PCB stuff? gonna calculate the width of the traces real quick...uh 2.5cm traces is kinda crazy, lemme double check that... uh yeah.

ok, so since we cant have giant fat 2cm traces on our PCB, we're gonna have to do something different. uh. so we kinda need to "banish" a couple amps on the logic side... wait a second, does the battery only supply whats needed? oh. oopsie, i guess we dont need 2cm traces on our PCB! (except for the motor...) ok, PCB time now! im gonna estimate the logic line needs 5A at most (probably only 3A at most, realistically, but lets just do 5A to be safe), so, according to kicad, with a current of `5A` and temperature rise of `10C`, we need `2.76552mm` traces (round to `2.8mm`, just to be safe). meanwhile, for `20A` and temperature rise of `10C`, we need `18.7156mm` traces (round to `20mm`, just to be safe). ok, time to get to work!

hmm... how to change the entire net... did it manually, LED panel's almost good! just gonna change the pad size...

![waw](</updatelogs/images/202507/07082025 - 2.png>)

ok, 8:50 PM, led panel done! now for the big PCB... (also those traces are MASSIVE) yeah, we also need to do the thing with the shared ground... yeah so this is kinda confusing... wait im gonna quickly commit the led stuff

oh yeah we should also look to source our diodes from LCSC

ok, back (took a rest from 9PM to 9:30PM), yeah these nets are absolutely messed up... really considering redoing it? how am i supposed to route the pins of the MOSFET when the traces are 2cm thick... yeah so if we shove 20A in a 0.8mm trace, we get some sweet 1800C temperature rise (aka, we start dealing with liquid copper)

ok, you know what, i guess we'll let it rise `15C`, and just print some fan blades to stick onto this (since, this thing is essentially a giant fan), bringing out traces to `14.6331mm` wide, rounded to `15mm`

wait im gonna find the datasheet or data of the motor to find out how many amps we should actually aim for

need to do some math, so if each LED is 5mm apart, and say, a 25cm diamter, we have a roughly 158 LED long circle (assuming the LEDs fit the circle perfectly, which they dont), anyways, what was i calculating again? we need to do a full revolution every "refresh" of the eye, so thats like 50 rotations per second? so like 3k rotations per minute?

wait im a little silly. oops. so uh, basically, since we're running it at 14V, we actually **ARENT** shoving 20A down the line, we actually are doing 5-6A, so we actually only need `4.39879mm` traces (calculated for `7A`, rounded to `4.4mm`). yeah sorry, that was a big waste of time... ok, looking for motors (original one is kinda... lacking documentation), andymark has terrifying shipping prices

wait im actually kinda confused because 14V @5-6A is, in fact, **NOT** enough for this motor... im gonna stop doing the PCB design for now, gonna focus on what motor we're using. ok, just spent a bit look at [some 550 motors](https://www.aliexpress.us/item/3256805434004883.html?spm=a2g0o.productlist.main.2.38ad10dbozbJho&algo_pvid=c85af6f1-91bd-4d8b-9026-3312fcf9b4de&algo_exp_id=c85af6f1-91bd-4d8b-9026-3312fcf9b4de-1&pdp_ext_f=%7B%22order%22%3A%22476%22%2C%22eval%22%3A%221%22%7D&pdp_npi=4%40dis%21USD%213.63%210.99%21%21%2125.92%217.06%21%40210318e817520322585382672ea633%2112000033773483986%21sea%21US%216405565024%21ABX&curPageLogUid=eMsbf9qdwhwJ&utparam-url=scene%3Asearch%7Cquery_from%3A) and i *think* they aren't strong enough? i guess we just stick with our original motor and try to figure stuff out?

looking back, a `1S 24A` BMS makes kinda no sense for the 20A max discharge battery, gotta fix that too. guess we going for `1S 16A` then! ok, talking to omniscient ai, i just got insulted, so i guess 775 isn't the way to go? so the 775 is an inrunner motor but we're looking for an outrunner motor. however, that setup would require us to have a slipring since the mosfet is still in the spinning bit, so thats kinda out of the question. also, the boost convertor does 2A max so we need to find another one

ok so its 12:30 AM right now, and ive think ive accepted the fact that we cant do this do a 775 motor, we have to use an outrunner motor. however, that requires us to move the entire motor control circuitry off the spinning board and onto a new board that stays stationary with respect to the table. this means we have two microcontrollers, one in the spinning bit for LED control and one at the base for motor control. they *should* communicate when to power on and off via bluetooth! 

[drone motor something](https://www.aliexpress.us/item/3256802252458485.html?spm=a2g0o.productlist.main.3.464bbwchbwchf3&algo_pvid=a1260a99-3e96-46e5-b9f9-6d5ccf6346fa&algo_exp_id=a1260a99-3e96-46e5-b9f9-6d5ccf6346fa-11&pdp_ext_f=%7B%22order%22%3A%22517%22%2C%22eval%22%3A%221%22%7D&pdp_npi=4%40dis%21USD%214.64%210.99%21%21%214.64%210.99%21%402101ec1a17520361227765313ea087%2112000020658933923%21sea%21US%216405565024%21ABX&curPageLogUid=lLdhzPZdPGnO&utparam-url=scene%3Asearch%7Cquery_from%3A)

something something esc, honestly, im a bit too tired tonight, so i guess ill continue looking into this tomorrow!

good night! (12:50 AM woo)

ok so its like 2:31 AM and ive been looking at memes for like an hour (i should stop), but realized im the buggest silly in the seven seas right now. we dont need a drone motor or an outrunner motor. we just need to flip the 775 motor upside down so that the shaft touches the spinny bit and spins with it, and is normally mounted onto the bit that doesnt spin. then, we have to have the two microcontroller setup, but this time we can actually use PWM and our MOSFET idea/setup (instead of a whole ESC setup for drone motors and whatever). this does mean we need like a giant clearance between the motor (like the big part) and the lower PCB, but i guess we could just print the bottom and just have a top PCB if we have to. anyways, this also gives us more space for the motor PCB and its wiring, so thats nice! ok good night!

**Time Spent: 4.25 hr**

## 07-09-2025: Day 15: Boost Convertor
**henry didnt find it**

wow today was quite the day, its already 10 PM..., anyways watched another movie today, time to start working! yeah so today in the doctors office i got bored while waiting and decided to research a couple of boost convertors (since the current MT3608 we have has a max amp of 2A, which is quite sad when we want to power motors). anyways, found [this one](https://www.aliexpress.us/item/3256805882203198.html?spm=a2g0n.productlist.0.0.186529edWzCVc3&aff_platform=msite&m_page_id=mvipdhwcaawioqjm197f1148b831e07212c62465f0&gclid=&pdp_ext_f=%7B%22order%22%3A%22937%22%2C%22eval%22%3A%221%22%7D&pdp_npi=4%40dis!USD!1.73!0.99!!!12.34!7.05!%402101c5ac17520963580108649eed83!12000035596268598!sea!US!6405565024!ABX&algo_pvid=c5c05c22-8da6-4f29-bb19-0adee8073828), but it requires an input voltage of 10-32V, which the battery doesnt exactly deliver. therefore, we continue hunting.

yeah so its been 22 minutes and im starting to think there arent any boost convertors around for this job. so uh, found [this](https://www.aliexpress.us/item/2255800011462620.html?spm=a2g0o.productlist.main.1.18b2lpAAlpAAaF&algo_pvid=556b5380-9541-4ed4-956d-35e1f915b3c7&algo_exp_id=556b5380-9541-4ed4-956d-35e1f915b3c7-26&pdp_ext_f=%7B%22order%22%3A%223088%22%2C%22eval%22%3A%221%22%7D&pdp_npi=4%40dis%21USD%211.87%210.99%21%21%211.87%210.99%21%402101ef5e17521136451725715e2715%2112000044237774496%21sea%21US%216405565024%21ABX&curPageLogUid=Ne4PmkucTc7K&utparam-url=scene%3Asearch%7Cquery_from%3A) but its limited to 5A in its input, so yeah. im kinda getting desperate here.

ok who keeps breaking the internet router

so i just had an idea, yeah its not gonna work (it was to skip the boost convertor for the motor and just attach it raw, but we need more volts!) yeah its been 45 minutes now and i cant find a good one. ok its now 11:05 PM and im just gonna take a break, ive looked through way too many aliexpress offers today...

ok im back at 12:15 AM and im honestly very tired lol, but lets try to push through.

[here's](https://www.aliexpress.us/item/3256805855172022.html?spm=a2g0o.productlist.main.12.7795lnSalnSasl&algo_pvid=b0afe62d-f32d-4314-85ed-17e95cc84a90&algo_exp_id=b0afe62d-f32d-4314-85ed-17e95cc84a90-11&pdp_ext_f=%7B%22order%22%3A%22712%22%2C%22eval%22%3A%221%22%7D&pdp_npi=4%40dis%21USD%210.96%210.96%21%21%216.85%216.85%21%402101c5b117521210612946204e1677%2112000035452245642%21sea%21US%216405565024%21ABX&curPageLogUid=SWzPmyjDzBHM&utparam-url=scene%3Asearch%7Cquery_from%3A) a thing for 2A battery protection (choose `2S 20A Balance` or something)

alright, lets just finish this research phase, im getting really tired

what did i just come across

![what this](</updatelogs/images/202507/07092025 - 1.png>)

ok theres actually no way i spent the entirety of today search for a single boost converter. anyways, im just gonna draw a wiring diagram real quick (yes for v3)

yeah so i just realized that... this soltuion kinda means that i need a step down to 5V thing for the motor system since we have a XIAO that doesnt want to become a frying pan

yeah ok, laid out all the components, its 1AM now, im just gonna wrap this up tomorrow (yay dont have to go outside tomorrow since its online on thursdays) (probably going to school on friday for driver practice? probably a good idea)

so yeah, thats it, good night!

**Time Spent: 2 hrs**

## 07-10-2025: Day 16: Rewiring 
**batteries**

ok, its 4:10 PM, so lets get this done! after yesterday and a bit of research before i went to sleep last night, ive determined that theres like no viable option for a boost convertor that can convert @20A, even at low voltages, to higher voltages, at least, none that are cheap. basically, all the ones that i could find were in the $20 to $30 price range, which is absolutely silly, so ive actually got a better idea! we just, instead of spending so much on a single sad boost convertor, we actually spend it on batteries, so that we already have the correct voltage! (this is also cheaper than buying the boost converter, gives us more power, and also allows us to skip the whole boost converter bit for the motor!)

this means, the motor... gets 4 batteries. yeah. however, note that the boost converter i found was $25-ish, and the 2 additional batteries would only be $10, meaning that buying batteries instead is actually a smarter move! (the omniscient ai also seems to agree, so this is probably also the good move forward!) however, all we need to do is make sure out battery protection system (as in over-discharge protection) is ok and not, you know, super dubious

to the aliexpress! but first, gotta do something else, brb! (its 4:20 right now)

yah so its 12:00 AM and i took some practice test and think i did ok, but anyways, back to drawing the layout! gotta find a 4S battery protection thingy... ok, found one thats 4S but 30A (we need 20A or less), 3S 20A (please so close)

idk, so far found these two but i dont like something about both of them
- [i cant tell if this acutal does discharge protection since weird docs contradict title but idk](https://www.aliexpress.us/item/3256806852470291.html?spm=a2g0o.productlist.main.8.270e37b5TFYjci&algo_pvid=deb023e0-46fe-4aff-b650-c48ea758565d&algo_exp_id=deb023e0-46fe-4aff-b650-c48ea758565d-8&pdp_ext_f=%7B%22order%22%3A%223256%22%2C%22eval%22%3A%221%22%2C%22orig_sl_item_id%22%3A%221005007038785043%22%2C%22orig_item_id%22%3A%221005005356630077%22%7D&pdp_npi=4%40dis%21USD%212.22%211.11%21%21%2115.86%217.93%21%402101ead817522078481501637e4d8d%2112000039180604374%21sea%21US%216405565024%21ABX&curPageLogUid=uLIF7P0l0uhI&utparam-url=scene%3Asearch%7Cquery_from%3A)
- [weird connector and hard to read docs](https://www.aliexpress.us/item/3256808381922829.html?spm=a2g0o.productlist.main.3.3e9d2360vC5qEx&algo_pvid=3f3e1191-641f-4e39-9b19-ada63354c459&algo_exp_id=3f3e1191-641f-4e39-9b19-ada63354c459-2&pdp_ext_f=%7B%22order%22%3A%22236%22%2C%22eval%22%3A%221%22%7D&pdp_npi=4%40dis%21USD%212.89%212.51%21%21%2120.61%2117.93%21%402103247917522076636808908e5bdd%2112000045753788312%21sea%21US%216405565024%21ABX&curPageLogUid=8Qs8lZR9Nvbh&utparam-url=scene%3Asearch%7Cquery_from%3A)

ok, went back to drawing the wiring diagram, but im not sure if we should do two hall effect sensors or one, ill brb, just gonna save and commit and continue on my phone!

how am i on 10%, anyways, basically, heres the deal. we have the two systems seperated (hey maybe we can use some of the extra pins for a speaker), only connected by bluetooth, but what if that connection fails, or we need more accurate data (since, RPM can change very fast). if the hall effect sensor is on the LED section, we wont have the ability to speed up accurately (probably some PID control), as in the feedback data will always be delayed by the connection. this shouldnt be a big deal, but disconnects or signal intereference can mess with this

ok, what if we moved the hall effect sensor to the motor side? well, we wont be able to have the exact timings for the LEDs, which is kinda really bad since the LEDs really need to know where they are. speaking of which, i have an idea for super precise position measuring, and kts very silly. code execution time measuring and prediciting, we havent even started firmware yet...

so basically, have delays and risk bad connection, or just dont even need them to send this data and just give each of them their own. and i think thats the better move since we get 5 of them at a time anyways

ok so im going up to school for driving practice tomorrow so good night! (its 1:24 AM, guess ill do it on like 5 hours of sleep) also, gotta remember to find a stronger boost converter for the LED side, wait, i dont remember saying this, but the logic side has been renamed to the led side! also, subsystem also works in place of side for both of them! ok good night now!

**Time Spent: 1.25 hrs**