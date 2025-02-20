import pygame

pygame.init()

class Buttons():
    def __init__(self, x, y, image, scale, display_surface):
        width = image.get_width()
        height = image.get_height()
        self.image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.clicked = False
        self.display_surface = display_surface

    def update(self, surface):
        action = False
        #Get mouse position
        pos = pygame.mouse.get_pos()

        #Check mouse clicked conditions
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] and not self.clicked:
                print("INSIDEEEEE")
                self.clicked = True
                action = True
            if not pygame.mouse.get_pressed()[0]:
                self.clicked = False

        #draw button on screen
        surface.blit(self.image, (self.rect.x, self.rect.y))

        return action



