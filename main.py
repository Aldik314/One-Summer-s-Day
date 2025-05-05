import pygame, sys
from settings import *
from button import Button
from abc import ABC, abstractmethod
from level import Level


class RenderStrategy(ABC):
    @abstractmethod
    def draw(self, game, dt: float):
        """Draw background elements based on game state"""
        pass


class CompositeRenderStrategy(RenderStrategy):
    def __init__(self, strategies):
        self.strategies = strategies

    def draw(self, game, dt):
        for strategy in self.strategies:
            strategy.draw(game, dt)


class ScrollingBGStrategy(RenderStrategy):
    def draw(self, game, dt):
        game.bg_x -= 2 * dt
        if game.bg_x <= -SCREEN_WIDTH:
            game.bg_x = 0
        game.screen.blit(game.bg, (game.bg_x, 0))
        game.screen.blit(game.bg, (game.bg_x + SCREEN_WIDTH, 0))
        game.screen.blit(game.bg1, (0, 0))


class MenuAnimationStrategy(RenderStrategy):
    def __init__(self):
        self.last_update = 0

    def draw(self, game, dt):
        now = pygame.time.get_ticks()
        if now - self.last_update > 200:  # 200ms = 5 FPS
            self.last_update = now
            game.anim_index = (game.anim_index + 1) % len(game.main_anim)
        game.screen.blit(game.main_anim[game.anim_index], (220, 550))


class TitleRenderStrategy(RenderStrategy):
    def draw(self, game, dt):
        game.screen.blit(game.title_image, game.title_rect)


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("One Summer's Day")
        pygame.display.set_icon(pygame.image.load('images/icon.png'))
        self.clock = pygame.time.Clock()

        # Load resources
        self.load_resources()

        # State management
        self.init_state_system()

        # Rendering system
        self.init_render_system()


        self.pause_menu_active = False
        self.pause_bg = pygame.Surface((350, 200), pygame.SRCALPHA)
        self.pause_bg.fill((40, 40, 40, 230))

        self.pause_buttons = {
            'resume': Button(
                SCREEN_WIDTH//2 - 150, SCREEN_HEIGHT//2 - 60,
                pygame.image.load('images/buttons/resume.png'),
                pygame.image.load('images/buttons/resume_light.png'),
                1
            ),
            'save_quit': Button(
                SCREEN_WIDTH//2 - 150, SCREEN_HEIGHT//2 + 70,
                pygame.image.load('images/buttons/save_quit.png'),
                pygame.image.load('images/buttons/save_quit_light.png'),
                1
            )
        }

        self.pre_pause_state = None

    def load_resources(self):
        """Load all game assets"""
        self.bg = pygame.image.load('images/bg_1.png')
        self.bg1 = pygame.image.load('images/nm2.png')
        self.bg_x = 0

        # Load animation frames
        self.main_anim = []
        for i in range(1, 16):
            try:
                frame = pygame.image.load(f'images/bg_sitting/{i}.png')
                self.main_anim.append(frame)
            except:
                print(f"Warning: Missing animation frame {i}")
        self.anim_index = 0

        # Title setup
        title_img = pygame.image.load('images/title1.png')
        self.title_image = pygame.transform.scale(
            title_img,
            (int(title_img.get_width() * 1.7), int(title_img.get_height() * 1.7))
        )
        self.title_rect = self.title_image.get_rect(center=(SCREEN_WIDTH / 2, 230))

        # Buttons
        self.new_button = self.create_button(370, 'new')
        self.load_button = self.create_button(470, 'load')
        self.quit_button = self.create_button(570, 'exit')

    def create_button(self, y, name):
        """Helper to create consistent buttons"""
        return Button(
            SCREEN_WIDTH / 2 - 90, y,
            pygame.image.load(f'images/buttons/{name}.png'),
            pygame.image.load(f'images/buttons/{name}_light.png'),
            0.9
        )

    def init_state_system(self):
        """Initialize game state tracking"""
        self.STATES = {
            'INTRO': 0,
            'TITLE': 1,
            'BUTTONS': 2,
            'PLAYING': 3
        }
        self.state = self.STATES['INTRO']
        self.start_time = pygame.time.get_ticks()
        self.button_timings = {'new': 1700, 'load': 2400, 'quit': 3100}
        self.visible_buttons = set()
        self.level = None

    def init_render_system(self):
        """Initialize rendering strategies"""
        self.render_strategies = {
            'scrolling_bg': ScrollingBGStrategy(),
            'menu_anim': MenuAnimationStrategy(),
            'title': TitleRenderStrategy()
        }

        # Composite strategies for different game states
        self.state_renderers = {
            self.STATES['INTRO']: CompositeRenderStrategy([
                self.render_strategies['scrolling_bg'],
                self.render_strategies['menu_anim']
            ]),
            self.STATES['TITLE']: CompositeRenderStrategy([
                self.render_strategies['scrolling_bg'],
                self.render_strategies['menu_anim'],
                self.render_strategies['title']
            ]),
            self.STATES['BUTTONS']: CompositeRenderStrategy([
                self.render_strategies['scrolling_bg'],
                self.render_strategies['menu_anim'],
                self.render_strategies['title']
            ]),
            self.STATES['PLAYING']: CompositeRenderStrategy([])
        }

    def run(self):
        """Main game loop"""
        while True:
            dt = self.clock.tick(60) / 1000  # Cap at 60 FPS
            self.handle_events()
            self.update_state()
            self.render_frame(dt)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit_game()

            # Handle key presses
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.toggle_pause_menu()

            # Handle pause menu buttons
            if self.pause_menu_active:
                # Pause menu button handling
                if self.pause_buttons['resume'].click_check(event):
                    self.toggle_pause_menu()
                elif self.pause_buttons['save_quit'].click_check(event):
                    self.save_and_quit()
            elif self.state == self.STATES['PLAYING']:
                continue  # Game handles its own input
            else:
                # Main menu button handling
                if 'new' in self.visible_buttons and self.new_button.click_check(event):
                    self.start_game()
                if 'load' in self.visible_buttons and self.load_button.click_check(event):
                    self.load_game()
                if 'quit' in self.visible_buttons and self.quit_button.click_check(event):
                    self.quit_game()

    def toggle_pause_menu(self):
        """Toggle pause menu on/off"""
        if self.state != self.STATES['PLAYING']:
            return  # Only allow pausing during gameplay

        self.pause_menu_active = not self.pause_menu_active
        if self.pause_menu_active:
            self.pre_pause_state = self.state
            pygame.mixer.music.pause()  # Pause game music
        else:
            pygame.mixer.music.unpause()

    def save_and_quit(self):
        """Save game and return to main menu"""
        if self.level:
            self.level.save_game()
        self.pause_menu_active = False
        self.state = self.STATES['INTRO']
        self.start_time = pygame.time.get_ticks()
        self.visible_buttons = set()
        pygame.mixer.music.unpause()

    def update_state(self):
        """Update game state based on timing"""
        elapsed = pygame.time.get_ticks() - self.start_time

        if self.state == self.STATES['INTRO'] and elapsed > 1000:
            self.state = self.STATES['TITLE']
        elif self.state == self.STATES['TITLE'] and elapsed > 1700:
            self.state = self.STATES['BUTTONS']

        if self.state == self.STATES['BUTTONS']:
            if elapsed > self.button_timings['new']:
                self.visible_buttons.add('new')
            if elapsed > self.button_timings['load']:
                self.visible_buttons.add('load')
            if elapsed > self.button_timings['quit']:
                self.visible_buttons.add('quit')

    def render_frame(self, dt):
        """Render complete game frame"""
        self.screen.fill((0, 0, 0))  # Clear screen

        # Draw background elements based on state
        self.state_renderers[self.state].draw(self, dt)

        # Draw main menu buttons if applicable
        if self.state == self.STATES['BUTTONS']:
            self.draw_buttons()

        # Draw game level if playing
        if self.state == self.STATES['PLAYING']:
            self.level.run(dt)

            # Draw pause menu on top if active
            if self.pause_menu_active:
                self.draw_pause_menu()

        pygame.display.update()

    def draw_pause_menu(self):
        """Draw the pause menu overlay"""
        # Darken background
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 150))
        self.screen.blit(overlay, (0, 0))

        # Draw menu box
        #menu_rect = self.pause_bg.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        #self.screen.blit(self.pause_bg, menu_rect)

        # Draw buttons
        self.pause_buttons['resume'].draw(self.screen)
        self.pause_buttons['save_quit'].draw(self.screen)

    def draw_buttons(self):
        """Draw visible menu buttons"""
        if 'new' in self.visible_buttons:
            self.new_button.draw(self.screen)
        if 'load' in self.visible_buttons:
            self.load_button.draw(self.screen)
        if 'quit' in self.visible_buttons:
            self.quit_button.draw(self.screen)

    def start_game(self):
        """Transition to gameplay state"""
        self.state = self.STATES['PLAYING']
        self.level = Level()

    def load_game(self):
        """Load saved game"""
        self.state = self.STATES['PLAYING']
        self.level = Level()
        self.level.load_game()

    def quit_game(self):
        """Cleanup and exit"""
        if self.level:
            self.level.save_game()
        pygame.quit()
        sys.exit()


if __name__ == '__main__':
    game = Game()
    game.run()