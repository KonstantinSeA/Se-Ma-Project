import time

import pygame
import sys
from classbutton import PhotoButton
from classvidoe import Video
from plays import game

pygame.init()

width, height = 1280, 720

screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Farmes's Valley")

play_button = PhotoButton(width / 2 - (770 / 2), 450, 220, 175, "", "PhotoSounds/play_button_hide.png",
                          "PhotoSounds/play_button_show.png", "PhotoSounds/button_click.mp3")
save_button = PhotoButton(width / 2 - (250 / 2), 450, 220, 175, "", "PhotoSounds/save_button_hide.png",
                          "PhotoSounds/save_button_show.png", "PhotoSounds/button_click.mp3")
exit_button = PhotoButton(width / 2 - (-270 / 2), 450, 220, 175, "", "PhotoSounds/exit_button_hide.png",
                          "PhotoSounds/exit_button_show.png", "PhotoSounds/button_click.mp3")
back_button = PhotoButton(width / 2 - (-800 / 2), 625, 200, 80, "", "PhotoSounds/back_button_hide.png",
                          "PhotoSounds/back_button_show.png", "PhotoSounds/button_click.mp3")
woman_button_hide = PhotoButton(width / 2 - (-20/2), 320, 90, 90, "", "PhotoSounds/player_woman_hide.png",
                                "", "PhotoSounds/button_click.mp3")
man_button_hide = PhotoButton(width / 2 - (200/2), 320, 90, 90, "", "PhotoSounds/player_man_hide.png",
                              "", "PhotoSounds/button_click.mp3")
woman_button_show = PhotoButton(width / 2 - (-20/2), 320, 90, 90, "", "PhotoSounds/player_woman_show.png",
                                "", "PhotoSounds/button_click.mp3")
man_button_show = PhotoButton(width / 2 - (200/2), 320, 90, 90, "", "PhotoSounds/player_man_show.png",
                              "", "PhotoSounds/button_click.mp3")
start_button = PhotoButton(width / 2 - (1200 / 2), 625, 200, 80, "", "PhotoSounds/start_button_hide.png",
                           "PhotoSounds/start_button_show.png", "PhotoSounds/button_click.mp3")
setting_button = PhotoButton(width / 2 - (-1155 / 2), 9, 60, 57, "", "PhotoSounds/settings_button.png", "",
                             "PhotoSounds/button_click.mp3")
plus_button = PhotoButton(width / 2 - (770 / 2), 450, 120, 85, "", "PhotoSounds/plus_button.png",
                          "", "PhotoSounds/button_click.mp3")
minus_button = PhotoButton(width / 2 - (-270 / 2), 450, 120, 85, "", "PhotoSounds/minus_button.png",
                          "", "PhotoSounds/button_click.mp3")
man_photo = pygame.image.load('PhotoSounds/man_photo.png')
woman_photo = pygame.image.load('PhotoSounds/woman_photo.png')
cursor = pygame.image.load("PhotoSounds/cursor.png")
fon_pers = pygame.image.load("PhotoSounds/fon_pers.png")
pygame.mouse.set_visible(False)

vid = Video("PhotoSounds/videomenu.mp4")
vid.set_size((1280, 720))
intro = Video("PhotoSounds/intro.mp4")
intro.set_size((1280, 720))
pygame.mixer.music.load("PhotoSounds/Farmers_Valley.mp3")
pygame.mixer.music.play(-1)
video_time = pygame.USEREVENT + 1
pygame.time.set_timer(video_time, 30000)
time_update = pygame.USEREVENT + 1
pygame.time.set_timer(time_update, 4500)
font = pygame.font.Font("PhotoSounds/VCROSDMonoRUSbyD.ttf", 32)
sound_button = pygame.mixer.Sound("PhotoSounds/Появление_кнопки.mp3")
sound_click = pygame.mixer.Sound("PhotoSounds/Печатание.mp3")
clock = pygame.time.Clock()
input_box = pygame.Rect(515, 495, 250, 45)
active = False
text = ''
num = 0
num2 = 0
num3 = 0
max_fps = 60

intro_check = True
personash_check = True


def menu():
    global intro_check
    running = True
    intro_v = True
    if intro_check:
        while intro_v:
            for event in pygame.event.get():
                if event.type == time_update:
                    intro_v = False
                    intro_check = False
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
                fade()
                running = False
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
            if event.type == pygame.USEREVENT and event.button == setting_button:
                fade()
                running = False
                vid.toggle_pause()
                settings()
            if event.type == pygame.USEREVENT and event.button == play_button:
                fade()
                running = False
                vid.toggle_pause()
                play_start()
            if event.type == pygame.USEREVENT and event.button == save_button:
                fade()
                running = False
                vid.toggle_pause()
                save_start()
            if vid.get_pts() >= 57:
                vid.restart()
            for own_button in [play_button, save_button, exit_button, setting_button]:
                own_button.events(event)
        vid.draw_video(screen, (0, 0))
        setting_button.check_mouse(pygame.mouse.get_pos())
        setting_button.draw_button(screen)
        play_button.check_mouse(pygame.mouse.get_pos())
        play_button.draw_button(screen)
        save_button.check_mouse(pygame.mouse.get_pos())
        save_button.draw_button(screen)
        exit_button.check_mouse(pygame.mouse.get_pos())
        exit_button.draw_button(screen)
        x, y = pygame.mouse.get_pos()
        screen.blit(cursor, (x, y))
        clock.tick(max_fps)
        pygame.display.update()


def play_start():
    global personash_check, active, text, font, num, num2, num3
    running = True
    player = Video("PhotoSounds/playerpick.mp4")
    player.set_size((1280, 720))
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()
            if player.get_pts() >= 55:
                player.restart()
            if event.type == pygame.MOUSEBUTTONDOWN:
                woman_button_hide.check_mouse(pygame.mouse.get_pos())
                if woman_button_hide.is_hovered:
                    personash_check = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                man_button_hide.check_mouse(pygame.mouse.get_pos())
                if man_button_hide.is_hovered:
                    personash_check = True
            if event.type == pygame.USEREVENT and event.button == back_button:
                fade()
                vid.toggle_pause()
                player.close()
                text = ''
                personash_check = False
                menu()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    fade()
                    vid.toggle_pause()
                    player.close()
                    text = ''
                    personash_check = False
                    menu()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if input_box.collidepoint(event.pos):
                    active = not active
                else:
                    active = False
            if event.type == pygame.USEREVENT and event.button == start_button:
                game.init()
                game.run()
            if event.type == pygame.KEYDOWN:
                if active:
                    num2 = 0
                    num3 = 0
                    if event.key == pygame.K_RETURN:
                        print(text)
                        text = ''
                    elif event.key == pygame.K_BACKSPACE:
                        text = text[:-1]
                        if num2 == 0:
                            sound_click.play()
                            num2 = 1
                    elif len(text) <= 9:
                        if num3 == 0:
                            sound_click.play()
                            num3 = 1
                        text += event.unicode
            for own_button in [back_button, woman_button_hide, woman_button_show, man_button_hide,
                               man_button_show, start_button]:
                own_button.events(event)
        player.draw_video(screen, (0, 0))
        back_button.check_mouse(pygame.mouse.get_pos())
        back_button.draw_button(screen)
        txt_surface = font.render(text, True, "#ce5252")
        screen.blit(txt_surface, (input_box.x + 5, input_box.y + 5))
        pygame.draw.rect(screen, "#f9ba66", input_box, 2)
        if personash_check:
            woman_button_hide.check_mouse(pygame.mouse.get_pos())
            woman_button_hide.draw_button(screen)
            man_button_show.check_mouse(pygame.mouse.get_pos())
            man_button_show.draw_button(screen)
            screen.blit(woman_photo, (width / 2 - (250 / 2), 27))
        else:
            woman_button_show.check_mouse(pygame.mouse.get_pos())
            woman_button_show.draw_button(screen)
            man_button_hide.check_mouse(pygame.mouse.get_pos())
            man_button_hide.draw_button(screen)
            screen.blit(man_photo, (width / 2 - (250 / 2), 27))
        if len(text) > 0:
            if num == 0:
                sound_button.play()
                num = 1
            start_button.check_mouse(pygame.mouse.get_pos())
            start_button.draw_button(screen)
        else:
            num = 0
        x, y = pygame.mouse.get_pos()
        screen.blit(cursor, (x, y))
        clock.tick(max_fps)
        pygame.display.update()


def save_start():
    running = True
    razrabotka = Video("PhotoSounds/dontwork.mp4")
    razrabotka.set_size((1280, 720))
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()
            if razrabotka.get_pts() >= 55:
                razrabotka.restart()
            if event.type == pygame.USEREVENT and event.button == back_button:
                fade()
                vid.toggle_pause()
                razrabotka.close()
                menu()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    fade()
                    vid.toggle_pause()
                    razrabotka.close()
                    menu()
            for own_button in [back_button]:
                own_button.events(event)
        razrabotka.draw_video(screen, (0, 0))
        back_button.check_mouse(pygame.mouse.get_pos())
        back_button.draw_button(screen)
        x, y = pygame.mouse.get_pos()
        screen.blit(cursor, (x, y))
        clock.tick(max_fps)
        pygame.display.update()


def settings():
    running = True
    settings_fon = Video("PhotoSounds/settingsfon.mp4")
    settings_fon.set_size((1280, 720))
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()
            if settings_fon.get_pts() >= 55:
                settings_fon.restart()
            if event.type == pygame.USEREVENT and event.button == back_button:
                fade()
                vid.toggle_pause()
                settings_fon.close()
                running = False
                menu()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    fade()
                    running = False
            for own_button in [back_button, plus_button, minus_button]:
                own_button.events(event)
        settings_fon.draw_video(screen, (0, 0))
        back_button.check_mouse(pygame.mouse.get_pos())
        back_button.draw_button(screen)
        minus_button.check_mouse(pygame.mouse.get_pos())
        minus_button.draw_button(screen)
        plus_button.check_mouse(pygame.mouse.get_pos())
        plus_button.draw_button(screen)
        x, y = pygame.mouse.get_pos()
        screen.blit(cursor, (x, y))
        clock.tick(max_fps)
        pygame.display.update()


def fade():
    running = True
    fade_alpha = 0

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        fade_surface = pygame.Surface((width, height))
        fade_surface.fill((0, 0, 0))
        fade_surface.set_alpha(fade_alpha)
        screen.blit(fade_surface, (0, 0))

        fade_alpha += 5
        if fade_alpha >= 105:
            fade_alpha = 255
            running = False

        pygame.display.flip()
        clock.tick(max_fps)


if __name__ == "__main__":
    menu()
