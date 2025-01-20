![ScreenShot 2025-01-19 at 18 17 25@2x](https://github.com/user-attachments/assets/97095bb2-f35f-4f95-97c9-bf18f8aee976)
# Boids!
Boids is an artificial life program, developed by [Craig Reynolds](https://www.red3d.com/cwr/) in 1986, which simulates the flocking behaviour of birds, and related group motion.

It can be great for simulating something like a flock of birds (hence the name boids) or a school of fish.

## Technology
Boids run on pygame (an python library for making 2D graphics in python) to run the visual simulation, the code also uses numpy for math calculations. I used Copilot to optimize math calculations + multithreading as it would consume lots of RAM before + was slow on older machines

## Running locally!
> [!WARNING]  
> This code may use up to 1GB or ram depending on boid count, and will take up threads. You were warned!
So you want to play it!
Here's the steps:
- Clone the repo
- Download python3 (if you don't have it already)
- Open your terminal app and change the directory to this folder and run the following:
    ```
    pip3 install numpy
    pip3 install python3
    ```
- Then run `python3 main.py`. You can press `r` to add boids and `-` to remove boids. Click to add a singular boid, you can also click `b` to change the boids appearance.
