import pygame

class Player:
    def __init__(self, x, y, image_path, speed):
        self.x = x
        self.y = y
        self.image = pygame.image.load(f'images/{image_path}')
        self.rect = self.image.get_rect(topleft=(x, y))
        self.speed = speed
        self.health = 100
        self.max_health = 100
        self.armor = 0
        self.invincible = False
        self.invincible_time = 0
        self.invincible_duration = 1000  # 1 second of invincibility after taking damage
        self.can_shoot = True  # Initialize the can_shoot attribute
        self.is_alive = True

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))
        self.draw_health_bar(screen)

    def draw_health_bar(self, screen):
        bar_width = 100
        bar_height = 10
        health_ratio = self.health / self.max_health
        health_bar_width = int(bar_width * health_ratio)

        health_bar_x = self.rect.centerx - (bar_width // 2)
        health_bar_y = self.rect.top - 25

        pygame.draw.rect(screen, (255, 0, 0), (health_bar_x, health_bar_y, bar_width, bar_height))
        pygame.draw.rect(screen, (0, 255, 0), (health_bar_x, health_bar_y, health_bar_width, bar_height))

        font = pygame.font.Font(None, 24)
        health_text = f"{int(self.health)}/{self.max_health}"
        text = font.render(health_text, True, (255, 255, 255))
        text_rect = text.get_rect(center=(self.rect.centerx, health_bar_y - 10))
        screen.blit(text, text_rect)

    def move(self, keys, screen_width, screen_height):
        if keys[pygame.K_a] and self.x > 0:
            self.x -= self.speed
        if keys[pygame.K_d] and self.x < screen_width - self.rect.width:
            self.x += self.speed
        if keys[pygame.K_w] and self.y > 0:
            self.y -= self.speed
        if keys[pygame.K_s] and self.y < screen_height - self.rect.height:
            self.y += self.speed
        self.rect.topleft = (self.x, self.y)

    def take_damage(self, damage):
        if not self.invincible:
            effective_damage = max(damage - self.armor, 0)
            self.health -= effective_damage
            self.invincible = True
            self.invincible_time = pygame.time.get_ticks()

            if self.health <= 0:
                self.health = 0
                self.is_alive = False  # Player is dead

            return effective_damage
        return 0

    def update_invincibility(self):
        if self.invincible:
            current_time = pygame.time.get_ticks()
            if current_time - self.invincible_time > self.invincible_duration:
                self.invincible = False  # End invincibility

    def die(self):
        print("Player has died")
        # Handle player's death
