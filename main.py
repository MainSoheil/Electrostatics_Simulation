import pygame as py
from array import array
from Base import Ball
from random import randint, randrange, choice
from os.path import exists as path_exists

init_eletrons = 100

py.font.init()
font = py.font.SysFont('Segoe UI', 20)
SIZE = array('H', [1000, 600])
WIN = py.display.set_mode(SIZE, py.DOUBLEBUF | py.RESIZABLE | py.HWACCEL)
py.display.set_caption("Electrostatics")
if path_exists("./assets/icon.png"):
    py.display.set_icon(py.image.load("./assets/icon.png"))
py.event.set_allowed(py.MOUSEBUTTONDOWN | py.KEYDOWN | py.WINDOWRESIZED | py.QUIT)

BG = py.Color(0, 0, 0)

class Electron(Ball):
    K = 9 * 10 ** 9

    def __init__(self, pos, radius, charge: float, color:list[int]=[30, 230, 30]) -> None:
        Ball.__init__(self, pos, color, radius, 0.1, [0, 0], 0.8, [0.4, 0.4])
        self.charge = charge
        self.charge_sign = None if charge == 0 else charge > 0
        if charge > 0:
            charge_text = '+'
        elif charge < 0:
            charge_text = '-'
        else:
            charge_text = '0'
        self.text = font.render(charge_text, True, py.Color(230, 230, 230))
        self.text_size = self.text.get_size()

    def apply_charge(self, others: list['Electron']):
        for e in others:
            if self is e:
                continue
            dx = self.pos[0] - e.pos[0]
            dy = self.pos[1] - e.pos[1]
            r2 = dx * dx + dy * dy
            if r2 == 0:
                continue
            r = r2 ** 0.5
            F = self.K * self.charge * e.charge / r2
            A = F / self.mass / self.FPS
            self.velocity[0] += A * dx / r
            self.velocity[1] += A * dy / r

    def draw(self, WIN: py.Surface):
        super().draw(WIN)
        WIN.blit(self.text, (self.pos[0] - self.text_size[0] // 2, self.pos[1] - self.text_size[1]))

electrons = [
    Electron([randrange(0, SIZE[0] - 5, 20), randrange(0, SIZE[1] - 5, 20)], 5, choice([-1, 1]) * 50 * 10**-6, [randint(0, 255) for _ in range(3)]) for _ in range(init_eletrons)
]

def draw():
    WIN.fill(BG)
    clone_electrons = electrons.copy()
    for e in clone_electrons:
        e.apply_charge(clone_electrons)
        e.apply_velocity()
        e.check_collition_wall(*SIZE)
        e.check_collition_others(clone_electrons)
        e.draw(WIN)

    py.display.flip()

def keydown():
    keys = py.key.get_pressed()
    force = [0, 0]
    if keys[py.K_RIGHT]:
        force[0] += 1
    if keys[py.K_LEFT]:
        force[0] -= 1
    if keys[py.K_UP]:
        force[1] -= 1
    if keys[py.K_DOWN]:
        force[1] += 1
     
    if any(force):
        for el in electrons:
            el.apply_force(force)

def main():
    run = True
    fps = 60
    clock = py.time.Clock()
    while run:
        for e in py.event.get():
            match e.type:
                case py.MOUSEBUTTONDOWN:
                    if e.button == 1:
                        electrons.append(Electron(e.pos, 5, 50 * 10**-6, [randint(0, 255) for _ in range(3)]))
                    elif e.button == 3:
                        electrons.append(Electron(e.pos, 5, -50 * 10**-6, [randint(0, 255) for _ in range(3)]))
                case py.KEYDOWN:
                    if e.key == py.K_ESCAPE:
                        run = False
                        break
                    if e.key == py.K_SPACE:
                        if electrons:
                            electrons.pop(randint(0, len(electrons)-1))
                case py.WINDOWRESIZED:
                    SIZE[0], SIZE[1] = e.x, e.y
                case py.QUIT:
                    run = False
                    break
        keydown()
        draw()
        clock.tick(fps)

if __name__ == "__main__":
    main()
