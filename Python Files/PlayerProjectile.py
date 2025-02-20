import pygame

pygame.init()

class playerProjectile(pygame.sprite.Sprite):
    """represents the player's fired projectiles"""

    def __init__(self,x, y, projectile_group, player,all_sprites,current_frame):
        """initilizes the player's projectile"""
        #Takes in all assets from pygame sprite class (inheritance)
        super().__init__()
        
        #set constant variables
        self.vel = 6 # vel = velocity
        self.range = 2000
        self.all_sprites = all_sprites
        self.current_frame = current_frame

        #generate the projectile relative to direction
        if player.velocity.x > 0:
            self.image = pygame.transform.scale(pygame.image.load("Images/Sprite Weapon/arrowProjectile.png"), (64,64))
        else:
            self.image = pygame.transform.scale(pygame.transform.flip(pygame.image.load("Images/Sprite Weapon/arrowProjectile.png"),True,False), (64,64))
            self.vel = -1*self.vel
            #Get rect for projectile
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.mask = pygame.mask.from_surface(self.image)

        self.starting_x = x
    
        projectile_group.add(self)
        

    def update(self):
        """Updates the player's projectile"""
        self.move()
        #Update the players mask
        self.mask = pygame.mask.from_surface(self.image)

    def move(self):
        """move the player's projectile"""
        self.rect.x += self.vel
        #if projectile is out of range -> kill it
        if abs(self.rect.x - self.starting_x) > self.range:
            self.kill()