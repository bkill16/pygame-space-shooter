import pygame
import sys
import random


class Laser(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((10, 15))
        self.image.fill((255, 255, 0))
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        self.speed = -10

    def update(self):
        self.rect.y += self.speed
        if self.rect.bottom < 0:
            self.kill()


class Asteroid(pygame.sprite.Sprite):
    def __init__(self, speed):
        super().__init__()
        self.image = pygame.image.load("assets/images/asteroid2.png")
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, WIDTH - self.rect.width)
        self.rect.y = 0
        self.speed = speed

    def update(self):
        self.rect.y += self.speed
        if self.rect.top > HEIGHT:
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
        self.shoot_delay = 100
        self.last_shot = pygame.time.get_ticks()
        self.all_sprites = all_sprites
        self.lasers = lasers
        self.speed = 10

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH

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


def handle_game_input(event, player):
    global game_state, laser_sound_playing
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_ESCAPE:
            game_state = MENU
            pygame.mixer.music.load("assets/sounds/menu-music.mp3")
            pygame.mixer.music.play(-1)
            if laser_sound_playing:
                pygame.mixer.Sound.stop(
                    pygame.mixer.Sound("assets/sounds/laser-gun.mp3")
                )
                laser_sound_playing = False
        elif event.key == pygame.K_SPACE:
            player.shoot()
            laser_sound = pygame.mixer.Sound("assets/sounds/laser-gun.mp3")
            laser_sound.play()
            laser_sound_playing = True


def main_loop():
    global game_state, score, asteroid_spawn_delay

    all_sprites = pygame.sprite.Group()
    lasers = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()

    player = Player(all_sprites, lasers)
    all_sprites.add(player)

    clock = pygame.time.Clock()
    score = 0
    asteroid_spawn_delay = 1000

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
                handle_game_input(event, player)

        if pygame.time.get_ticks() % asteroid_spawn_delay < 50:
            speed = random.randint(5, 10)
            asteroid = Asteroid(speed)
            all_sprites.add(asteroid)
            asteroids.add(asteroid)

        all_sprites.update()

        for laser in lasers:
            hits = pygame.sprite.spritecollide(laser, asteroids, True)
            for hit in hits:
                score += 1
                laser.kill()

        if score > 0 and score % 5 == 0:
            asteroid_spawn_delay = max(200, asteroid_spawn_delay - 100)

        if game_state == MENU:
            draw_menu()
        elif game_state == GAME:
            draw_game()
            all_sprites.draw(screen)
            pygame.display.flip()

        clock.tick(60)


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
    laser_sound_playing = False

    main_loop()
