import pygame
import random

# Initialize pygame
pygame.init()

# Game Constants
WIDTH, HEIGHT = 400, 600
FPS = 60
GRAVITY = 0.5
JUMP_STRENGTH = -10
PLATFORM_WIDTH = 70
PLATFORM_HEIGHT = 10

# Colors
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)

# Create the game screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Doodle Jump Clone')

# Load player image
doodle_image = pygame.image.load("doodle.png")  # Ensure you have 'doodle.png'
doodle_image = pygame.transform.scale(doodle_image, (40, 40))

clock = pygame.time.Clock()

# Doodle player class
class Doodle:
    def __init__(self):
        self.x = WIDTH // 2
        self.y = HEIGHT - 200
        self.width = 40
        self.height = 40
        self.velocity_x = 0
        self.velocity_y = 0
        self.on_ground = False

    def move(self, platforms):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            self.velocity_x = -5
        elif keys[pygame.K_d]:
            self.velocity_x = 5
        else:
            self.velocity_x = 0

        self.x += self.velocity_x  # Horizontal movement
        self.check_vertical_collision(platforms)  # Check for vertical collisions after horizontal movement

        # Apply gravity if not on the ground
        if not self.on_ground:
            self.velocity_y += GRAVITY

    def jump(self, platforms):
        if self.on_ground:
            self.velocity_y = JUMP_STRENGTH  # Apply jump velocity only when on the ground

        self.check_vertical_collision(platforms)  # Handle vertical collisions during jump

    def check_vertical_collision(self, platforms):
        self.on_ground = False  # Reset this each frame to ensure proper collision detection
        self.y += self.velocity_y  # Apply vertical velocity (falling or jumping)

        # Check collision with each platform
        for platform in platforms:
            if (self.x + self.width > platform.x and self.x < platform.x + platform.width) and \
               (self.y + self.height <= platform.y and self.y + self.height + self.velocity_y >= platform.y):
                self.velocity_y = 0  # Stop downward velocity
                self.y = platform.y - self.height  # Place player on top of platform
                self.on_ground = True  # Mark that the player is on the platform
                break

    def draw(self, screen):
        screen.blit(doodle_image, (self.x, self.y))


# Platform class
class Platform:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = PLATFORM_WIDTH
        self.height = PLATFORM_HEIGHT
        self.color = GREEN

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))


# Main Game Loop
def main():
    doodle = Doodle()
    platforms = [Platform(random.randint(0, WIDTH - PLATFORM_WIDTH), random.randint(0, HEIGHT - PLATFORM_HEIGHT)) for _ in range(12)]
    # Place the doodle above the first platform so it starts on it
    doodle.y = platforms[0].y - doodle.height

    running = True
    while running:
        clock.tick(FPS)
        screen.fill(WHITE)

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Jump with spacebar
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:  # Jump with 'Spacebar'
            doodle.jump(platforms)

        # Update and move the player
        doodle.move(platforms)

        # Generate new platforms if needed
        for platform in platforms:
            platform.y += 0.5  # Move platforms down
            if platform.y > HEIGHT:  # Reset platform to top if it goes off screen
                platform.y = -2
                platform.x =  random.randint(0, WIDTH - PLATFORM_WIDTH) 

        # Draw the player and platforms
        doodle.draw(screen)
        for platform in platforms:
            platform.draw(screen)

        pygame.display.flip()

    pygame.quit()


# Run the game
main()