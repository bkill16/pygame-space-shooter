import pygame
import sys
import random


# Laser class, handles creation and behavior of player's laser shots
class Laser(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((10, 15))  # Create laser surface
        self.image.fill((255, 255, 0))  # Yellow laser color
        self.rect = self.image.get_rect()  # Get rectangle for positioning
        self.rect.centerx = x  # Set the x position of the laser
        self.rect.bottom = (
            y  # Set the y position of the laser (starting from player's position)
        )
        self.speed = -10  # Speed of the laser (moves upwards)

    def update(self):
        # Update laser position
        self.rect.y += self.speed
        # Remove the laser if it goes off-screen
        if self.rect.bottom < 0:
            self.kill()


# Asteroid class, handles the creation and behavior of falling asteroids
class Asteroid(pygame.sprite.Sprite):
    def __init__(self, speed):
        super().__init__()
        # Load the asteroid image
        self.image = pygame.image.load("assets/images/asteroid2.png")
        self.rect = self.image.get_rect()  # Get rectangle for positioning
        # Randomly position asteroid on the x-axis, starting at the top
        self.rect.x = random.randint(0, WIDTH - self.rect.width)
        self.rect.y = 0  # Start from the top of the screen
        self.speed = speed  # Speed of the falling asteroid

    def update(self):
        # Update asteroid position
        self.rect.y += self.speed
        # Remove the asteroid if it goes off-screen
        if self.rect.top > HEIGHT:
            self.kill()


# Player class, handles player movement and shooting mechanics
class Player(pygame.sprite.Sprite):
    def __init__(self, all_sprites, lasers):
        super().__init__()
        # Load the player spaceship image
        self.image = pygame.image.load("assets/images/spaceship2.png")
        self.rect = self.image.get_rect()  # Get rectangle for positioning
        # Position the player at the bottom center of the screen
        self.rect.center = (WIDTH // 2, HEIGHT - 50)
        self.shoot_delay = 100  # Delay between laser shots in milliseconds
        self.last_shot = pygame.time.get_ticks()  # Keep track of last shot time
        self.all_sprites = all_sprites  # Reference to all game sprites
        self.lasers = lasers  # Reference to the player's lasers
        self.speed = 10  # Speed of the player

    def update(self):
        # Handle player movement
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed  # Move left
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed  # Move right
        # Prevent player from moving off the left side of the screen
        if self.rect.left < 0:
            self.rect.left = 0
        # Prevent player from moving off the right side of the screen
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH

    def shoot(self):
        # Handle shooting mechanics with delay
        now = pygame.time.get_ticks()  # Get current time
        if now - self.last_shot > self.shoot_delay:
            self.last_shot = now  # Update last shot time
            # Create a new laser at the player's current position
            laser = Laser(self.rect.centerx, self.rect.top)
            self.all_sprites.add(laser)  # Add laser to all sprites
            self.lasers.add(laser)  # Add laser to player's lasers


# Initialize the game, set up the screen, and start music
def initialize_game():
    pygame.init()  # Initialize Pygame
    pygame.mixer.init()  # Initialize sound mixer
    screen = pygame.display.set_mode((WIDTH, HEIGHT))  # Set screen size
    pygame.display.set_caption("Game Start Menu")  # Set window title
    return screen


# Load resources such as fonts, images, and sounds
def load_resources():
    global font, menu_background, font_path, game_background
    font_path = "assets/fonts/upheavtt.ttf"  # Path to font
    font = pygame.font.Font(font_path, 50)  # Load font

    # Load and scale menu background image
    menu_background_image = pygame.image.load("assets/images/menu-background.png")
    menu_background = pygame.transform.scale(menu_background_image, (WIDTH, HEIGHT))
    # Load and scale game background image
    game_background_image = pygame.image.load("assets/images/game-background.png")
    game_background = pygame.transform.scale(game_background_image, (WIDTH, HEIGHT))
    # Load and play menu background music
    pygame.mixer.music.load("assets/sounds/menu-music.mp3")
    pygame.mixer.music.play(-1)  # Loop the music


# Draw the menu screen with title and options
def draw_menu():
    global font_path
    # Tile the menu background across the screen
    for x in range(0, WIDTH, menu_background.get_width()):
        for y in range(0, HEIGHT, menu_background.get_height()):
            screen.blit(menu_background, (x, y))

    # Draw the title text
    title_font = pygame.font.Font(font_path, 80)
    title_text = title_font.render(title, True, YELLOW)
    title_rect = title_text.get_rect(center=(WIDTH // 2, HEIGHT // 4))
    screen.blit(title_text, title_rect)

    # Draw each menu option
    for i, option in enumerate(menu_options):
        option_text = font.render(option, True, RED if i == selected_option else WHITE)
        option_rect = option_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + i * 100))
        screen.blit(option_text, option_rect)

    pygame.display.flip()  # Update display


# Draw the game screen
def draw_game():
    # Tile the game background across the screen
    for x in range(0, WIDTH, game_background.get_width()):
        for y in range(0, HEIGHT, game_background.get_height()):
            screen.blit(game_background, (x, y))


# Handle input during the menu screen
def handle_menu_input(event):
    global selected_option, game_state
    if event.key == pygame.K_UP:
        selected_option = (selected_option - 1) % len(menu_options)  # Move selection up
    elif event.key == pygame.K_DOWN:
        selected_option = (selected_option + 1) % len(
            menu_options
        )  # Move selection down
    elif event.key == pygame.K_RETURN:
        # Start game or quit based on selected option
        if selected_option == 0:
            print("Starting the game...")
            pygame.mixer.music.stop()
            game_state = GAME  # Start the game
        else:
            pygame.mixer.music.stop()
            pygame.quit()
            sys.exit()  # Quit the game


# Handle input during the game, including shooting and pausing
def handle_game_input(event, player):
    global game_state, laser_sound_playing
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_ESCAPE:
            game_state = MENU  # Return to menu if ESC is pressed
            pygame.mixer.music.load("assets/sounds/menu-music.mp3")
            pygame.mixer.music.play(-1)
            # Stop laser sound if it's playing
            if laser_sound_playing:
                pygame.mixer.Sound.stop(
                    pygame.mixer.Sound("assets/sounds/laser-gun.mp3")
                )
                laser_sound_playing = False
        elif event.key == pygame.K_SPACE:
            player.shoot()  # Shoot when spacebar is pressed
            laser_sound = pygame.mixer.Sound("assets/sounds/laser-gun.mp3")
            laser_sound.play()  # Play laser sound
            laser_sound_playing = True


# Main game loop, handles menu, game state, and spawning
def main_loop():
    global game_state, score, asteroid_spawn_delay

    # Sprite groups for the player, lasers, and asteroids
    all_sprites = pygame.sprite.Group()
    lasers = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()

    player = Player(all_sprites, lasers)  # Initialize player
    all_sprites.add(player)

    clock = pygame.time.Clock()  # Game clock for controlling frame rate
    score = 0  # Initialize score
    asteroid_spawn_delay = 1000  # Initial delay between asteroid spawns

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.mixer.music.stop()
                pygame.quit()
                sys.exit()  # Quit the game if window is closed

            if game_state == MENU:
                if event.type == pygame.KEYDOWN:
                    handle_menu_input(event)  # Handle menu input

            elif game_state == GAME:
                handle_game_input(event, player)  # Handle game input

        # Spawn new asteroids at a fixed interval
        if pygame.time.get_ticks() % asteroid_spawn_delay < 50:
            speed = random.randint(5, 10)  # Random asteroid speed
            asteroid = Asteroid(speed)
            all_sprites.add(asteroid)
            asteroids.add(asteroid)

        all_sprites.update()  # Update all sprites

        # Check for collisions between lasers and asteroids
        for laser in lasers:
            hits = pygame.sprite.spritecollide(laser, asteroids, True)
            for hit in hits:
                score += 1  # Increase score when an asteroid is hit
                laser.kill()  # Remove the laser after it hits

        # Increase asteroid spawn rate as the score increases
        if score > 0 and score % 5 == 0:
            asteroid_spawn_delay = max(200, asteroid_spawn_delay - 100)

        # Draw the appropriate screen based on game state
        if game_state == MENU:
            draw_menu()  # Draw menu screen
        elif game_state == GAME:
            draw_game()  # Draw game screen
            all_sprites.draw(screen)
            pygame.display.flip()  # Update display

        clock.tick(60)  # Control frame rate


# Entry point of the program
if __name__ == "__main__":
    WIDTH, HEIGHT = 800, 600  # Screen dimensions
    screen = initialize_game()  # Initialize the game screen
    load_resources()  # Load all resources

    # Define colors
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    RED = (255, 0, 0)
    YELLOW = (255, 255, 0)

    # Menu settings
    menu_options = ["Start Game", "Quit"]  # Menu options
    selected_option = 0  # Default selected menu option
    title = "Astro Assault"  # Game title

    # Game states
    MENU = "menu"
    GAME = "game"
    game_state = MENU  # Start the game in the menu
    laser_sound_playing = False  # Track whether the laser sound is playing

    main_loop()  # Start the main game loop
