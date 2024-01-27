import pygame
import sys
from classbutton import PhotoButton
from classvidoe import Video

pygame.init()

width, height = 1280, 720

screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Farmes's Valley")

play_button = PhotoButton(width / 2 - (770 / 2), 450, 220, 175, "", "play_button_hide.png",
                          "play_button_show.png", "button_click.mp3")
save_button = PhotoButton(width / 2 - (250 / 2), 450, 220, 175, "", "save_button_hide.png",
                          "save_button_show.png", "button_click.mp3")
exit_button = PhotoButton(width / 2 - (-270 / 2), 450, 220, 175, "", "exit_button_hide.png",
                          "exit_button_show.png", "button_click.mp3")
back_button = PhotoButton(width / 2 - (-800 / 2), 625, 200, 80, "", "back_button_hide.png",
                          "back_button_show.png", "button_click.mp3")
woman_button_hide = PhotoButton(width / 2 - (-20/2), 320, 90, 90, "", "player_woman_hide.png",
                                "", "button_click.mp3")
man_button_hide = PhotoButton(width / 2 - (200/2), 320, 90, 90, "", "player_man_hide.png",
                              "", "button_click.mp3")
woman_button_show = PhotoButton(width / 2 - (-20/2), 320, 90, 90, "", "player_woman_show.png",
                                "", "button_click.mp3")
man_button_show = PhotoButton(width / 2 - (200/2), 320, 90, 90, "", "player_man_show.png",
                              "", "button_click.mp3")


vid = Video("videomenu.mp4")
vid.set_size((1280, 720))
intro = Video("intro.mp4")
intro.set_size((1280, 720))
pygame.mixer.music.load("Farmers_Valley.mp3")
pygame.mixer.music.play(-1)
video_time = pygame.USEREVENT + 1
pygame.time.set_timer(video_time, 30000)
time_update = pygame.USEREVENT + 1
pygame.time.set_timer(time_update, 4500)
clock = pygame.time.Clock()
input_box = pygame.Rect(515, 495, 250, 45)
active = False
text = ''
font = pygame.font.Font("VCROSDMonoRUSbyD.ttf", 32)

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
                running = False
                pygame.quit()
                sys.exit()
            if event.type == pygame.USEREVENT and event.button == play_button:
                running = False
                vid.toggle_pause()
                play_start()
            if vid.get_pts() >= 57:
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
    global personash_check, active, color, text, font, sleep_woman, sleep_man
    running = True
    player = Video("playerpick.mp4")
    player.set_size((1280, 720))
    while running:
        ui_refresh_rate = clock.tick(60) / 1000
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()
            if player.get_pts() >= 55:
                player.restart()
            if event.type == pygame.USEREVENT and event.button == woman_button_hide:
                personash_check = False
                print(3)
            if event.type == pygame.USEREVENT and event.button == man_button_hide:
                personash_check = True
                print(4)
            if event.type == pygame.USEREVENT and event.button == back_button:
                vid.toggle_pause()
                player.close()
                menu()
            for own_button in [back_button, woman_button_hide, woman_button_show, man_button_hide,
                               man_button_show]:
                own_button.events(event)
            if event.type == pygame.KEYDOWN:
                if active:
                    if event.key == pygame.K_RETURN:
                        print(text)
                        text = ''
                    elif event.key == pygame.K_BACKSPACE:
                        text = text[:-1]
                    elif len(text) <= 9:
                        text += event.unicode
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
        else:
            woman_button_show.check_mouse(pygame.mouse.get_pos())
            woman_button_show.draw_button(screen)
            man_button_hide.check_mouse(pygame.mouse.get_pos())
            man_button_hide.draw_button(screen)

        pygame.display.update()


menu()
