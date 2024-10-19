import pygame
import sys


class Laser(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((10, 15))
        self.image.fill((255, 255, 0))
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        self.speed = -1

    def update(self):
        self.rect.y += self.speed
        if self.rect.bottom < 0:
            self.kill()


class Player(pygame.sprite.Sprite):
    def __init__(self, all_sprites, lasers):
        super().__init__()
        self.image = pygame.image.load("assets/images/spaceship2.png")
        self.rect = self.image.get_rect()
        self.rect.center = (
            WIDTH // 2,
            HEIGHT - 50,
        )
        self.shoot_delay = 250
        self.last_shot = pygame.time.get_ticks()
        self.all_sprites = all_sprites
        self.lasers = lasers

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rect.x -= 1
        if keys[pygame.K_RIGHT]:
            self.rect.x += 1
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH

        if keys[pygame.K_SPACE]:
            self.shoot()
            pygame.mixer.music.load("assets/sounds/laser-gun.mp3")
            pygame.mixer.music.play(0)

    def shoot(self):
        now = pygame.time.get_ticks()
        if now - self.last_shot > self.shoot_delay:
            self.last_shot = now
            laser = Laser(self.rect.centerx, self.rect.top)
            self.all_sprites.add(laser)
            self.lasers.add(laser)


def initialize_game():
    pygame.init()
    pygame.mixer.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Game Start Menu")
    return screen


def load_resources():
    global font, menu_background, font_path, game_background
    font_path = "assets/fonts/upheavtt.ttf"
    font = pygame.font.Font(font_path, 50)

    menu_background_image = pygame.image.load("assets/images/menu-background.png")
    menu_background = pygame.transform.scale(menu_background_image, (WIDTH, HEIGHT))
    game_background_image = pygame.image.load("assets/images/game-background.png")
    game_background = pygame.transform.scale(game_background_image, (WIDTH, HEIGHT))
    pygame.mixer.music.load("assets/sounds/menu-music.mp3")
    pygame.mixer.music.play(-1)


def draw_menu():
    global font_path
    for x in range(0, WIDTH, menu_background.get_width()):
        for y in range(0, HEIGHT, menu_background.get_height()):
            screen.blit(menu_background, (x, y))

    title_font = pygame.font.Font(font_path, 80)
    title_text = title_font.render(title, True, YELLOW)
    title_rect = title_text.get_rect(center=(WIDTH // 2, HEIGHT // 4))
    screen.blit(title_text, title_rect)

    for i, option in enumerate(menu_options):
        option_text = font.render(option, True, RED if i == selected_option else WHITE)
        option_rect = option_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + i * 100))
        screen.blit(option_text, option_rect)

    pygame.display.flip()


def draw_game():
    for x in range(0, WIDTH, game_background.get_width()):
        for y in range(0, HEIGHT, game_background.get_height()):
            screen.blit(game_background, (x, y))


def handle_menu_input(event):
    global selected_option, game_state
    if event.key == pygame.K_UP:
        selected_option = (selected_option - 1) % len(menu_options)
    elif event.key == pygame.K_DOWN:
        selected_option = (selected_option + 1) % len(menu_options)
    elif event.key == pygame.K_RETURN:
        if selected_option == 0:
            print("Starting the game...")
            pygame.mixer.music.stop()
            game_state = GAME
        else:
            pygame.mixer.music.stop()
            pygame.quit()
            sys.exit()


def handle_game_input(event):
    global game_state
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_ESCAPE:
            game_state = MENU
            pygame.mixer.music.play(-1)


def main_loop():
    global game_state

    all_sprites = pygame.sprite.Group()
    lasers = pygame.sprite.Group()

    player = Player(all_sprites, lasers)
    all_sprites.add(player)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.mixer.music.stop()
                pygame.quit()
                sys.exit()

            if game_state == MENU:
                if event.type == pygame.KEYDOWN:
                    handle_menu_input(event)

            elif game_state == GAME:
                handle_game_input(event)

        all_sprites.update()

        if game_state == MENU:
            draw_menu()
        elif game_state == GAME:
            draw_game()
            all_sprites.draw(screen)
            pygame.display.flip()


if __name__ == "__main__":
    WIDTH, HEIGHT = 800, 600
    screen = initialize_game()
    load_resources()

    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    RED = (255, 0, 0)
    YELLOW = (255, 255, 0)

    menu_options = ["Start Game", "Quit"]
    selected_option = 0
    title = "Astro Assault"

    MENU = "menu"
    GAME = "game"
    game_state = MENU

    main_loop()
