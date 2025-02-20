import pygame, random, MinionMonster, Buttons
pygame.init()

class Game():
    """Helps run and monitor the game"""
    def __init__(self, player, display_surface, player_sprite_group, all_sprites, mother_sprite_group, minion_sprite_group, Playerprojectile_sprite_group, Motherprojectile_sprite_group, FPS, clock, windowH, windowW, MotherMonster, current_scene,difficultyLevel):
        """initialize the game"""
        #Attach sprite groups and player
        self.MotherMonster = MotherMonster
        self.player_sprite_group = player_sprite_group
        self.all_sprites = all_sprites
        self.mother_sprite_group = mother_sprite_group
        self.minion_sprite_group = minion_sprite_group
        self.Playerprojectile_sprite_group = Playerprojectile_sprite_group
        self.Motherprojectile_sprite_group = Motherprojectile_sprite_group
        self.windowW = windowW
        self.windowH = windowH
        self.display_surface = display_surface
        self.player = player
        self.difficultyLevel = difficultyLevel

        #Set sounds
        self.PlayerHit_sound = pygame.mixer.Sound("Audio/PlayerHit.wav")
        self.MonsterHit_sound = pygame.mixer.Sound("Audio/MonsterHit.wav")
        self.MonsterPowerUp_sound = pygame.mixer.Sound("Audio/MonsterPowerUp.wav")
        self.BlobDeath_sound = pygame.mixer.Sound("Audio/BlobDeath.wav")

        #Set time values
        self.FPS = FPS
        self.clock = clock

        #Set constant variables
        self.starting_boost_time = 15
        self.safeTime = 10

        #Game values
        self.score = 0
        self.round_number = 1
        self.frame_count = 0
        self.boost_time = self.starting_boost_time
        self.round_time = 0
        self.Reset = False
        self.current_scene = current_scene
        self.Win = "None"

        #Set fonts
        self.EvilEmpireFont = pygame.font.Font("Fonts/EvilEmpire.ttf", 30)
        self.titleFont = pygame.font.Font("Fonts/EvilEmpire.ttf", 90)
        self.BigSpaceFont = pygame.font.Font("Fonts/BigSpace.ttf", 30)


    def update(self):
        """Updates Game"""
        if not self.Reset:
            self.frame_count += 1
            if self.frame_count % self.FPS == 0: 
                self.round_time += 1 
                self.boost_time -= 1
                self.frame_count = 0

            self.draw()
            self.check_game_status()
            self.check_collisions()
            self.add_blob()
            self.buff_mother_monster()
            

    def add_blob(self):
        """Adds a blob to the game"""
        
        #Check to add a blob every [time interval] seconds
        self.speed = 10
        self.speedCheck = True
        if self.MotherMonster.difficultyLevel <= 95:
            self.safeTime = 5
            self.speed += (95-self.MotherMonster.difficultyLevel)
        if not self.Reset:
            if self.frame_count % self.FPS*self.speed == 0:
                #Add a blob only when safeTime has passed
                if self.round_time % self.safeTime == 0:
                    blob = MinionMonster.MonsterMinions(self.all_sprites, self.minion_sprite_group, self.windowH, True)
                    self.minion_sprite_group.add(blob)

                    if self.speedCheck:
                        if self.speed <= 0:
                            self.speedCheck = False
                            self.speed = 1.5
                        else:
                            self.speed -= 0.5


    def draw(self):
        """draws HUD and other game objects"""
        #Set colors
        BLACK = (0, 0, 0)
        LIGHT_GRAY = (130, 133, 122)
        ORANGE = (230, 142, 76)
        
        #Draw rect around HUD
        pygame.draw.rect(self.display_surface, LIGHT_GRAY, pygame.Rect(0, 600, 1200, 100))
        #Draw rect around MotherMonster HP
        pygame.draw.rect(self.display_surface, ORANGE, pygame.Rect(940, 550, 250, 50))

        #Set text
        health_text = self.BigSpaceFont.render("Health: " + str(self.player.health), True, BLACK)
        health_rect = health_text.get_rect()
        health_rect.bottomleft = (10, self.windowH - 5)

        title_text = self.titleFont.render("Desert Escape!", True, BLACK)
        title_rect = title_text.get_rect()
        title_rect.center = (self.windowW//2, self.windowH - 42)     

        time_text = self.EvilEmpireFont.render("Monster Boost in: " + str(self.boost_time), True, BLACK)
        time_rect = time_text.get_rect()
        time_rect.bottomright = (self.windowW - 10, self.windowH - 5)

        MonsterHealth = self.EvilEmpireFont.render("Monster Health: " + str(self.MotherMonster.health), True, BLACK)
        MonsterHealth_rect = MonsterHealth.get_rect()
        MonsterHealth_rect.bottomright = (self.windowW - 12, self.windowH - 110)

        #Draw the HUD
        self.display_surface.blit(health_text, health_rect)
        self.display_surface.blit(title_text, title_rect)
        self.display_surface.blit(time_text, time_rect)
        self.display_surface.blit(MonsterHealth, MonsterHealth_rect)


    def check_collisions(self):
        """checks for all collisions that affect gameplay (ex. minions, player, projectiles, mother monster's)"""
        #Check for collisions between Blobs and player arrows
        collision_dict = pygame.sprite.groupcollide(self.Playerprojectile_sprite_group, self.minion_sprite_group, True, True, pygame.sprite.collide_mask)
        if collision_dict:
            for sprites in collision_dict.values():
                for sprite in sprites:
                    #-> Add sounds
                    self.BlobDeath_sound.play()
                    #sprite.is_dead = True
                    sprite.animate_death = True

        #Check for collisions between player and Mother Monster's projectiles
        collision_dict1 = pygame.sprite.spritecollide(self.player, self.Motherprojectile_sprite_group, False)
        if collision_dict1:
            for projectile in collision_dict1:
                #Play player hit sound
                self.PlayerHit_sound.play()
                #Destroys projectile
                projectile.kill()
            #Takes away player health
            self.player.health -=  random.randint(5,10)

        #Check for collisions between player and blobs
        collision_dict2 = pygame.sprite.spritecollide(self.player, self.minion_sprite_group, False,pygame.sprite.collide_mask)
        if collision_dict2:
            for blob in collision_dict2:
                #Player player hit sound
                self.BlobDeath_sound.play()
                #Destroy blob in contact
                blob.kill()
                self.player.position = (blob.rect.centerx, blob.rect.centery - 70)
            self.player.health -= random.randint(1,10)
        
        #Check for collision between playerProjectiles and MotherMonster
        collision_dict3 = pygame.sprite.spritecollide(self.MotherMonster,self.Playerprojectile_sprite_group, False, pygame.sprite.collide_mask)
        if collision_dict3:
            for projectile in collision_dict3:
                #Plays monster hit sound effect
                self.MonsterHit_sound.play()
                #Destroys projectile in contact
                projectile.kill()
            self.MotherMonster.health -= random.randint(5,15)
            

    def check_game_status(self):
        """Checks conditions to see if needs any change is needed"""
        if self.player.health <= 0:
            self.Win = "False"
            self.reset_game()
            print("HELLO X2")
        elif self.MotherMonster.health <= 0:
            self.Win = "True"
            print("MONSTER DIEDDD")
            self.reset_game()

    def reset_game(self):
        """resets the game in the case of player losing"""
        #empty out sprite groups and player sprite groups
        self.mother_sprite_group.empty()
        self.minion_sprite_group.empty()
        self.player_sprite_group.empty()
        self.Playerprojectile_sprite_group.empty()
        self.Motherprojectile_sprite_group.empty()
        self.player.reset()

        #Resets changed values
        self.score = 0
        self.round_number = 1
        self.player.health = self.player.starting_health
        self.Reset = True
        self.boost_time = self.starting_boost_time

        #Resets MotherMonster health based on selected levels
        if self.difficultyLevel == 99:
            self.MotherMonster.health = self.MotherMonster.starting_health
        else:
            self.MotherMonster.health = self.MotherMonster.starting_health+100

    def buff_mother_monster(self):
        """buffs mother monster"""
        #Check if boost time is up
        if self.boost_time == 0:
            #Plays Monster power up sound
            self.MonsterPowerUp_sound.play()
            #Increases MotherMonster's velocity
            self.MotherMonster.velocity = self.MotherMonster.velocity*1.1
            #Makes MotherMonster's bullets 2% more likely to fire
            self.MotherMonster.difficultyLevel -= self.MotherMonster.difficultyLevel*0.02
            #Resets boost time to starting_boost_time
            self.boost_time = self.starting_boost_time