import pygame
import sys
from entities.character import Character
from weapons.pistol import Pistol
from weapons.aura import Aura
from weapons.flamethrower import Flamethrower

class Menu:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.Font(None, 74)
        self.small_font = pygame.font.Font(None, 50)
        self.selected_index = 0
        self.selected_character = None  # To store the chosen character

        # Main menu options
        self.options = ["Start Game", "Character Selection", "Upgrades", "Options", "Quit"]
        self.option_rects = []  # To store the rectangles for each option

        # Character selection variables
        self.characters = [
            Character("Warrior", health=150, armor=10, speed=5.0, damage=1.2, attack_speed=0.9, radius=1.0,
                      starting_weapon=Pistol()),
            Character("Mage", health=100, armor=5, speed=5, damage=1.5, attack_speed=1.1, radius=1.5,
                      starting_weapon=Aura()),
            Character("Rogue", health=80, armor=3, speed=5, damage=1.3, attack_speed=1.5, radius=1.0,
                      starting_weapon=Flamethrower()),
        ]
        self.current_character_index = 0
        self.in_character_selection = False  # Track if we're in the character selection screen

        # Initialize Pygame's mixer and load music
        pygame.mixer.init()
        pygame.mixer.music.load('assets/sounds/menu_music.mp3')
        pygame.mixer.music.set_volume(0.5)  # Set volume to 50%
        pygame.mixer.music.play(-1)  # Play the music in a loop

    def draw(self):
        self.screen.fill((0, 0, 0))

        if self.in_character_selection:
            self.draw_character_selection()
        else:
            self.option_rects = []  # Clear the previous rectangles
            for i, option in enumerate(self.options):
                color = (255, 255, 255) if i == self.selected_index else (100, 100, 100)
                text = self.font.render(option, True, color)
                rect = text.get_rect(center=(self.screen.get_width() // 2, 200 + i * 100))
                self.screen.blit(text, rect)
                self.option_rects.append(rect)

        pygame.display.flip()

    def draw_character_selection(self):
        # Placeholder for the character model
        model_rect = pygame.Rect(self.screen.get_width() // 4 - 150, self.screen.get_height() // 2 - 150, 300, 300)
        pygame.draw.rect(self.screen, (255, 255, 255), model_rect, 2)

        # Draw the selected character's name and attributes
        character = self.characters[self.current_character_index]
        name_text = self.font.render(character.name, True, (255, 255, 255))
        name_rect = name_text.get_rect(center=(3 * self.screen.get_width() // 4, 100))
        self.screen.blit(name_text, name_rect)

        # Display character stats next to the model placeholder
        stats_text = [
            f"Health: {character.health}",
            f"Armor: {character.armor}",
            f"Speed: {character.speed}",
            f"Damage: {character.damage}",
            f"Attack Speed: {character.attack_speed}",
            f"Radius: {character.radius}",
        ]

        for i, stat in enumerate(stats_text):
            stat_text = self.small_font.render(stat, True, (255, 255, 255))
            stat_rect = stat_text.get_rect(topleft=(3 * self.screen.get_width() // 4 - 150, 200 + i * 50))
            self.screen.blit(stat_text, stat_rect)

        # Left and right arrows for scrolling
        left_arrow = self.small_font.render("<", True, (255, 255, 255))
        right_arrow = self.small_font.render(">", True, (255, 255, 255))

        left_rect = left_arrow.get_rect(center=(self.screen.get_width() // 4 - 200, self.screen.get_height() // 2))
        right_rect = right_arrow.get_rect(center=(self.screen.get_width() // 4 + 200, self.screen.get_height() // 2))

        self.screen.blit(left_arrow, left_rect)
        self.screen.blit(right_arrow, right_rect)

        # Confirm and Back options
        confirm_text = self.small_font.render("Confirm", True, (255, 255, 255))
        back_text = self.small_font.render("Back", True, (255, 255, 255))

        confirm_rect = confirm_text.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() - 100))
        back_rect = back_text.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() - 50))

        self.screen.blit(confirm_text, confirm_rect)
        self.screen.blit(back_text, back_rect)

        self.character_selection_rects = {
            "left": left_rect,
            "right": right_rect,
            "confirm": confirm_rect,
            "back": back_rect
        }

    def run(self):
        while True:
            self.draw()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if self.in_character_selection:
                        self.handle_character_selection_keys(event.key)
                    else:
                        self.handle_main_menu_keys(event.key)
                elif event.type == pygame.MOUSEMOTION:
                    if not self.in_character_selection:
                        self.handle_mouse_motion(event.pos)
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if self.in_character_selection:
                        self.handle_character_selection_click(event.pos)
                    else:
                        self.handle_main_menu_click(event.pos)

    def handle_main_menu_keys(self, key):
        if key == pygame.K_DOWN:
            self.selected_index = (self.selected_index + 1) % len(self.options)
        elif key == pygame.K_UP:
            self.selected_index = (self.selected_index - 1) % len(self.options)
        elif key == pygame.K_RETURN:
            self.execute_option()

    def handle_main_menu_click(self, mouse_pos):
        for i, rect in enumerate(self.option_rects):
            if rect.collidepoint(mouse_pos):
                self.selected_index = i
                self.execute_option()
                break

    def handle_mouse_motion(self, mouse_pos):
        for i, rect in enumerate(self.option_rects):
            if rect.collidepoint(mouse_pos):
                self.selected_index = i
                break

    def handle_character_selection_keys(self, key):
        if key == pygame.K_LEFT:
            self.current_character_index = (self.current_character_index - 1) % len(self.characters)
        elif key == pygame.K_RIGHT:
            self.current_character_index = (self.current_character_index + 1) % len(self.characters)
        elif key == pygame.K_RETURN:
            self.confirm_character_selection()
        elif key == pygame.K_BACKSPACE:
            self.in_character_selection = False  # Go back to the main menu

    def handle_character_selection_click(self, mouse_pos):
        if self.character_selection_rects["left"].collidepoint(mouse_pos):
            self.current_character_index = (self.current_character_index - 1) % len(self.characters)
        elif self.character_selection_rects["right"].collidepoint(mouse_pos):
            self.current_character_index = (self.current_character_index + 1) % len(self.characters)
        elif self.character_selection_rects["confirm"].collidepoint(mouse_pos):
            self.confirm_character_selection()
        elif self.character_selection_rects["back"].collidepoint(mouse_pos):
            self.in_character_selection = False  # Go back to the main menu

    def confirm_character_selection(self):
        self.selected_character = self.characters[self.current_character_index]
        print(f"Selected character: {self.selected_character.name}")
        self.in_character_selection = False  # Go back to the main menu after confirming

    def execute_option(self):
        selected_option = self.options[self.selected_index]
        if selected_option == "Start Game":
            self.start_game()
        elif selected_option == "Character Selection":
            self.in_character_selection = True
        elif selected_option == "Upgrades":
            self.upgrades()
        elif selected_option == "Options":
            self.options_menu()
        elif selected_option == "Quit":
            pygame.quit()
            sys.exit()

    def start_game(self):
        if self.selected_character:
            from game_logic.game import Game  # Import here to avoid circular imports
            game = Game(character=self.selected_character)  # Pass the selected character to the game
            game.run()
        else:
            print("Please select a character first!")

    def upgrades(self):
        print("Upgrades screen will be implemented later")

    def options_menu(self):
        print("Options screen will be implemented later")
