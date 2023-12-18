
import pygame
import sys
import random
from time import clock
import math  # TO calculate  gravity and sin , cos for the functions

WIDTH = 1200  # width of the game window
HEIGHT = 750  # height of the game window
pause = False  # variable which is used to determine whether the game is paused or not


pygame.init()
large_text = pygame.font.SysFont("Century", 50)
myfont = pygame.font.SysFont('Comic', 25)
alert_large = pygame.font.SysFont("Century", 35)
screen = pygame.display.set_mode((WIDTH, HEIGHT))

clock_game = pygame.time.Clock()

pygame.font.init()  # you have to call this at the start if you want to use this module.

# Background
class Background(pygame.sprite.Sprite):  # class for the background image
    def __init__(self, image_file, location):
        pygame.sprite.Sprite.__init__(self)  # sprite and how to use it  came from here   REFERENCE     https://www.youtube.com/watch?v=jMe7xQACb8U
        self.image = pygame.image.load(image_file)
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location  # the location of the image should be inputted as a tuple (x,y)



# only the lander
class Lander(pygame.sprite.Sprite):  # class for the lander image
    def __init__(self, image_file, location):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(image_file)
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location  # the location of the image should be inputted as a tuple (x,y)
        self.rot_image = self.image
        self.angle = 0
        self.veloc_y = random.random()
        self.veloc_x = random.randrange(-1,1)
        self.fuel = 500
        self.altitude = 0
        self.damage = 0
        self.random_alert = 0  # Will carry alert time
        self.random_key = 0  # Will holds key value
        self.pause_game = False


    def free_fall(self):
        self.rect.y += self.veloc_y
        self.rect.x += self.veloc_x             # we assume no wind
        self.veloc_y += 0.1

    def reset_stats(self):
        self.rect.top = 0
        self.veloc_y = random.random()
        self.veloc_x = random.randrange(-1,1)
        self.fuel = 500
        self.angle = 0
        self.damage = 0
        self.rot_image = pygame.transform.rotate(self.image, self.angle)

    def check_boundaries(self):
        if self.rect.top < 0:
            self.rect.top = 0
            self.veloc_y = random.random()
        if self.rect.right < 0:
            self.rect.left = WIDTH
        if self.rect.left > WIDTH:
            self.rect.right = 0
        if self.rect.bottom > HEIGHT:
            self.reset_stats()
            self.rect.left = random.randint(0, 1123)
            return True
        else:
            return False

    def get_fuel(self):
        return self.fuel

    def burn_fuel(self):
        self.fuel=self.fuel-5

    def start_engine(self):
        self.burn_fuel()
        self.veloc_x = self.veloc_x + 0.33 * math.sin(math.radians(-self.angle))                    #  velocity calcuation
        self.veloc_y = self.veloc_y - 0.33 * math.cos(math.radians(self.angle))

    def rotate_right(self):
        self.angle -= 1 % 360
        self.rot_image = pygame.transform.rotate(self.image, self.angle)

    def rotate_left(self):
        self.angle += 1 % 360
        self.rot_image = pygame.transform.rotate(self.image, self.angle)

    def to_ground(self):
        self.altitude = 1000 - self.rect.top
        return self.altitude

    def get_damage(self):
        return self.damage

    def get_alert(self):  # Set a new alert time and return it
        self.random_alert = random.randint(int(clock()), int(clock() + 15))
        return self.random_alert

    def get_key(self):  # Randomize and return key value
        self.random_key = random.randint(1, 3)
        return self.random_key

    def check_landing(self, pad):
        if self.veloc_y<5:
            if self.veloc_x <5 and self.veloc_x>-5:
                if -7<=self.angle<=7 :
                    if self.rect.left > pad.rect.left and self.rect.right < pad.rect.right:
                        if self.rect.bottom == pad.rect.top:
                            return True

# only the engine
class Engine(pygame.sprite.Sprite):  # class for the thrust image
    def __init__(self, image_file, location):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(image_file)
        self.rot_image = self.image
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location  #  (x,y)

        self.thrst_angle = lander.angle

    def rotate_thrust(self): #                                         REFERENCE https://www.pygame.org/wiki/RotateCenter?parent=CookBook
        self.rot_image = pygame.transform.rotate(self.image, self.thrst_angle)


# landing pad , pipes , and their interaction
class Object(pygame.sprite.Sprite):  # class for the obstacle and padzimages
    def __init__(self, image_file, location):
        pygame.sprite.Sprite.__init__(self)  # call Sprite initializer
        self.image = pygame.image.load(image_file)
        self.pad_image = pygame.image.load(image_file)

        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location  # (x,y)  y is the top postion

        self.destroyed = False

        # for the pads


    def get_status(self):  # Return the status of the obstacle
        return self.destroyed

    def obstacle_collision(self, lander):  # Increment lander damage by 10 % if the meteor collides with the lander
        if lander.rect.colliderect(self.rect):
            lander.damage += 10
            return True
        else:
            return False


def resume():  # Resume the game
    global pause
    pause = False




objects = pygame.sprite.Group()  # Create obstacle sprite group
particles = pygame.sprite.Group()  # Create sprite group for background, and lander
pads = pygame.sprite.Group() # Create a sprite group for pads

background = Background('mars_background_instr.png', [0, 0])
lander = Lander('lander.png', [600, 0])



pad_1 = Object('pad.png', [860, 732])

pad_2 = Object('pad_tall.png', [500, 620])

pad_3 = Object('pad.png', [200, 650])


# create obstacles
obstacle_1 = Object('pipe_ramp_NE.png', [90, 540])
obstacle_2 = Object('building_dome.png', [420, 575])
obstacle_3 = Object('satellite_SW.png', [1150, 435])
obstacle_4 = Object('rocks_ore_SW.png', [1080, 620])
obstacle_5 = Object('building_station_SW.png', [800, 640])

# Add to the sprite group 'obstacles'
objects.add(obstacle_1, obstacle_2, obstacle_3, obstacle_4, obstacle_5)
pads.add(pad_1,pad_2,pad_3)
particles.add(lander,background)




alert_signal = Lander('lander.png', [600, 0])  # Holds the lander system failure causes


game_status = True  # Holds the status of the game


def main():  # The main function which runs the game
    global game_status, pause,score,lives  # change name
    score=0
    lives=3

    random_signal = alert_signal.get_alert()  # Holds the randomized alert signal time
    random_key = alert_signal.get_key()  # Carries the randomized key used to decide which control failure will occur


    while game_status:  # main game loop

        clock_game.tick(25)
        screen.fill([255, 255, 255])  # Fill the empty spaces with white color

        for things in particles:                  # GENERATE THE LANDER AND BACKGROUND
                screen.blit(things.image,things.rect)

        for obstacle in objects:  #  GENERATE THE OBSTACLES
            # if a collision occurs the obstacle gets destroyed and it is no longer shown
            if not obstacle.get_status():
                screen.blit(obstacle.image, obstacle.rect)
                if obstacle.obstacle_collision(lander):
                    obstacle.destroyed = True

        for things in pads:                # GENERATE PADS
                screen.blit(things.image,things.rect)




        # Waits for an event
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

        pressed_key = pygame.key.get_pressed()  # Take pressed key value


        if pressed_key[pygame.K_ESCAPE]:  # Stop game if the 'Esc' button is pressed
            game_status = False
        elif lives==0:  # check for players lifes
            game_status = False
            score=0
        elif lander.get_fuel() <= 0:  # check fuel
            screen.blit(lander.rot_image, lander.rect)
        else:
            if not random_signal < clock() < random_signal+2:  # While has a 2 second difference
                if lander.get_damage() < 100:
                    if pressed_key[pygame.K_SPACE]:  # turns on the engine
                        thrst = Engine('thrust.png', [lander.rect.left + 30, lander.rect.bottom - 10])  # creates an engine
                        # sprite
                        lander.start_engine()
                        thrst.rotate_thrust()
                        screen.blit(thrst.rot_image, thrst.rect)
                        pygame.display.update()

                    if pressed_key[pygame.K_LEFT]:
                        lander.rotate_left()

                    if pressed_key[pygame.K_RIGHT]:
                        lander.rotate_right()

                    if lander.check_landing(pad_1) or lander.check_landing(pad_2) or lander.check_landing(pad_3):  # CHECK IF SHIP IS ON THE PAD

                        score=score+50
                        random_signal = alert_signal.get_alert()           # creates a new key and/situation for an error to occur
                        random_key = alert_signal.get_key()

                        for obstacle in objects:
                            obstacle.destroyed = False
                        lander.reset_stats()

                else:
                    lander.damage = 100  # Stop lander damage at 100 %
            else:
                alert_msg = alert_large.render('ALERT', False, (0, 0, 255))
                screen.blit(alert_msg, (190, 80))  # SHOWS THE ALERT ON THE BOARD
                if random_key == 1:                          # WHEN KEY 1 IS ROLLED SPACE WORKS AND LEFT WORKS BUT RIGHT DOESN'T
                    if pressed_key[pygame.K_SPACE]:
                        thrst = Engine('thrust.png', [lander.rect.left + 30, lander.rect.bottom - 10])
                        lander.start_engine()
                        thrst.rotate_thrust()
                        screen.blit(thrst.rot_image, thrst.rect)
                        pygame.display.update()

                    if pressed_key[pygame.K_LEFT]:
                        lander.rotate_left()
                elif random_key == 2:                #WHEN KEY 2 IS ROLLED LEFT WORKS AND RIGHT WORKS BUT SPACE DOESN'T
                    if pressed_key[pygame.K_LEFT]:
                        lander.rotate_left()

                    if pressed_key[pygame.K_RIGHT]:  #
                        lander.rotate_right()
                else:                                 # WHEN KEY 3 HAPPENS SPACE AND RIGHT WORKS BUT LEFT DOESN'T
                    if pressed_key[pygame.K_SPACE]:
                        thrst = Engine('thrust.png', [lander.rect.left + 30, lander.rect.bottom - 10])
                        lander.start_engine()
                        thrst.rotate_thrust()
                        screen.blit(thrst.rot_image, thrst.rect)
                        pygame.display.update()

                    if pressed_key[pygame.K_RIGHT]:
                        lander.rotate_right()

        screen.blit(lander.rot_image, lander.rect)




        time_passed = myfont.render(format(round(clock(),2))+'/s', False, (255, 0, 0))            # REFERENCE https://stackoverflow.com/questions/20842801/how-to-display-text-in-pygame
        screen.blit(time_passed, (72, 10))  # Display clock in seconds


        velocity_y = myfont.render(format(round(lander.veloc_y, 2)) + 'm/s', False, (255, 0, 0))
        screen.blit(velocity_y, (280, 56))  # DISPLAY THE Y VALUE OR THE SPEED GOING DOWNARDS

        velocity_x = myfont.render(format(round(lander.veloc_x, 2)) + 'm/s', False, (255, 0, 0))
        screen.blit(velocity_x, (280, 33))  # DISPLAY THE HORIZONTAL SPEED

        fuel_remaining = myfont.render(format(lander.fuel) + 'kg', False, (255, 0, 0))
        screen.blit(fuel_remaining, (72, 33))  # REMAINING FUEL

        altitude = myfont.render(format(lander.to_ground()) + 'm', False, (255, 0, 0))
        screen.blit(altitude, (280, 10))  # DISPLAY ATITUDE

        lander_damage = myfont.render(format(lander.get_damage()) + '%', False, (255, 0, 0))
        screen.blit(lander_damage, (95, 56))  # DISLAY DAMAGE TAKEN

        game_score = myfont.render(format(score), False, (255, 0, 0))
        screen.blit(game_score, (77, 82))  # DISPLAY SCORE

        lander.free_fall()  # GRAVITY FROM LANDER CLASS

        if lander.check_boundaries():

            random_signal = alert_signal.get_alert()
            random_key = alert_signal.get_key()  # Get a new random key
            lives=lives-1  # Reduce lives with 1

            for obstacle in objects:  # Reset all obstacles and make them visible
                obstacle.destroyed = False


            pause = True  # Set 'pause' to True so the game pauses when 'paused' method is called
            crash_msg = large_text.render('GAME OVER YOU DIED!', False, (255, 0, 0))
            screen.blit(crash_msg, (420, 300))

            while pause==True:
                for event in pygame.event.get():

                    if event.type == pygame.KEYDOWN:  # Wait for a key to be pressed and if so resumes the game
                        resume()

                pygame.display.update()
                clock_game.tick(25)

        pygame.display.update()

    pygame.quit()  # quit game if game_status when its False


main()

