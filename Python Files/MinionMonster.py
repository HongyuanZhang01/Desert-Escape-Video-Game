import pygame, random

pygame.init()

class MonsterMinions(pygame.sprite.Sprite):
    """small enemy class in display"""
    def __init__(self, all_sprites, minion_sprite_group, windowH, Popup):
        """initializes the minions"""
        super().__init__()
        #Set values and initialize sprite groups within class
        self.current_sprite = 0
        self.windowH = windowH
        self.minion_sprite_group = minion_sprite_group
        self.all_sprites = all_sprites
        self.Popup = Popup
        self.animate_death = False

        #Randomly decide minion color based on random int
        colorList = ["Aqua", "BluishGreen", "Sandy"]
        color = random.randint(0,2)

        #Animation frames
        self.spawn_sprites = []
        self.die_sprites = []
        self.idle_sprites = []

        #Load idle images
        for w in range(22):
            self.idle_sprites.append(pygame.transform.scale(pygame.image.load("Images/Minion Blobs/"+colorList[color]+"/Idle/tile"+str(w)+".png"), (46,46)))

        #Load Popup images
        for w in range(21):
            self.spawn_sprites.append(pygame.transform.scale(pygame.image.load("Images/Minion Blobs/"+colorList[color]+"/Popup/tile0.png"), ((w+.5)*2.5,(w+.5)*2.5)))

        #Load Death images
        for sprites in self.spawn_sprites:
            self.die_sprites.insert(0, sprites)

        #Creates blob and gives it a rect based on chosen int
        self.image = self.spawn_sprites[self.current_sprite]
        self.rect = self.image.get_rect()
        self.rect.left = random.randint(64, 800)
        self.rect.bottom = random.randint(64, 550)

        #Create Minion Blob mask
        self.mask = pygame.mask.from_surface(self.image)
        

    def update(self):
        """Update the minion"""
        #Check to animate a blob
        self.check_animations()

        #Update the blob's mask
        self.mask = pygame.mask.from_surface(self.image)
        

    def check_animations(self):
        """Check if animations should run"""
        #Check if needed to run death frames or popup frames
        if self.Popup:
            self.animate(self.spawn_sprites, 0.9)
        elif self.animate_death:
            self.animate(self.die_sprites, 0.9)
        else:
            self.animate(self.idle_sprites, 0.5)


    def animate(self, sprite_list, speed):
        """animates the minion"""
        keys = pygame.key.get_pressed()
        #If animation is death frames; kill blob
        if self.animate_death:
            self.kill()
            return
        #Runs frames
        if self.current_sprite < len(sprite_list) - 1:
            self.current_sprite += speed
        else:
            self.current_sprite = 0
            if self.Popup:
                self.Popup = False
        if keys[pygame.K_SPACE]:
            self.current_sprite = 0
        
        #Assigns new frame to blob
        self.image = sprite_list[int(self.current_sprite)]