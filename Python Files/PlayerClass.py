import pygame, PlayerProjectile

pygame.init()

#Install the vector math function
vector = pygame.math.Vector2

class Player(pygame.sprite.Sprite):
    """represents and controls player"""

    def __init__(self, x, y,projectile_group,windowW,windowH,all_sprites):
        """initialize the player"""
        #Takes in all assets from pygame sprite class (inheritance)
        super().__init__()

        #constant variables
        self.horizontal_accel = 0.5
        self.friction = 0.15
        self.starting_health = 100
        self.vertical_accel = 0.5
        self.windowW = windowW
        self.windowH = windowH
        self.lastDirection = 1
        self.all_sprites = all_sprites

        #Set values
        self.shots = 0

        #Animation frames
        self.move_right = []
        self.move_left = []
        self.idle_right = []
        self.idle_left = []
        self.attack_left = []
        self.attack_right = []
        self.die_right = []
        self.die_left = []

        #import move right frames
        for w in range(5):
            self.move_right.append(pygame.transform.scale(pygame.image.load("Images/Sprite Run/adventurer-run-0"+str(w)+".png"), (64,64)))
        #import move left frames
        for sprite in self.move_right:
            self.move_left.append(pygame.transform.flip(sprite, True, False))
        #import idle right frames
        for w in range(3):
            self.idle_right.append(pygame.transform.scale(pygame.image.load("Images/Sprite Idle/adventurer-idle-0"+str(w)+".png"), (64,64)))
        #import idle left frames
        for sprite in self.idle_right:
            self.idle_left.append(pygame.transform.flip(sprite, True, False))

        #import attack right frames
        for w in range(6):
            self.attack_right.append(pygame.transform.scale(pygame.image.load("Images/Sprite Weapon/adventurer-bow-0"+str(w)+".png"), (64,64)))
        
        #import attack left frames
        for sprite in self.attack_right:
            self.attack_left.append(pygame.transform.flip(sprite,True,False))
        
        #import death frames right
        for w in range(6):
            self.die_right.append(pygame.transform.scale(pygame.image.load("Images/Sprite Die/adventurer-die-0"+str(w)+".png"), (64,64)))
        #import death frames left
        for sprite in self.die_right:
            self.die_left.append(pygame.transform.flip(sprite,True,False))

        #Load image and get rect
        self.current_sprite = 0
        self.current_projectile_frame = self.current_sprite
        self.image = self.idle_right[self.current_sprite]
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

        #Attach sprite groups
        self.projectile_group = projectile_group

        #Load sounds
        self.fire_sound = pygame.mixer.Sound("Audio/PlayerFire.wav")

        #Animation booleans
        self.animate_fire = False

        #Kinematics vectors 
        self.position = vector(x ,y)
        self.velocity = vector(0, 0)
        self.acceleration = vector(0, 0)

        #Initial player values
        self.health = self.starting_health
        self.startingX = x
        self.startingY = y
        
    def update(self):
        """updates the player"""
        #Create and update player mask        
        self.mask = pygame.mask.from_surface(self.image)
        #Draw the mask
        mask_outline = self.mask.outline()
        pygame.draw.lines(self.image,(255,255,0), True, mask_outline)

        #Update
        self.move()
        self.check_animations()


    def fire(self):
        """fires player projectile"""
        #Plays fire sound
        self.fire_sound.play()
        #Fires projectile by generating projectile through playerProjectile class
        PlayerProjectile.playerProjectile(self.rect.x+15, self.rect.y+40,self.projectile_group, self, self.all_sprites,self.current_projectile_frame)
        self.animate_fire = True


    def move(self):
        """move the player"""
        #Sets acceleration vector
        self.acceleration = vector(0, 0)
        #Movements
        movement = True
        #Gets list of keys that are pressed
        self.keys = pygame.key.get_pressed()
        #See if left arrow or a key are pressed
        if self.keys[pygame.K_LEFT] or self.keys[pygame.K_a]:
            movement = False
            #See if character is inside boundaries relevant to direction
            if self.rect.left > 20:
                #Changes acceleration (x) to left
                self.acceleration.x = -1*self.horizontal_accel
                #Animates the change by running move_left frames
                self.animate(self.move_left, 0.5)
                #Sets last direction to 0: meaning left
                self.lastDirection = 0
        #See if right arrow or d key are pressed
        elif self.keys[pygame.K_RIGHT] or self.keys[pygame.K_d] and movement:
            movement = False
            #See if character is inside boundaries relevant to direction
            if self.rect.right < self.windowW - 750:
                #Change acceleration (x) to right
                self.acceleration.x = self.horizontal_accel
                #Animates change by running move_right frames
                self.animate(self.move_right, 0.5)
                #Sets last direction to 1: meaning right
                self.lastDirection = 1
        #See if up arrow or w key are pressed
        elif self.keys[pygame.K_UP] or self.keys[pygame.K_w] and movement:
            movement = False
            #See if character is inside boundaries relevant to direction
            if self.rect.top > 50:
                #Change acceleration (y) to up
                self.acceleration.y = -1*self.vertical_accel
                #Determines which side idle frames character should run while moving up
                if self.lastDirection == 1:
                    self.image = self.idle_right[0]
                else:
                    self.image = self.idle_left[0]
        #See if down arrow or s key is pressed
        elif self.keys[pygame.K_DOWN] or self.keys[pygame.K_s] and movement:
            movement = False
            #See if character is inside boudnaries relevant to direction
            if self.rect.bottom < self.windowH - 130:
                #Change acceleration (y) to down
                self.acceleration.y = self.vertical_accel
                #Determines which side idle frames character should run while moving up
                if self.lastDirection == 1:
                    self.image = self.idle_right[0]
                else:
                    self.image = self.idle_left[0]

        #Calculate New position (kinematic value)
        self.acceleration -= self.velocity*self.friction
        self.velocity += self.acceleration
        self.position += self.velocity + 0.5*self.acceleration

        #Update rect based on kinematic calculations
        self.rect.topleft = self.position

    def check_animations(self):
        """Checks if any player animations are needed"""
        #Check if animation fire is needed to run
        if self.animate_fire:
            if self.velocity.x > 0:
                self.animate(self.attack_right, 0.1)
            else:
                self.animate(self.attack_left, 0.1)

    def reset(self):
        """reset the player position"""
        #Changes velocity vector and positional vector to original values
        self.velocity = vector(0,0)
        self.position = vector(self.startingX, self.startingY)
        #Attaches new positional (original values) to rect
        self.rect.topleft = self.position
        #(rect autmatically applies to the mask of player)

    def animate(self,sprite_list, speed):
        """animates the player"""
        #Changes frames depending on speed
        if self.current_sprite < len(sprite_list) - 1:
            self.current_sprite += speed
        else:
            self.current_sprite = 0
            #End fire animation
            if self.animate_fire:
                self.animate_fire = False
        #If SPACE: current_sprite is now 0
        if self.keys[pygame.K_SPACE]:
            self.current_sprite = 0
        
        #Attaches new frame (img) to player
        self.image = sprite_list[int(self.current_sprite)]