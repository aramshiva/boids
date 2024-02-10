import pygame
import random

pygame.init()

HEIGHT = 1000
WIDTH = 1000
w = pygame.display.set_mode([HEIGHT, WIDTH])
w.fill((33, 33, 33))
boids = []
num_of_boids = 25
Debug = True


# actual important stuff
class Boid:
    def __init__(self, size, color):
        self.size = size
        self.color = color
        self.num_of_boids = num_of_boids  # Define num_of_boids as a class attribute

    def create(self):
        # create list of dictonaries of boids using num_of_boids
        for i in range(self.num_of_boids):
            boids.append(
                {
                    "num": i,
                    "x": random.randint(0, WIDTH),
                    "y": random.randint(0, HEIGHT),
                }
            )

    def draw(self):
        # draw boids
        for boid in boids:
            pygame.draw.circle(w, self.color, (boid["x"], boid["y"]), self.size)

    def move(self):
        for boid in range(len(boids)):
            # implement basic movement
            boids[boid]["x"] += random.randint(-3, 4)
            if boids[boid]["x"] <= 0:
                boids[boid]["x"] += 4
            if boids[boid]["x"] >= WIDTH:
                boids[boid]["x"] -= 5
            boids[boid]["y"] += random.randint(-2, 3)
            if boids[boid]["y"] <= 0:
                boids[boid]["y"] += 3
            if boids[boid]["y"] >= HEIGHT:
                boids[boid]["y"] -= 4

        # Check if Birds are colliding
        for boid in boids:
            for otherboid in range(len(boids) - 1):
                otherboidz = boids[otherboid]
                if random.randint(1, 2) == 1:
                    # Kill a bird
                    if (
                        boid["x"] == otherboidz["x"]
                        and boid["y"] == otherboidz["y"]
                        and boid["num"] != otherboidz["num"]
                    ):
                        boids.pop(otherboid)
                else:
                    # Make a new baby bird
                    if (
                        boid["x"] == otherboidz["x"]
                        and boid["y"] == otherboidz["y"]
                        and boid["num"] != otherboidz["num"]
                    ):
                        self.num_of_boids += 1  # Update the class attribute
                        boids.append(
                            {
                                "num": self.num_of_boids - 1,
                                "x": boid["x"],
                                "y": boid["y"],
                            }
                        )

    def cohesion(self):  # steer towards the average heading of local flockmates
        for boid in boids:
            sum_x = 0
            sum_y = 0
            count = 0
            for otherboid in boids:
                if boid != otherboid:
                    distance = (
                        (boid["x"] - otherboid["x"]) ** 2
                        + (boid["y"] - otherboid["y"]) ** 2
                    ) ** 0.5
                    if distance < 50:  # consider only nearby boids
                        sum_x += otherboid["x"]
                        sum_y += otherboid["y"]
                        count += 1
            if count > 0:
                avg_x = sum_x / count
                avg_y = sum_y / count
                boid["x"] += int((avg_x - boid["x"]) / 10)
                boid["y"] += int((avg_y - boid["y"]) / 10)
                if (
                    Debug
                    and int((avg_y - boid["y"]) / 10) != 0
                    and int((avg_x - boid["x"]) / 10) != 0
                ):
                    print("COHESION USED, details below:")
                    print(
                        "("
                        + str(int((avg_x - boid["x"]) / 10))
                        + ", "
                        + str(int((avg_y - boid["y"]) / 10))
                        + ")"
                    )

    def separation(self):  # steer to avoid crowding local flockmates
        pass

    def alignment(
        self,
    ):  # steer to move in the same direction as the average heading of local flockmates
        pass


# code
Boidz = Boid(5, (255, 255, 255))
Boidz.create()
while True:
    Boidz.draw()
    pygame.display.flip()
    w.fill((33, 33, 33))
    Boidz.move()
    Boidz.cohesion()  # Added cohesion
    pygame.time.wait(100)

input()
