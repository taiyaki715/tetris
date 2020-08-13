import pygame
import threading


class Button{
    def __init__(self, master, posx, posy, x, y, 
                 button_color, onmouse_button_color, text, text_font, func):
        self.master = master
        self.position = (posx, poxy)
        self.size = (x, y)
        self.color = button_color
        self.color_onmouse = onmouse_button_color
        self.text = text
        self.font = text_font
        self.function = func
}

    def make(self):
        pygame.draw.rect(self.master, self.button_color, 
                         (*self.position, *self.size))
        pygame.display.update()

    def show(self):
        self.thread = threading.Thread(target=self.make)
        self.thread.start()