import pygame
import sys
from classbutton import PhotoButton
from classvidoe import Video

pygame.init()

width, height = 1280, 720

screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Farmes's Valley")

play_button = PhotoButton(width / 2 - (770/2), 450, 220, 175, "", "play_button_hide.png",
                          "play_button_show.png", "button_click.mp3")
save_button = PhotoButton(width / 2 - (250/2), 450, 220, 175, "", "save_button_hide.png",
                          "save_button_show.png", "button_click.mp3")
exit_button = PhotoButton(width / 2 - (-270/2), 450, 220, 175, "", "exit_button_hide.png",
                          "exit_button_show.png", "button_click.mp3")

vid = Video("videomenu.mp4")
vid.set_size((1280, 720))
intro = Video("intro.mp4")
intro.set_size((1280, 720))
pygame.mixer.music.load("Farmers Valley.mp3")
pygame.mixer.music.play(-1)
time_update = pygame.USEREVENT + 1
pygame.time.set_timer(time_update, 4500)


def menu():
    running = True
    intro_v = True
    while intro_v:
        for event in pygame.event.get():
            if event.type == time_update:
                intro_v = False
                intro.close()
        intro.draw_video(screen, (0, 0))
        pygame.display.update()
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()
            if event.type == pygame.USEREVENT and event.button == exit_button:
                running = False
                pygame.quit()
                sys.exit()
            if event.type == pygame.USEREVENT and event.button == play_button:
                play_start()
            if event.type == time_update:
                vid.restart()
            for own_button in [play_button, save_button, exit_button]:
                own_button.events(event)
        vid.draw_video(screen, (0, 0))
        play_button.check_mouse(pygame.mouse.get_pos())
        play_button.draw_button(screen)
        save_button.check_mouse(pygame.mouse.get_pos())
        save_button.draw_button(screen)
        exit_button.check_mouse(pygame.mouse.get_pos())
        exit_button.draw_button(screen)
        pygame.display.update()


def play_start():
    pass


menu()