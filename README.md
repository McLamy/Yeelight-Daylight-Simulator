# Yeelight Daylight Simulation

_Foreword_
I wanted to have a backlight for my monitors on my desk. However, I didn't want to sit in rainbow colors all the time, but the light should bring me added value and accordingly increase my productivity or signal to my body when it's time to finish work. That's why I developed this script, which calculates the current light temperature in Kelvin and converts it into RGB values, which are then sent to Yeelight. With this script, I want to simulate daylight. However, I found that the light was overall too warm, so I added a bell curve that keeps the light at 6500K for a longer period of time around noon, which should increase productivity.
I took several photos of sunlight on a white wall and compared the RGB values to those from the script. They didn't match exactly, so I implemented a color shift to get as close as possible to the colors of the sun photos.

_Installation_

- The script comes with the following dependencies: yeelight, math, pytz, suntime
- Change the coordinates to your own coordinates
- Change the IP address of Yeelight to the IP address in your network.
