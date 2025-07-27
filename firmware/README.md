# Firmware

This folder contains the code/firmware that should be put on the two microcontrollers!

Setup Information:
- Act like the respective folder (see below) is the drive of your microcontroller. Or more straightforward, the `README.md` of the respective folder should have the path of `D:/README.md` (or whatever letter the drive shows up as) (**NOT** this `README.md`)
    - [`firmware/led/`](</firmware/led/>) for the LED subsystem
    - [`firmware/motor/`](</firmware/motor/>) for the motor subsystem


As of now, there's not exactly a "test" firmware, as in making sure you wired everything correctly. Use a multimeter to check connections first! As of time of release, Bluetooth has NOT been implemented yet (due to it being kinda hard to write it without being able to test it quickly), so the current release is ok for testing purposes. Do not test the systems together, test them seperately first.