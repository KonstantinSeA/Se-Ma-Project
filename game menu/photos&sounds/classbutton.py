import pygame


class PhotoButton:
    def __init__(self, x: object, y: object, witdh: object, height: object, text: object, image_path: object, hower_image_path: object = None,
                 sound_p: object = None) -> object:
        self.x = x
        self.y = y
        self.wigth = witdh
        self.height = height
        self.text = text
        self.image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(self.image, (witdh, height))
        self.hover_image = self.image
        if hower_image_path:
            self.hover_image = pygame.image.load(hower_image_path)
            self.hover_image = pygame.transform.scale(self.hover_image, (witdh, height))
        self.rect = self.image.get_rect(topleft=(x, y))
        self.sound = None
        if sound_p:
            self.sound = pygame.mixer.Sound(sound_p)
        self.is_hovered = False

    def draw_button(self, screen):
        current_image = self.hover_image if self.is_hovered else self.image
        screen.blit(current_image, self.rect.topleft)

    def check_mouse(self, mouse_pos):
        self.is_hovered = self.rect.collidepoint(mouse_pos)

    def events(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self.is_hovered:
            if self.sound:
                self.sound.play()
            pygame.event.post(pygame.event.Event(pygame.USEREVENT, button=self))