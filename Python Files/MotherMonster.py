import pygame, random
import MonsterProjectile

pygame.init()   

class motherMonster(pygame.sprite.Sprite):
    """represents the mother monster"""

    def __init__(self,all_sprites,mother_sprite_group, Monsterprojectile_group,windowH,player_sprite_group,difficultyLevel):
        """initialize the mother monster"""
        #Takes in all assets from pygame sprite class (inheritance)
        super().__init__()
        #Set constant variables
        #Determine velocity based on selected level
        if difficultyLevel == 99:
            self.velocity = 2
        else:
            self.velocity = 3
        self.windowH = windowH
        self.starting_health = 250

        #Determine MotherMonster health based on selected level
        if difficultyLevel == 99:
            self.health = self.starting_health
        else:
            self.health = self.starting_health+100

        #Attach sprite groups
        self.all_sprites = all_sprites
        self.mother_sprite_group = mother_sprite_group
        self.Monsterprojectile_group = Monsterprojectile_group
        self.player_sprite_group = player_sprite_group
        self.difficultyLevel = difficultyLevel

        #determine up and down motion
        self.dy = random.choice([-1, 1])

        #Declare Animation booleans
        self.animate_death = False
        self.animate_fire = False

        #Create MotherMonster's image and give it a rect
        self.image = pygame.image.load("Images/Miscellaneous/MotherMonster.png")
        self.rect = self.image.get_rect()
        self.rect.center = (900, self.windowH//2)

    
    def update(self):
        """updates the mother monster"""
        self.move()        
        #Randomly fire a bullet
        if random.randint(-50, 100) > self.difficultyLevel and len(self.Monsterprojectile_group) < 10:
            self.fire()

    def fire(self):
        """fires mother monster projectile"""
        #Generates and calls the MonsterProjectile class
        MonsterProjectile.MonsterProjectile(self.rect.centerx, self.rect.centery, self.player_sprite_group, self.Monsterprojectile_group)

    def move(self):
        """move the mother monster"""
        #Move the monster depending on the delta direction by x velocity
        self.rect.y += self.dy*self.velocity

        #Restrict to edge of screen
        if self.rect.top <= 0:
            self.dy = -1*self.dy
        elif self.rect.bottom >= 600:
            self.dy = -1*self.dy

    def reset(self):
        """reset the mother monster"""
        #Puts mother monster in the middle of the screen and chooses a new delta direction
        self.rect.center = (900,self.windowH//2)
        self.dy = random.choice([-1, 1])