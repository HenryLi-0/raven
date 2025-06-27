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

