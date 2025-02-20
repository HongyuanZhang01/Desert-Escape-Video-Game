import pygame, random
pygame.init()

class MonsterProjectile(pygame.sprite.Sprite):
    """represents the monster's fired projectiles"""

    def __init__(self, x, y, player_sprite_group, projectile_group):
        """initilizes the monster's projectile"""
        #Takes in all assets from pygame sprite class (inheritance)
        super().__init__()

        #set constant variables
        self.range = 1000
        self.player_sprite_group = player_sprite_group

        #Non-constant variables
        self.vel = random.randint(3,8) #vel = velocity

        #Initialize sprite groups
        self.projectile_group = projectile_group

        #Initialize positions
        self.x = x
        self.y = y
        #Draw the projectile and get rect
        self.image = pygame.transform.scale(pygame.image.load("Images/Miscellaneous/MonsterProjectile.png"),(30,15))
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)

        #Add to projectile sprite group
        projectile_group.add(self)

    
    def update(self):
        """Updates the monster's projectile"""
        self.move()

    def move(self):
        """move the monster's projectile"""
        self.rect.x -= self.vel
        #If projectile exceeds range -> kill it
        if abs(self.rect.x - self.x) > self.range:
            self.kill()
        