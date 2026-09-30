from array import array
import pygame as py
from math import hypot
from typing import Any, Sequence

class Entity:
    FPS = 60

    def __init__(self, pos: list[int], color: list[int]) -> None:
        self.pos = array('f', pos)
        self.color = color

class Physic(Entity):
    G = 9.8
    A = G / Entity.FPS

    def __init__(self, mass: float, velocity: list[int], dump:float, friction:list[float]) -> None:
        self.mass = mass
        self.velocity = array('f', velocity)
        self.dump = dump
        self.friction = friction
        self.colliding = [False, False]

    def apply_physic(self, WIDTH: int, HEIGHT: int):
        self.colliding[:] = [False, False]
        self.apply_gravity()
        self.apply_velocity()
        self.check_collition_wall(WIDTH, HEIGHT)
        self.apply_friction()

    def apply_velocity(self):
        self.pos[0] += self.velocity[0]
        self.pos[1] += self.velocity[1]

    def apply_gravity(self):
        self.velocity[1] += self.A

    def apply_force(self, force: Sequence[float|int]):
        accelration = (force[0] / self.mass / self.FPS, force[1] / self.mass / self.FPS)
        self.velocity[0] += accelration[0]
        self.velocity[1] += accelration[1]

    def apply_friction(self):
        if self.colliding[1]:
            friction_step = self.friction[1] * self.A
            if abs(self.velocity[0]) < friction_step:
                self.velocity[0] = 0
            else:
                self.velocity[0] -= friction_step * (1 if self.velocity[0] > 0 else -1)
        if self.colliding[0]:
            friction_step = self.friction[0] * self.A
            if abs(self.velocity[1]) < friction_step:
                self.velocity[1] = 0
            else:
                self.velocity[1] -= friction_step * (1 if self.velocity[1] > 0 else -1)

    def check_collition_wall(self, WIDTH: int, HEIGHT: int):
            pass

    def check_collition_others(self, others:list[Any]):
        pass

class Ball(Physic):
    def __init__(self, pos: list[int], color: list[int], radius: int, mass: float, velocity: list[int], dump:float=0.8, friction:list[float]=[0.6,0.6]) -> None:
        Entity.__init__(self, pos, color)
        Physic.__init__(self, mass, velocity, dump, friction)
        self.radius = radius

    def draw(self, WIN: py.Surface):
        py.draw.circle(WIN, self.color, self.pos, self.radius)

    def check_collition_wall(self, WIDTH: int, HEIGHT: int):
        if self.pos[0] + self.radius > WIDTH:
            self.pos[0] = WIDTH - self.radius
            self.velocity[0] *= -self.dump
            self.colliding[0] = True
        if self.pos[0] - self.radius < 0:
            self.pos[0] = self.radius
            self.velocity[0] *= -self.dump
            self.colliding[0] = True
        if self.pos[1] + self.radius > HEIGHT:
            self.pos[1] = HEIGHT - self.radius
            self.velocity[1] *= -self.dump
            self.colliding[1] = True
        if self.pos[1] - self.radius < 0:
            self.pos[1] = self.radius
            self.velocity[1] *= -self.dump
            self.colliding[1] = True

    def check_collition_others(self, others):
        for e in others:
            if self is e:
                continue

            dx = self.pos[0] - e.pos[0]
            dy = self.pos[1] - e.pos[1]
            d = hypot(dx, dy)
            min_d = self.radius + e.radius

            if d == 0 or d >= min_d:
                continue

            nx = dx / d
            ny = dy / d

            overlap = min_d - d
            self.pos[0] += nx * overlap * 0.5
            self.pos[1] += ny * overlap * 0.5
            e.pos[0] -= nx * overlap * 0.5
            e.pos[1] -= ny * overlap * 0.5

            rvx = self.velocity[0] - e.velocity[0]
            rvy = self.velocity[1] - e.velocity[1]
            vn = rvx * nx + rvy * ny

            if vn > 0:
                continue

            j = -(1 + self.dump) * vn / 2
            self.velocity[0] += j * nx
            self.velocity[1] += j * ny
            e.velocity[0] -= j * nx
            e.velocity[1] -= j * ny
