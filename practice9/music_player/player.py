import pygame
import os

class MusicPlayer:
    def __init__(self, music_folder):
        self.music_folder = music_folder
        self.playlist = self.load_music()
        self.index = 0
        self.is_playing = False
        self.is_loaded = False

    def load_music(self):
        files = []
        for file in os.listdir(self.music_folder):
            if file.endswith(".wav") or file.endswith(".mp3"):
                files.append(os.path.join(self.music_folder, file))
        return sorted(files)

    def load_track(self):
        if self.playlist:
            pygame.mixer.music.load(self.playlist[self.index])
            self.is_loaded = True

    def play(self):
        if not self.playlist:
            return

        # если трек ещё не загружен — загружаем
        if not self.is_loaded:
            self.load_track()

        pygame.mixer.music.play()
        self.is_playing = True

    def stop(self):
        pygame.mixer.music.stop()
        self.is_playing = False

    def next_track(self):
        if self.playlist:
            self.index = (self.index + 1) % len(self.playlist)
            self.is_loaded = False
            self.load_track()
            pygame.mixer.music.play()
            self.is_playing = True

    def prev_track(self):
        if self.playlist:
            self.index = (self.index - 1) % len(self.playlist)
            self.is_loaded = False
            self.load_track()
            pygame.mixer.music.play()
            self.is_playing = True

    def current_track_name(self):
        if self.playlist:
            return os.path.basename(self.playlist[self.index])
        return "No music"