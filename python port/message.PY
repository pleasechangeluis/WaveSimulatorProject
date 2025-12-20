import pygame
import random
import math
import time
import _thread
import multiprocessing
from multiprocessing import pool

pygame.init()

WIDTH = 1920
HEIGHT = 1080

frame_count = 0
frame_rate = 240  # Frames per second of the program
round_amount = 1  # Accuracy of displayed numbers
updates_per_second = 30  # Simulation frame rate, performance impact
sim_speed = 1  # Simulation time steps per simulation frame, performance impact
loss_coefficient = 2 # Abstract loss of energy, needs to be elaborated on. 0 is off.
voxel_size = 40  # Resolution of simulation
energy_added_on_click = 100 #obvious

partition = []
partition_size = 4

voxel = []
update_space_list = []
update_space_queue = []
voxel_width = WIDTH / voxel_size
voxel_height = HEIGHT / voxel_size

screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
running = True


# classes and (FUN)ctions

class Space:

    def __init__(self, value, pos):
        self.value = value
        self.pos = pos
        self.adjacent = []
        self.velocity = 0

    def update(self):

        self.value += self.velocity / updates_per_second

        self.add_force(-self.value / updates_per_second)


        if self in update_space_list:
            for neighbor in self.adjacent:
                neighbor.add_force(self.velocity / (len(self.adjacent)))

        self.add_force(-self.velocity - (self.value / updates_per_second))

        self.value -= self.value * (loss_coefficient/updates_per_second)



    def add_force(self, force):
        self.velocity += force

#        if (math.fabs(self.velocity)) <= 0 and (math.fabs(self.value)) <= 0:
#            self.value = 0
#            self.velocity = 0
#            if self in update_space_list:
#                update_space_list.remove(self)
#        elif self not in update_space_list and self not in update_space_queue:
#            update_space_queue.append(self)


font = pygame.font.Font('freesansbold.ttf', 16)

for i in range(voxel_size):
    voxel.append([])
    for j in range(voxel_size):
        space = Space(0, (i, j))
        voxel[i].append(space)

for i in range(voxel_size):
    for j in range(voxel_size):
        update_space_list.append(voxel[i][j])
        for p in range(-1, 2):
            for k in range(-1, 2):
                if (0 > i + p or i + p >= voxel_size) or (0 > j + k or j + k >= voxel_size) or (p == 0 and k == 0):
                    continue
                voxel[i][j].adjacent.append((voxel[i + p][j + k]))

for i in range((voxel_size**2)//partition_size):
    partition.append([])
print("partition size:", len(partition))



counter = 0
side_length = math.floor(partition_size ** 1 / 2)
for s1 in range(side_length):
    for s2 in range(side_length):
        for i in range(side_length):
            for j in range(side_length):
                x = (s1*side_length) + i
                y = (s2*side_length) + j
                partition[counter].append(voxel[x][y])
                if (i == 0 or i == side_length - 1) or (j == 0 or j == side_length - 1):
                    temp_voxel = []
                    if i == 0 and j == 0:
                        if x - 1 > 0:
                            temp_voxel.append(voxel[x - 1][y])
                        if y - 1 > 0:
                            temp_voxel.append(voxel[x][y - 1])
                        if x - 1 > 0 and y - 1 > 0:
                            temp_voxel.append(voxel[x - 1][y - 1])
                    elif i == side_length - 1 and j == 0:
                        if x + 1 < voxel_size:
                            temp_voxel.append(voxel[x + 1][y])
                        if y - 1 > 0:
                            temp_voxel.append(voxel[x][y - 1])
                        if x + 1 < voxel_size and y - 1 > 0:
                            temp_voxel.append(voxel[x + 1][y - 1])
                    elif i == 0 and j == side_length - 1:
                        if x - 1 > 0:
                            temp_voxel.append(voxel[x - 1][y])
                        if y + 1 < voxel_size:
                            temp_voxel.append(voxel[x][y + 1])
                        if x - 1 > 0 and y + 1 < voxel_size:
                            temp_voxel.append(voxel[x - 1][y + 1])
                    elif i == side_length - 1 and j == side_length - 1:
                        if x + 1 < voxel_size:
                            temp_voxel.append(voxel[x + 1][y])
                        if y + 1 < voxel_size:
                            temp_voxel.append(voxel[x][y + 1])
                        if x + 1 < voxel_size and y + 1 < voxel_size:
                            temp_voxel.append(voxel[x + 1][y + 1])
                    else:
                        if i == 0 and x - 1 > 0:
                            temp_voxel.append(voxel[x - 1][y])
                        elif i == side_length - 1 and x + 1 < voxel_size:
                            temp_voxel.append(voxel[x + 1][y])
                        elif j == 0 and y - 1 > 0:
                            temp_voxel.append(voxel[x][y - 1])
                        elif j == side_length - 1 and y + 1 < voxel_size:
                            temp_voxel.append(voxel[x][y + 1])
                    partition[counter].extend(temp_voxel)

        counter += 1

for part in partition:
    print("next partition")
    for i in range(len(part)):
        print(part[i].pos)
    print(len(part))


def update_partition(partition_number):
    for temp in partition[partition_number]:
        temp.update()

def load_changes():
    for indexical in range(partition_size):
        p = multiprocessing.Process(target=update_partition, args=(indexical,))
        p.start()
       # p.join()


# runtime
while running:
    screen.fill((0, 0, 0))
    # update variables
    voxel_width = WIDTH / voxel_size
    voxel_height = HEIGHT / voxel_size
    m_x = pygame.mouse.get_pos()[0]
    m_y = pygame.mouse.get_pos()[1]
    selected_space = (0, 0)
    voxel_color = (75, 75, 75)
    # no more!!

    if frame_count % (frame_rate // updates_per_second) == 0:
        for space in update_space_list:
            space.update()

    for i in range(voxel_size):  # go through each space
        temp_x_loc = voxel_width * i
        temp_y_loc = voxel_height * i

        for j in range(voxel_size):
            temp_x2_loc = voxel_width * j
            temp_y2_loc = voxel_height * j
            color_coefficient = 255
            r = min(math.fabs(min((voxel[i][j].value, 0))) * color_coefficient, 255)
            b = min(math.fabs(max((voxel[i][j].value, 0))) * color_coefficient, 255)

            pygame.draw.polygon(screen, (r, 0, b),
                                # rect LOOKED funny so I did POLYGON instead :D
                                [(temp_x_loc, temp_y2_loc), (temp_x_loc, temp_y2_loc + voxel_height),
                                 (temp_x_loc + voxel_width, temp_y2_loc + voxel_height),
                                 (temp_x_loc + voxel_width, temp_y2_loc)])

            if temp_x_loc <= m_x <= temp_x_loc + voxel_width and temp_y2_loc <= m_y <= temp_y2_loc + voxel_height:
                pygame.draw.circle(screen, (0, 100, 0),
                                   (temp_x_loc + voxel_width / 2, temp_y2_loc + voxel_height / 2), 10)
                selected_space = (i, j)

            # draw value on each space
    #        screen.blit(font.render(str(round(voxel[i][j].value, round_amount)), False, voxel_color),
    #                    (temp_x_loc + voxel_width / 2 - 4, temp_y2_loc + voxel_height / 2 - 7))

    #        pygame.draw.line(screen, voxel_color, (temp_x_loc, 0), (temp_x_loc, HEIGHT))
    #        pygame.draw.line(screen, voxel_color, (0, temp_y_loc), (WIDTH, temp_y_loc)) #draws lines
    #    pygame.draw.line(screen, voxel_color, (WIDTH - 1, 0), (WIDTH - 1, HEIGHT))
    #    pygame.draw.line(screen, voxel_color, (0, HEIGHT - 1), (WIDTH, HEIGHT - 1))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                voxel[selected_space[0]][selected_space[1]].add_force(energy_added_on_click)

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                pass

    pygame.display.flip()
    frame_count += 1
    clock.tick(frame_rate)


pygame.quit()
