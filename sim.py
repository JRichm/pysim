import pygame
import sys
import random
import colors as c

class Simulation:
    def __init__(self, num_dots):
        pygame.init()
        self.width = 1280
        self.height = 720
        self.num_dots = num_dots
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.clock = pygame.time.Clock()
        self.dots = [Dot(random.randint(self.width / 4, self.width - (self.width / 4)), random.randint(self.height / 4, self.height - (self.height / 4))) for _ in range(num_dots)]
        self.draw_screen()

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            self.update()
            self.draw()
            pygame.display.flip()
            self.clock.tick(240)  # Adjust the frame rate as needed

    def draw_screen(self):
        self.screen.fill(c.red)
        black_screen = pygame.Surface((self.width - 30, self.height - 30))
        black_screen.fill(c.black)
        self.screen.blit(black_screen, (15, 15))


    def update(self):
        for dot in self.dots:
            dot.update(self.width, self.height, self.dots)

    def draw(self):
        self.draw_screen()
        for dot in self.dots:
            dot.draw(self.screen)


class Dot:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.color = c.white  # White color
        self.velocity = (random.randint(0, 10000), random.randint(0, 10000))
        self.drag = 0
        self.gravAmm = 0
        self.gravMax = 300
        self.worldGrav = 30

    def calculate_velocity(self):

        # add drag from previous velocity
        self.velocity = (self.velocity[0] - self.drag, self.velocity[1] - self.drag)

        # add gravity 
        self.gravAmm += self.worldGrav
        if self.gravAmm > self.gravMax:
            self.gravAmm = self.gravMax

        self.velocity = (self.velocity[0], self.velocity[1] + self.gravAmm)


    def check_collision(self, other_dot):
        distance = ((self.x - other_dot.x) ** 2 + (self.y - other_dot.y) ** 2) ** 0.5
        return distance < 4  # Assuming dots have a radius of 2, adjust as needed

    def update(self, screen_width, screen_height, all_dots):
        self.calculate_velocity()

        self.x += self.velocity[0] * 0.001
        self.y += self.velocity[1] * 0.001

        # Bounce off walls
        if self.x < 20:
            self.x = 20
            self.velocity = (-self.velocity[0] / 1.1, self.velocity[1])
        elif self.x > screen_width - 20:
            self.x = screen_width - 20
            self.velocity = (-self.velocity[0] / 1.1, self.velocity[1])

        if self.y < 20:
            self.y = 20
            self.velocity = (self.velocity[0], -self.velocity[1] / 1.1)
        elif self.y > screen_height - 20:
            self.y = screen_height - 20
            self.velocity = (self.velocity[0], -self.velocity[1] / 1.1)

        # Check for collisions with other dots
        for other_dot in all_dots:
            if other_dot != self and self.check_collision(other_dot):
                # Handle the collision (you can adjust this based on your needs)
                self.velocity = (-self.velocity[0], -self.velocity[1])
                other_dot.velocity = (-other_dot.velocity[0], -other_dot.velocity[1])

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), 2)  # Draw a small circle for the dot

