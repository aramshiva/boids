![ScreenShot 2025-01-19 at 18 17 25@2x](https://github.com/user-attachments/assets/97095bb2-f35f-4f95-97c9-bf18f8aee976)
# Boids!
Boids is an artificial life program, developed by [Craig Reynolds](https://www.red3d.com/cwr/) in 1986, which simulates the flocking behaviour of birds, and related group motion.

Boids uses three simple rules to work accurately:
- separation: steer to avoid crowding local flockmates
- alignment: steer towards the average heading of local flockmates
- cohesion: steer to move towards the average position (center of mass) of local flockmates

### TL;DR Boids is a program that can create really cool swarm intelligences and can simulate basically real flocks of birds, schools of fish and stuff like that.

## Technology
-The visual/graphics run on [`pygame`](https://pygame.org) (An python library to make 2D graphics.python) to run the visuals. 
- [`numpy`](https://numpy.org/) is used to run more complex mathmatical calculations to caclulate boids three rules.
- [`GitHub Copilot`](https://github.com/features/copilot) was used to optimize my bad math calculations + adding multithreading.

## Run Yourself!
That's cool and all but how do I run it myself?
> [!WARNING]
> This code uses a lot (~1GB) of RAM and threads. This is due to how the optimization techniques work and I do not guarantee it will work on your local machine, if it doesn't post a GitHub issue but I can't promise anything
- Make sure you have [Python](https://www.python.org/) installed.
- Next, clone the repo and move to that directory.
- Run: 
```
pip install -r requirements.txt
```
- Last, run `python3 main.py`!

### Controls
`R` - Add boids
`CLICK` - Add boid
`-` - Remove boids
`B` - Change boid mode (different filters and styles!)
`C` - Change color of boids