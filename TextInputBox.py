import pygame

class TextInputBox(pygame.sprite.Sprite):
    def __init__(self, x, y, w, font, inac):
        super().__init__()
        self.color = (255, 255, 255)
        self.backcolor = None
        self.pos = (x, y)
        self.width = w
        self.font = font
        self.active = False
        self.text = inac
        self.inactive_text = inac
        self.render_text()

    def render_text(self):
        t_surf = self.font.render(self.text, True, self.color, self.backcolor)
        self.image = pygame.Surface((max(self.width, t_surf.get_width() + 10), t_surf.get_height() + 10),
                                    pygame.SRCALPHA)
        if self.backcolor:
            self.image.fill(self.backcolor)
        self.image.blit(t_surf, (5, 5))
        pygame.draw.rect(self.image, self.color, self.image.get_rect().inflate(-2, -2), 2)
        self.rect = self.image.get_rect(topleft=self.pos)

    def update(self, event_list, Result):
        if not self.active and self.text == '':
            self.text = self.inactive_text
        for event in event_list:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if not self.active and self.text == '':
                    self.text = self.inactive_text
                self.active = self.rect.collidepoint(event.pos)
                if self.active and self.text == self.inactive_text:
                    self.text = ''
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE and self.active:
                    self.text = self.text[:-1]
                else:
                    if self.active and event.unicode in '1234567890':
                        self.text += event.unicode

                self.render_text()