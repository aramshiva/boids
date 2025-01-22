import pygame
import math
import random
import numpy as np
from collections import defaultdict
import threading

pygame.init()

COLORS = {"BLUE": (12, 18, 226),"RED": (255, 0, 0),"GREEN": (0, 255, 0),"YELLOW": (255, 255, 0),"ORANGE": (255, 165, 0),"PURPLE": (128, 0, 128),"PINK": (255, 192, 203),"CYAN": (0, 255, 255),"WHITE": (255, 255, 255),"BLACK": (0, 0, 0),"GRAY": (128, 128, 128),"BROWN": (165, 42, 42), "GRAY": (128, 128, 128)}
HEIGHT = 750
WIDTH = 1250
BG_COLOR = (255, 255, 255)
# VISION_COLOR = (200, 200, 200)
VISION_COLOR = COLORS["YELLOW"]
SHOW_VISION = True
BOID_SIZE = 5
BOID_TYPE = "lights"
VISION_RADIUS = 20
BOIDS_COUNT = 1000
TRANSPARENCY_VALUE = 5
VISION_TYPE = "circle"
BOID_COLOR = COLORS["RED"]

class Grid:
    def __init__(self, cell_size):
        self.cell_size = cell_size
        self.grid = defaultdict(list)
        self.max_flock = int(BOIDS_COUNT * 0.3)
    
    def get_cell_coords(self, pos):
        return (int(pos['x'] // self.cell_size), int(pos['y'] // self.cell_size))
    
    def update_boid(self, boid):
        cell = self.get_cell_coords(boid.pos)
        self.grid[cell].append(boid)
    
    def neighbors(self, boid):
        cell = self.get_cell_coords(boid.pos)
        neighbors = []
        neighbor_cells = [(cell[0] + dx, cell[1] + dy) for dx in [-1, 0, 1] for dy in [-1, 0, 1]]
        neighbors = [boid for neighbor_cell in neighbor_cells for boid in self.grid.get(neighbor_cell, [])]
        flock = [n for n in neighbors if n != boid]
        if len(flock) > self.max_flock:
            return []
        return flock

    def clear(self):
        self.grid.clear()

class Boid:
    def __init__(self, posX=random.randint(1, WIDTH), posY=random.randint(0, HEIGHT)):
        self.pos = {'x': posX, 'y': posY}
        angle = math.radians(random.uniform(0, 360))
        self.velocity = {'x': math.cos(angle) * 2, 'y': math.sin(angle) * 2}
        self.size = BOID_SIZE
        self.angle = math.atan2(self.velocity['y'], self.velocity['x'])
        self.cached_neighbors = []
        self.color = BOID_COLOR
        self.points = self.generate_points()

    def generate_points(self):
        if BOID_TYPE == "exp":
            return [
                (self.size * math.cos(self.angle) + random.randint(-3, 3),
                 self.size * math.sin(self.angle) + random.randint(-3, 3)),
                (self.size * math.cos(self.angle + 2.6) + random.randint(-3, 3),
                 self.size * math.sin(self.angle + 2.6) + random.randint(-3, 3)),
                (self.size * math.cos(self.angle - 2.6) + random.randint(-3, 3),
                 self.size * math.sin(self.angle - 2.6) + random.randint(-3, 3))
            ]
        return []

    def limit_speed(self, max_speed):
        speed = math.sqrt(self.velocity['x']**2 + self.velocity['y']**2)
        if speed > max_speed:
            self.velocity['x'] = (self.velocity['x'] / speed) * max_speed
            self.velocity['y'] = (self.velocity['y'] / speed) * max_speed

    def draw(self, surface):
        if SHOW_VISION:
            if VISION_TYPE == "circle":
                pygame.draw.circle(surface, VISION_COLOR, (int(self.pos['x']), int(self.pos['y'])), VISION_RADIUS, 1)
            elif VISION_TYPE == "square":
                pygame.draw.rect(surface, VISION_COLOR, (int(self.pos['x']) - VISION_RADIUS, int(self.pos['y']) - VISION_RADIUS, 2 * VISION_RADIUS, 2 * VISION_RADIUS))
            else:
                vision_surface = pygame.Surface((2 * VISION_RADIUS, 2 * VISION_RADIUS), pygame.SRCALPHA)
                vision_surface.set_alpha(TRANSPARENCY_VALUE)
                pygame.draw.circle(vision_surface, VISION_COLOR, (VISION_RADIUS, VISION_RADIUS), VISION_RADIUS)
                surface.blit(vision_surface, (int(self.pos['x']) - VISION_RADIUS, int(self.pos['y']) - VISION_RADIUS))
        if BOID_TYPE == "invisible":
            pass
        if BOID_TYPE == "triangle":
            points = [
                (self.pos['x'] + self.size * math.cos(self.angle),
                 self.pos['y'] + self.size * math.sin(self.angle)),
                (self.pos['x'] + self.size * math.cos(self.angle + 2.6),
                 self.pos['y'] + self.size * math.sin(self.angle + 2.6)),
                (self.pos['x'] + self.size * math.cos(self.angle - 2.6),
                 self.pos['y'] + self.size * math.sin(self.angle - 2.6))
            ]
            pygame.draw.polygon(surface, self.color, points)
        if BOID_TYPE == "lights":
            BG_COLOR = (3, 8, 172)
            # BOID_COLOR = (12, 18, 226)
            points = [
            (self.pos['x'] + self.size * math.cos(self.angle),
             self.pos['y'] + self.size * math.sin(self.angle)),
            (self.pos['x'] + self.size * math.cos(self.angle + 2.6),
             self.pos['y'] + self.size * math.sin(self.angle + 2.6)),
            (self.pos['x'] + self.size * math.cos(self.angle - 2.6),
             self.pos['y'] + self.size * math.sin(self.angle - 2.6))
            ]
            flock_size = len(self.cached_neighbors)
            intensity = min(255, 50 + flock_size * 5)
            color1, color2, color3 = self.color
            flock_color = (
            min(255, color1 + intensity),
            min(255, color2 + intensity),
            min(255, color3 + intensity)
            )
            pygame.draw.polygon(surface, flock_color, points)
        elif BOID_TYPE == "exp":
            points = [
                (self.pos['x'] + point[0], self.pos['y'] + point[1])
                for point in self.points
            ]
            pygame.draw.polygon(surface, self.color, points)
            if self.pos['x'] < self.size:
                pygame.draw.polygon(surface, self.color, [(p[0] + WIDTH, p[1]) for p in points])
            elif self.pos['x'] > WIDTH - self.size:
                pygame.draw.polygon(surface, self.color, [(p[0] - WIDTH, p[1]) for p in points])
            if self.pos['y'] < self.size:
                pygame.draw.polygon(surface, self.color, [(p[0], p[1] + HEIGHT) for p in points])
            elif self.pos['y'] > HEIGHT - self.size:
                pygame.draw.polygon(surface, self.color, [(p[0], p[1] - HEIGHT) for p in points])
        elif BOID_TYPE == "circle":
            pygame.draw.circle(surface, self.color, (int(self.pos["x"]), int(self.pos["y"])), 5)
        elif BOID_TYPE == "square":
            pygame.draw.rect(surface, self.color, (self.pos['x'], self.pos['y'], self.size, self.size))
    def separation(self, boids):
            steer = {'x': 0, 'y': 0}
            my_pos = np.array([self.pos['x'], self.pos['y']], dtype=np.float64)
            positions = np.array([[b.pos['x'], b.pos['y']] for b in boids], dtype=np.float64)
            if len(positions) > 0:
                differences = positions - my_pos
                distances = np.linalg.norm(differences, axis=1)
                mask = distances < VISION_RADIUS
                if np.any(mask):
                    differences = differences[mask]
                    distances = distances[mask].reshape(-1, 1)
                    steer_forces = np.divide(differences, distances, where=distances != 0)
                    steer['x'], steer['y'] = -np.sum(steer_forces, axis=0)
    
            return steer

    def alignment(self, boids):
        avg_velocity = {'x': 0, 'y': 0}
        count = 0
        for other in boids:
            if other != self:
                dx = self.pos['x'] - other.pos['x']
                dy = self.pos['y'] - other.pos['y']
                distance = math.sqrt(dx**2 + dy**2)
                if distance < VISION_RADIUS:
                    avg_velocity['x'] += other.velocity['x']
                    avg_velocity['y'] += other.velocity['y']
                    count += 1
        if count > 0:
            avg_velocity['x'] /= count
            avg_velocity['y'] /= count
            return avg_velocity
        return {'x': 0, 'y': 0}

    def cohesion(self, boids):
        center = {'x': 0, 'y': 0}
        count = 0
        for other in boids:
            if other != self:
                dx = self.pos['x'] - other.pos['x']
                dy = self.pos['y'] - other.pos['y']
                distance = math.sqrt(dx**2 + dy**2)
                if distance < VISION_RADIUS:
                    center['x'] += other.pos['x']
                    center['y'] += other.pos['y']
                    count += 1
        if count > 0:
            center['x'] /= count
            center['y'] /= count
            return {'x': center['x'] - self.pos['x'], 'y': center['y'] - self.pos['y']}
        return {'x': 0, 'y': 0}
    
    def update(self, boids):
        sep = self.separation(boids)
        align = self.alignment(boids)
        coh = self.cohesion(boids)
        separation_weight = 5.0
        alignment_weight = 1.0
        cohesion_weight = 2.0
        jitter = {'x': (random.random() - 0.5) * 1.0, 'y': (random.random() - 0.5) * 1.0}
        self.velocity['x'] += (separation_weight * sep['x'] + alignment_weight * align['x'] + cohesion_weight * coh['x'] + jitter['x'])
        self.velocity['y'] += (separation_weight * sep['y'] + alignment_weight * align['y'] + cohesion_weight * coh['y'] + jitter['y'])
        self.limit_speed(2)
        self.pos['x'] += self.velocity['x']
        self.pos['y'] += self.velocity['y']
        self.angle = math.atan2(self.velocity['y'], self.velocity['x'])

        if BOID_TYPE == "exp" and random.randint(1, 100) == 1:
            self.points = self.generate_points()

        if self.pos['x'] < -self.size:
            self.pos['x'] = WIDTH + self.size
        elif self.pos['x'] > WIDTH + self.size:
            self.pos['x'] = -self.size
        if self.pos['y'] < -self.size:
            self.pos['y'] = HEIGHT + self.size
        elif self.pos['y'] > HEIGHT + self.size:
            self.pos['y'] = -self.size
    
boids = [Boid(random.randint(1, WIDTH), random.randint(1, HEIGHT)) for _ in range(BOIDS_COUNT)]

screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption("boids")

grid = Grid(VISION_RADIUS)
running = True

def update_boids():
    while running:
        grid.clear()
        for boid in boids:
            grid.update_boid(boid)
        for boid in boids:
            boid.cached_neighbors = grid.neighbors(boid)
            boid.update(boid.cached_neighbors)
        pygame.time.Clock().tick(60)

def draw_boids():
    while running:
        screen.fill(BG_COLOR)
        for boid in boids:
            boid.draw(screen)
        pygame.display.flip()

update_thread = threading.Thread(target=update_boids)
draw_thread = threading.Thread(target=draw_boids)

update_thread.start()
draw_thread.start()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            x, y = pygame.mouse.get_pos()
            boids.append(Boid(x, y))
        elif event.type == pygame.VIDEORESIZE:
            WIDTH, HEIGHT = event.w, event.h
            screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_v:
                SHOW_VISION = not SHOW_VISION
            if event.key == pygame.K_g:
                if VISION_TYPE == "circle":
                    VISION_TYPE = "square"
                elif VISION_TYPE == "square":
                    VISION_TYPE = "lights"
                elif VISION_TYPE == "lights":
                    VISION_TYPE = "circle"
            elif event.key == pygame.K_c:
                BOID_COLOR = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
                for boid in boids: boid.color = BOID_COLOR
            elif event.key == pygame.K_b:
                if BOID_TYPE == "triangle":
                    BOID_TYPE = "circle"
                elif BOID_TYPE == "circle":
                    BOID_TYPE = "square"
                elif BOID_TYPE == "square":
                    BOID_TYPE = "lights"
                elif BOID_TYPE == "lights":
                    SHOW_VISION = True
                    BOID_TYPE = "invisible"
                    OLD_BG_COLOR = BG_COLOR
                    BG_COLOR = (0, 0, 0) 
                else:
                    SHOW_VISION = False
                    BG_COLOR = OLD_BG_COLOR
                    BOID_TYPE = "triangle"
            elif event.key == pygame.K_r:
                for _ in range(random.randint(1, 100)):
                    boids.append(Boid(random.randint(1, WIDTH), random.randint(1, HEIGHT)))
            elif event.key == pygame.K_MINUS:
                for _ in range(random.randint(1, 100)):
                    if boids:
                        boids.pop()

update_thread.join()
draw_thread.join()

pygame.quit()
