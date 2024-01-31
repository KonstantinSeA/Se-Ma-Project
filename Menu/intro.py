from classvidoe import Video
import pygame


pygame.init()

width, height = 1280, 720

screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Farmes's Valley")
intro = Video("intro.mp4")
intro.set_size((1280, 720))
time_update = pygame.USEREVENT + 1
pygame.time.set_timer(time_update, 4500)


def intro():
    intro_v = True
    while intro_v:
        for event in pygame.event.get():
            if event.type == time_update:
               intro_v = False
               intro.close()
        intro.draw_video(screen, (0, 0))
        pygame.display.update()


intro()