import io
import math
import pygame
import random
import struct
import wave

from .hole import Hole

# Game Engine

DARK_BROWN = (60, 40, 20)
MOLE_BROWN = (140, 95, 55)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BUTTON_GREEN = (70, 110, 55)
BUTTON_HOVER_GREEN = (90, 135, 65)

DIFFICULTIES = {
    "Easy": (60, 0.01),
    "Medium": (45, 0.02),
    "Hard": (30, 0.04),
}

class GameEngine:
    def __init__(self, width, height, rows=3, cols=3):
        self.width = width
        self.height = height

        self.holes = []
        spacing_x = width // (cols + 1)
        spacing_y = (height - 80) // (rows + 1)
        for r in range(rows):
            for c in range(cols):
                cx = spacing_x * (c + 1)
                cy = 80 + spacing_y * (r + 1)
                self.holes.append(Hole(cx, cy))

        self.spawn_chance = 0.02   # per-hole, per-frame chance to pop up
        self.mole_up_frames = 45   # how long a mole stays up if not whacked
        self.difficulty = "Medium"

        self.round_seconds = 30
        self.time_left_frames = self.round_seconds * 60

        self.score = 0
        self.misses = 0
        self.font = pygame.font.SysFont("Arial", 28)
        self.game_over_font = pygame.font.SysFont("Arial", 42, bold=True)
        self.button_font = pygame.font.SysFont("Arial", 24, bold=True)
        if pygame.mixer.get_init() is None:
            pygame.mixer.init()
        self.whack_sound = self._make_tone(880, 0.08, 0.35)
        self.miss_sound = self._make_tone(220, 0.12, 0.3)
        self.round_end_sound = self._make_tone(440, 0.35, 0.4)
        self.game_over = False
        self.selecting_difficulty = False
        self.quit_requested = False

    @staticmethod
    def _make_tone(frequency, duration, volume):
        sample_rate = 22050
        sample_count = int(sample_rate * duration)
        pcm = bytearray()
        for index in range(sample_count):
            fade_in = min(1.0, index / (sample_rate * 0.01))
            fade_out = min(1.0, (sample_count - index) / (sample_rate * 0.03))
            envelope = min(fade_in, fade_out)
            sample = int(
                32767
                * volume
                * envelope
                * math.sin(2 * math.pi * frequency * index / sample_rate)
            )
            pcm.extend(struct.pack("<h", sample))

        audio = io.BytesIO()
        with wave.open(audio, "wb") as wav_file:
            wav_file.setnchannels(1)
            wav_file.setsampwidth(2)
            wav_file.setframerate(sample_rate)
            wav_file.writeframes(pcm)
        audio.seek(0)
        return pygame.mixer.Sound(file=audio)

    def handle_event(self, event):
        if event.type == pygame.QUIT:
            self.quit_requested = True
            return

        if event.type != pygame.MOUSEBUTTONDOWN:
            return

        if self.selecting_difficulty:
            self._handle_difficulty_click(event.pos)
        elif self.game_over:
            self._handle_game_over_click(event.pos)
        else:
            self._handle_click(event.pos)

    def _handle_game_over_click(self, pos):
        if self._play_again_button().collidepoint(pos):
            self.selecting_difficulty = True
        elif self._quit_button().collidepoint(pos):
            self.quit_requested = True

    def _handle_difficulty_click(self, pos):
        for difficulty, button in self._difficulty_buttons():
            if button.collidepoint(pos):
                self._start_round(difficulty)
                return

        if self._quit_button().collidepoint(pos):
            self.quit_requested = True

    def _start_round(self, difficulty):
        self.difficulty = difficulty
        self.mole_up_frames, self.spawn_chance = DIFFICULTIES[difficulty]
        self.time_left_frames = self.round_seconds * 60
        self.score = 0
        self.misses = 0
        for hole in self.holes:
            hole.active = False
            hole.timer = 0
        self.game_over = False
        self.selecting_difficulty = False

    def _play_again_button(self):
        return pygame.Rect(self.width // 2 - 120, self.height // 2 + 65, 240, 52)

    def _quit_button(self):
        return pygame.Rect(self.width // 2 - 120, self.height // 2 + 130, 240, 52)

    def _difficulty_buttons(self):
        button_width = 130
        gap = 12
        total_width = len(DIFFICULTIES) * button_width + (len(DIFFICULTIES) - 1) * gap
        left = (self.width - total_width) // 2
        top = self.height // 2 - 10
        return [
            (
                difficulty,
                pygame.Rect(left + index * (button_width + gap), top, button_width, 52),
            )
            for index, difficulty in enumerate(DIFFICULTIES)
        ]

    def _draw_button(self, screen, label, rect):
        color = BUTTON_HOVER_GREEN if rect.collidepoint(pygame.mouse.get_pos()) else BUTTON_GREEN
        pygame.draw.rect(screen, color, rect, border_radius=8)
        text = self.button_font.render(label, True, WHITE)
        screen.blit(text, text.get_rect(center=rect.center))

    def _handle_click(self, pos):
        hit_something = False

        for hole in self.holes:
            if hole.contains_mole(pos):
                hole.whack()
                self.score += 1
                hit_something = True
                break

        if hit_something:
            self.whack_sound.play()
        else:
            self.misses += 1
            self.miss_sound.play()

    def handle_input(self):
        # Reserved for continuously-held-key input; this game is
        # entirely mouse-driven, so there's nothing to poll here.
        pass

    def update(self):
        if self.game_over:
            return

        self.time_left_frames -= 1
        if self.time_left_frames <= 0:
            self.game_over = True
            self.round_end_sound.play()
            return

        for hole in self.holes:
            hole.update()
            if not hole.active and random.random() < self.spawn_chance:
                hole.pop_up(self.mole_up_frames)

    def render(self, screen):
        if self.selecting_difficulty:
            title = self.game_over_font.render("Choose Difficulty", True, BLACK)
            screen.blit(
                title,
                title.get_rect(center=(self.width // 2, self.height // 2 - 85)),
            )
            for difficulty, button in self._difficulty_buttons():
                self._draw_button(screen, difficulty, button)
            self._draw_button(screen, "Quit", self._quit_button())
            return

        if self.game_over:
            title = self.game_over_font.render("Game Over", True, BLACK)
            final_score = self.font.render(f"Final score: {self.score}", True, BLACK)
            screen.blit(
                title,
                title.get_rect(center=(self.width // 2, self.height // 2 - 100)),
            )
            screen.blit(
                final_score,
                final_score.get_rect(center=(self.width // 2, self.height // 2 - 45)),
            )
            self._draw_button(screen, "Play Again", self._play_again_button())
            self._draw_button(screen, "Quit", self._quit_button())
            return

        for hole in self.holes:
            pygame.draw.circle(screen, DARK_BROWN, (hole.center_x, hole.center_y), 40)
            if hole.active:
                pygame.draw.circle(
                    screen,
                    MOLE_BROWN,
                    (hole.center_x, hole.center_y),
                    hole.MOLE_RADIUS,
                )

        score_text = self.font.render(f"Score: {self.score}", True, BLACK)
        screen.blit(score_text, (10, 10))

        seconds_left = max(0, self.time_left_frames // 60)
        timer_text = self.font.render(f"Time: {seconds_left}s", True, BLACK)
        screen.blit(timer_text, (self.width - 140, 10))
