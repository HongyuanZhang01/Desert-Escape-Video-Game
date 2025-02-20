import pygame

pygame.init()

def blit_alpha(surface, image, location, opacity):
        #Assign the (x,y) of image
        x = location[0]
        y = location[1]
        #Generate second slightly altered img and overlays
        #it over original to create transparent effect
        temp = pygame.Surface((1000, 600)).convert()
        temp.blit(surface, (-x, -y))
        temp.blit(image, (0, 0))
        temp.set_alpha(opacity)        
        #Makes new overlaid img appear on screen
        surface.blit(temp, location)