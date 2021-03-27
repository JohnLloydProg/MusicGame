import pygame
from beat import Beat
from button import Button, MusicButton
import threading
import os
import math
import time


class Game:
    def __init__(self, title):
        pygame.init()
        self.win = pygame.display.set_mode((1080, 720))
        pygame.display.set_caption(title)
        self.clock = pygame.time.Clock()
        self.paused = False
        self.main()

    def play_music(self, name):
        beats = []
        combo_counter = 1
        score = 0
        beat_timer = 0
        with open(os.curdir + "/songs/" + name + "/beat_list.txt") as soundtrack_delays:
            d = soundtrack_delays.readline()
            delays = list(d.split(", "))
        try:
            background_image = pygame.image.load(os.curdir + "/songs/" + name + "/background_img.jpg")
        except FileNotFoundError:
            background_image = pygame.image.load(os.curdir + "/images/default_background_img.jpg")
        background_image = pygame.transform.scale(background_image, (1080, 720))
        backboard_image = pygame.image.load(os.curdir + "/images/backboard.jpg")
        player_button = pygame.image.load(os.curdir + "/images/player_button.png")
        screen = pygame.Surface((1080, 720), pygame.SRCALPHA)
        screen.fill((0, 0, 0, 125))
        font = pygame.font.SysFont("None", 50)
        another_song_button = Button(390, 275, pygame.image.load(os.curdir+"/images/another_song_button.png"))
        restart_button = Button(390, 370, pygame.image.load(os.curdir+"/images/restart_button.png"))
        music_player = threading.Thread(target=music_function, daemon=True, args=(os.curdir+"/songs/"+name,))
        music_player.start()
        run = True
        while run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        if beats:
                            if 260 >= beats[0].x:
                                dis = math.sqrt(math.pow(200 - (beats[0].x + 45), 2) + math.pow(520 - (beats[0].y + 45), 2))
                                if dis <= 10:
                                    score += 100 * combo_counter
                                    combo_counter += 1
                                elif 25 >= dis > 10:
                                    score += 50 * combo_counter
                                    combo_counter += 1
                                elif 50 >= dis > 25:
                                    score += 25
                                    combo_counter = 1
                                beats.remove(beats[0])
                    if event.key == pygame.K_ESCAPE:
                        if self.paused:
                            self.paused = False
                            pygame.mixer.music.unpause()
                        else:
                            self.paused = True
                            pygame.mixer.music.pause()
                if not self.paused:
                    if event.type == pygame.USEREVENT+1:
                        beat_timer += 10
                        if delays[0] != "end" and float(delays[0]) * 1000 == beat_timer:
                            beats.append(Beat(1045, 475))
                            delays.pop(0)
                            beat_timer = 0
                        elif delays[0] == "end" and len(beats) == 0 and not pygame.mixer.music.get_busy():
                            self.show_score(name, score, background_image)
                else:
                    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                        if another_song_button.inside():
                            pygame.mixer.music.stop()
                            self.paused = False
                            self.music_selection()
                        elif restart_button:
                            self.paused = False
                            self.play_music(name)

            if self.paused:
                menu_screen = pygame.Surface((1080, 720), pygame.SRCALPHA)
                menu_screen.fill((0, 0, 0, 100))
                self.win.blit(menu_screen, (0, 0))
                another_song_button.draw(self.win)
                restart_button.draw(self.win)
                pygame.display.update()
                self.clock.tick(30)
            else:
                pygame.time.set_timer(pygame.USEREVENT+1, 10)
                self.win.blit(background_image, (0, 0))
                self.win.blit(screen, (0, 0))
                self.win.blit(backboard_image, (0, 465))
                self.win.blit(player_button, (150, 470))
                for beat in beats:
                    beat.move(5)
                    if beat.x + 90 < 150:
                        combo_counter = 1
                        beats.remove(beat)
                    beat.draw(self.win)
                self.win.blit(font.render(str(score), True, (255, 255, 255)), (1070 - len(str(score)) * 20, 10))
                self.win.blit(font.render(str(combo_counter), True, (255, 255, 255)), (10, 10))
                pygame.display.update()
                self.clock.tick(60)

    def music_selection(self):
        background_img = pygame.image.load(os.curdir + "/images/menu_background_img.jpg")
        background_img = pygame.transform.scale(background_img, (1080, 720))
        screen = pygame.Surface((1080, 720), pygame.SRCALPHA)
        screen.fill((0, 0, 0, 125))
        song_dir = os.curdir+"/songs"
        songs = []
        back_button = Button(5, 5, pygame.image.load(os.curdir+"/images/back_button.png"))
        for i in range(len(os.listdir(song_dir))):
            songs.append(MusicButton(760, 10 + (85*i), pygame.image.load(os.curdir+"/images/music_button.png"), os.listdir(song_dir)[i]))
        run = True
        while run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    for song in songs:
                        if song.inside():
                            self.play_music(song.name)
                    if back_button.inside():
                        self.main()

            self.win.blit(background_img, (0, 0))
            self.win.blit(screen, (0, 0))
            for song in songs:
                song.draw(self.win)
            back_button.draw(self.win)
            pygame.display.update()
            self.clock.tick(60)

    def main(self):
        background_img = pygame.image.load(os.curdir+"/images/menu_background_img.jpg")
        background_img = pygame.transform.scale(background_img, (1080, 720))
        screen = pygame.Surface((1080, 720), pygame.SRCALPHA)
        screen.fill((0, 0, 0, 125))
        play_button = Button(760, 535, pygame.image.load(os.curdir+"/images/play_button.png"))
        exit_button = Button(760, 630, pygame.image.load(os.curdir+"/images/exit_button.png"))
        run = True
        while run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if play_button.inside():
                        self.music_selection()
                        print("Open Menu")
                    elif exit_button.inside():
                        pygame.quit()
                        quit()

            self.win.blit(background_img, (0, 0))
            self.win.blit(screen, (0, 0))
            play_button.draw(self.win)
            exit_button.draw(self.win)
            pygame.display.update()
            self.clock.tick(60)

    def show_score(self, name, score, background_img):
        restart_button = Button(20, 610, pygame.image.load(os.curdir+"/images/restart_button.png"))
        continue_button = Button(760, 610, pygame.image.load(os.curdir+"/images/continue_button.png"))
        display_gui = pygame.image.load(os.curdir+"/images/score_display_img.png")
        screen = pygame.Surface((1080, 720), pygame.SRCALPHA)
        screen.fill((0, 0, 0, 125))
        font = pygame.font.SysFont("None", 75)
        view_score = 0
        run = True
        while run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if restart_button.inside():
                        self.play_music(name)
                    elif continue_button.inside():
                        self.music_selection()

            if view_score != score:
                view_score += score * 0.02

            self.win.blit(background_img, (0, 0))
            self.win.blit(screen, (0, 0))
            self.win.blit(display_gui, (0, 0))
            self.win.blit(font.render(name, True, (255, 255, 255)), (10, 25))
            self.win.blit(font.render(str(int(view_score)), True, (255, 255, 255)), (920 - (len(str(view_score))*14), 200))
            restart_button.draw(self.win)
            continue_button.draw(self.win)
            pygame.display.update()
            self.clock.tick(50)


def music_function(music_path):
    time.sleep(2.55)
    pygame.mixer.music.load(music_path + "/song.mp3")
    pygame.mixer.music.play()


if __name__ == "__main__":
    game = Game("Music Game")
    for i in range(10):
        print("working")
        time.sleep(1)
