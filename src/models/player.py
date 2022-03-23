import pygame
from src.resource_manager import ResourceManager


class Player(pygame.sprite.Sprite):
    def __init__(self, parent, twin, x, y):
        super().__init__()
        
        # reference to GameScene so they can access methods/data in other game objects
        self.parent = parent
        
        # Load all animations of character
        self.twin = twin
        self.img_idle = []
        self.img_walk_up = []
        self.img_walk_down = []
        for i in range(3):
            self.img_idle.append(ResourceManager().get_image("player"+self.twin+"_idle%d.png"%(i)))
        self.img_idle.append(ResourceManager().get_image("playergood_idle0.png")) # quick safety measure :)
        for i in range(4):
            self.img_walk_up.append(ResourceManager().get_image("playergoodback_walk%d.png"%(i))) # good/evil twin look same from behind :)
            self.img_walk_down.append(ResourceManager().get_image("player"+self.twin+"_walk%d.png"%(i)))
        self.image = self.img_idle[0]

        # Variables for smooth movement
        self.x = int(x)
        self.y = int(y)
        #self.rect = pygame.Rect(self.x, self.y, 32, 32)
        # Updated here to make (x,y) the center of the player's hit box
        self.rect = pygame.Rect(int(self.x)-16, int(self.y)-16-22, 32, 32)
        self.vx = 0
        self.vy = 0
        self.left_pressed = False
        self.right_pressed = False
        self.up_pressed = False
        self.down_pressed = False
        self.speed = 4
        
        # Variables to control animation
        self.aniframe = 0
        self.ani_to = 0
        self.moving = False

        # Obstacles
        #self.obstacles = obstacles

    def player_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.left_pressed = True
        else:
            self.left_pressed = False
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.right_pressed = True
        else:
            self.right_pressed = False
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.up_pressed = True
        else:
            self.up_pressed = False
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.down_pressed = True
        else:
            self.down_pressed = False

    def animation_state(self):
        self.ani_to += 1
        if self.ani_to > 3:
            self.ani_to = 0
            self.aniframe += 1
            if self.moving == True and self.aniframe > 3:
                self.aniframe = 0
            elif self.moving == False and self.aniframe > 2:
                self.aniframe = 0
                
        if self.left_pressed and not self.right_pressed:
            dx = -1 # expected change in x-direction
        elif self.right_pressed and not self.left_pressed:
            dx = 1 # expected change in x-direction
        else:
            dx = 0
        if self.up_pressed and not self.down_pressed:
            dy = -1 # expected change in y-direction
        elif self.down_pressed and not self.up_pressed:
            dy = 1 # expected change in y-direction
        else:
            dy = 0
        
        # set frames
        if dx == 0 and dy == 0:
            self.moving = False
        else:
            self.moving = True
        if dy < 0:
            self.image = self.img_walk_up[self.aniframe]
        elif dy > 0 or dx > 0 or dx < 0:
            self.image = self.img_walk_down[self.aniframe]
        else:
            self.image = self.img_idle[self.aniframe]

    def movement(self):
        self.vx = 0
        self.vy = 0
        if self.left_pressed and not self.right_pressed:
            self.vx = -self.speed
        if self.right_pressed and not self.left_pressed:
            self.vx = self.speed
        if self.up_pressed and not self.down_pressed:
            self.vy = -self.speed
        if self.down_pressed and not self.up_pressed:
            self.vy = self.speed
        self.x += self.vx
        self.y += self.vy

        # Collision (incomplete)

        # Barrier (not a good implementation of barrier, not precise because has some approximation)
        # mit-mit: updated here so (x,y) will now represent center of player hitbox, not the
        # upper left corner of the graphic
        
        # mit-mit: moved this into occmanager.HandleCollision()
        
        # handle collisions (from occupancy grid)
        if self.left_pressed and not self.right_pressed:
            dx = -1 # expected change in x-direction
        elif self.right_pressed and not self.left_pressed:
            dx = 1 # expected change in x-direction
        else:
            dx = 0
        if self.up_pressed and not self.down_pressed:
            dy = -1 # expected change in y-direction
        elif self.down_pressed and not self.up_pressed:
            dy = 1 # expected change in y-direction
        else:
            dy = 0
        (x, y) = self.parent.occmanager.HandleCollision(self.twin, self.x, self.y, dx, dy)
        self.x = x
        self.y = y

        #self.rect = pygame.Rect(int(self.x), int(self.y), 32, 32)
        # Updated here to make (x,y) the center of the player's hit box
        self.rect = pygame.Rect(int(self.x)-16, int(self.y)-16-22, 32, 32)

    def update(self):
        self.player_input()
        self.animation_state()
        self.movement()
