import pygame
import Game, MotherMonster, PlayerClass, Buttons, transparent

#Initialize pygame
pygame.init()

#Set display surface
windowW = 1200
windowH = 700
# display_surface = pygame.display.set_mode((windowW,windowH))
display_surface = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
pygame.display.set_caption("Desert Escape")

#FPS and clock
fps = 60
clock = pygame.time.Clock()

class Scenes():
    def __init__(self):
        '''initializes the entire Desert Escape Game'''
        self.current_scene = 0
        self.running = True
        self.GAME = True


    def update(self):
        '''Updates the program'''
        self.SceneManager()


    def SceneManager(self):
        '''Manages which scene should be displayed'''
        while self.GAME:
            #Chooses which scene to display
            if self.current_scene == 0:
                self.Intro()
            elif self.current_scene == 1:
                self.Desert_Escape()
            elif self.current_scene == 2:
                self.Game_won()
            #Check to display game lost screen
            elif self.current_scene == 3:
                self.Game_lost()
                self.current_scene = 4
            #Checks if current_scene exceeds 3; if true -> resets to 0
            if self.current_scene > 3:
                self.current_scene = 0


    def Intro(self):
        '''Create first scene; intro scene'''
        #Creates the buttons
        image1 = pygame.image.load("Images/Buttons/Level1Btn.png").convert_alpha()
        level1Btn = Buttons.Buttons(650, 525, image1, 0.5, display_surface)

        image2 = pygame.image.load("Images/Buttons/Level2Btn.png").convert_alpha()
        level2Btn = Buttons.Buttons(350, 525, image2, 0.5, display_surface)

        transparent_BG = pygame.image.load("Images/Miscellaneous/transparent BG.png")

        background_image2 = pygame.image.load("Images/Miscellaneous/roughBackground.png")
        background_image2 = pygame.transform.scale(background_image2, (windowW, windowH))
        background_rect2 = background_image2.get_rect()
        background_rect2.topleft = (0, 0)

        #Reset sound and init/play background sound
        pygame.mixer.music.stop()
        pygame.mixer.music.load("Audio/BG2.wav")
        pygame.mixer.music.play(-1,0.0)

        #Initializes font
        self.WhatTheFudgesticks = pygame.font.Font("Fonts/WhatTheFudgesticks.ttf", 20)
        self.titleFont = pygame.font.Font("Fonts/EvilEmpire.ttf", 90)

        #Creates parts of the storyline
        Storyline1 = self.WhatTheFudgesticks.render("You have been stranded on a cursed island. It is inhabited by a monster called the ",True,(255,255,255))
        Storyline1_rect = Storyline1.get_rect()
        Storyline1_rect.topleft = (200, 100)

        Storyline2 = self.WhatTheFudgesticks.render("Typhon, and it's blocking your escape route off the island. You're going to have to defeat ",True,(255,255,255))
        Storyline2_rect = Storyline2.get_rect()
        Storyline2_rect.topleft = (200, 130)

        Storyline3 = self.WhatTheFudgesticks.render("it if you want to survive. Typhon's offspring will constantly be spawning. Don't ",True,(255,255,255))
        Storyline3_rect = Storyline3.get_rect()
        Storyline3_rect.topleft = (200, 160)

        Storyline4 = self.WhatTheFudgesticks.render("be distracted and focus on defeating the Typhon. Best of luck!",True,(255,255,255))
        Storyline4_rect = Storyline4.get_rect()
        Storyline4_rect.topleft = (200, 190)

        #Adds all storyline parts to a dictionary
        Storyline = {
            Storyline1: Storyline1_rect,
            Storyline2: Storyline2_rect,
            Storyline3: Storyline3_rect,
            Storyline4: Storyline4_rect
        }

        #Create game title
        TitleText = self.titleFont.render("DESERT ESCAPE", True, (0,0,0))
        TitleText_rect = TitleText.get_rect()
        TitleText_rect.center = (windowW//2,windowH//2+100)

        Introrunning = True
        while Introrunning:

            #Fill in display surface --CHANGE LATER--
            display_surface.blit(background_image2, background_rect2)

            #Draw Decor basic shapes
            transparent.blit_alpha(display_surface, transparent_BG, (110, 70), 170)
            pygame.draw.line(display_surface, (0,0,0), (300,500), (900,500), 10)

            #Draw text onto screen (Storyline) by using key and values of dictionary
            for keys, value in Storyline.items():
                display_surface.blit(keys, value)

            #Draw Other text onto the screen
            display_surface.blit(TitleText,TitleText_rect)

            #Check if level 1 button is pressed (returns true)
            if level1Btn.update(display_surface):
                self.level = 99
                print("CHECKED CONDITION IS TRUEEEE (1)")
                self.current_scene = 1
                Introrunning = False

            #Check if level 2 button is pressed (returns true)
            if level2Btn.update(display_surface):
                self.level = 95
                print("CHECKED CONDITION IS TRUEEEE (2)")
                self.current_scene = 1
                Introrunning = False

            #See if user wants to quit
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    Introrunning = False
                    self.GAME = False
                    break

            #Update display
            pygame.display.update()


    def Game_lost(self):
        #Create background image
        game_lost_bg = pygame.transform.scale(pygame.image.load("Images/Miscellaneous/Game Lost BG.png"), (windowW,windowH))
        game_lost_bg_rect = game_lost_bg.get_rect()
        game_lost_bg_rect.topleft = (0, 0)

        #Create restart button
        RestartImg1 = pygame.image.load("Images/Buttons/RestartBtn.png").convert_alpha()
        RestartImg1 = Buttons.Buttons(525, 100, RestartImg1, 0.4, display_surface)

        #Create text
        GameOverFont = pygame.font.Font("Fonts/EvilEmpire.ttf", 150)
        GameOverText = GameOverFont.render("GAME OVER...", True, (0,0,0))
        GameOverText_rect = GameOverText.get_rect()
        GameOverText_rect.center = (windowW//2, windowH//2)

        StorylineLost = self.WhatTheFudgesticks.render("You failed to defeat Typhon and became his lunch...",True,(255,255,255))
        StorylineLost_rect = StorylineLost.get_rect()
        StorylineLost_rect.center = (windowW//2, 475)

        EndSceneRunning = True
        while EndSceneRunning:

            #Blit background image to screen
            display_surface.blit(game_lost_bg, game_lost_bg_rect)

            #Blit text to screen
            display_surface.blit(GameOverText, GameOverText_rect)
            display_surface.blit(StorylineLost, StorylineLost_rect)

            #Checks if restart button has been pressed
            if RestartImg1.update(display_surface):
                print("RESTARTING")
                self.current_scene = 0
                print("CURRENT SCENE>!>!> "+str(self.current_scene))
                EndSceneRunning = False

            #Checks if user wants to quit
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    EndSceneRunning = False
                    self.GAME = False
                    break

            
            #Update display
            pygame.display.update()
            

    def Desert_Escape(self):
        '''creates main scene; game scene'''

        #Create Sprite groups
        all_sprites = pygame.sprite.Group()

        player_sprite_group = pygame.sprite.Group()
        Playerprojectile_sprite_group = pygame.sprite.Group()

        mother_sprite_group = pygame.sprite.Group()
        minion_sprite_group = pygame.sprite.Group()
        Motherprojectile_sprite_group = pygame.sprite.Group()

        #Set values
        difficultyLevel = self.level

        #Reset sound and init/play background sound
        pygame.mixer.music.stop()
        pygame.mixer.music.load("Audio/Background_music.wav")
        pygame.mixer.music.play(-1,0.0)

        #Create Game Characters
        player = PlayerClass.Player(100,windowH//2,Playerprojectile_sprite_group,windowW,windowH,all_sprites)
        player_sprite_group.add(player)
        MotherMonster1 = MotherMonster.motherMonster(all_sprites,mother_sprite_group,Motherprojectile_sprite_group, windowH, player_sprite_group,difficultyLevel)
        mother_sprite_group.add(MotherMonster1)

        #Create HUD and initialize Game
        game = Game.Game(player, display_surface, player_sprite_group, all_sprites,mother_sprite_group,minion_sprite_group, Playerprojectile_sprite_group,Motherprojectile_sprite_group,fps,clock,windowH,windowW, MotherMonster1,self.current_scene,difficultyLevel)

        #Creates background
        background_image = pygame.image.load("Images/Miscellaneous/roughBackground.png")
        background_image = pygame.transform.scale(background_image, (windowW, windowH))
        background_rect = background_image.get_rect()
        background_rect.topleft = (0, 0)

        #Main game loop
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    self.GAME = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        player.fire()
            
            #Check if the player won, then go to game won scene
            if game.Win == "True":
                print("CURRENT SCENE IS NOW 2")
                pygame.mixer.music.stop()
                self.current_scene = 2
                break
            
            #Check if the player lost, then go to game lost scene
            elif game.Win == "False":
                print("CURRENT SCENE IS NOW 3")
                pygame.mixer.music.stop()
                self.current_scene = 3
                break

            #Fill in display surface --CHANGE LATER--
            display_surface.blit(background_image, background_rect)

            #Update and draw game
            game.draw()
            game.update()

            #Update and draw sprite groups
            player_sprite_group.update()
            player_sprite_group.draw(display_surface)

            mother_sprite_group.update()
            mother_sprite_group.draw(display_surface)

            Motherprojectile_sprite_group.update()
            Motherprojectile_sprite_group.draw(display_surface)

            minion_sprite_group.update()
            minion_sprite_group.draw(display_surface)

            Playerprojectile_sprite_group.update()
            Playerprojectile_sprite_group.draw(display_surface)

            #Update all enemy sprite group
            all_sprites.add(mother_sprite_group)
            all_sprites.add(minion_sprite_group)

            #Update display and tick clock
            pygame.display.update()
            clock.tick(fps)

    def Game_won(self):
        """Creates game over scene"""
        #Reset and init/start new music
        pygame.mixer.music.stop()
        pygame.mixer.music.load("Audio/Game_won_sound.wav")
        pygame.mixer.music.play(-1,0.0)
        
        #Creates background image
        background_img1 = pygame.image.load("Images/Miscellaneous/Game Won BG.png")
        background_img1 = pygame.transform.scale(background_img1, (windowW, windowH))
        background_img1_rect = background_img1.get_rect()

        #Set buttons
        RestartBTN = pygame.image.load("Images/Buttons/RestartBtn.png").convert_alpha()
        RestartBTN = Buttons.Buttons(550, 425, RestartBTN, 0.35, display_surface)

        StorylineWon = self.WhatTheFudgesticks.render("Congratulations! You defeated Typhon and can safely escape from the cursed island!",True,(255,255,255))
        StorylineWon_rect = StorylineWon.get_rect()
        StorylineWon_rect.topleft = (200, 550)

        GameWonRunning = True
        while GameWonRunning:
            #Create background image
            display_surface.blit(background_img1, background_img1_rect)

            #Make rectangle background behind storyline to make storyline more visible
            transparent_BG = pygame.transform.scale(pygame.image.load("Images/Miscellaneous/transparent BG.png"), (850, 70))
            transparent.blit_alpha(display_surface, transparent_BG, (175, 530), 170)

            #Blit game won storyline onto screen
            display_surface.blit(StorylineWon, StorylineWon_rect)

            #Checks if restart button has been pressed
            if RestartBTN.update(display_surface):
                print("RestartBTN pressed")
                GameWonRunning = False
                self.current_scene = 0

            #Check if user wants to quit
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    GameWonRunning = False
                    self.GAME = False
                    break

            #Update pygame
            pygame.display.update()
            

if __name__ == "__main__":
    Scenes().update()

    #End the Game --REMOVE LATER--
    pygame.quit()