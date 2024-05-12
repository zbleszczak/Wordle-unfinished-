import pygame
import sys
import random

# Define colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)

# Initialize Pygame
pygame.init()

# Set the size of the game window
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Set the title of the game window
pygame.display.set_caption("Word Guessing Game")

# Define a font for the text
font = pygame.font.Font(None, 50)

# Define a list of words to choose from
word_list = ["apple", "banana", "cherry", "orange", "pear"]

# Choose a random word from the list
secret_word = word_list[random.randint(0, len(word_list)-1)]

# Split the word into individual letters separated by spaces
word_letters = " ".join(list(secret_word))

# Create a list of empty strings with the same length as the word, using Unicode character for a square
display_letters = ["-" if c != " " else " " for c in word_letters]

# Define the number of attempts allowed
num_guesses = 6

# Define a variable to hold the player's word
player_word = ""

# Define a variable to hold the feedback message
feedback_text = ""

# Define a variable to hold the input box text
input_box_text = ""

bad_guesses = []

# Define a function to display the word squares and the feedback message
def display_word_and_feedback():
    global input_box_text, display_letters, feedback_text, num_guesses, bad_guesses

    screen.fill((255, 255, 255))

    # Define a center position for the game window
    center_x = SCREEN_WIDTH // 2
    center_y = SCREEN_HEIGHT // 2

    # Define a font for the text
    font = pygame.font.Font(None, 36)

    # Draw the input box
    input_box_width = 360
    input_box_height = 40
    input_box_x = center_x - input_box_width // 2
    input_box_y = center_y - 50
    pygame.draw.rect(screen, (0, 0, 0), (input_box_x, input_box_y, input_box_width, input_box_height), 2)
    input_box_surface = font.render(input_box_text, True, (0, 0, 0))
    input_box_text_x = input_box_x + 5
    input_box_text_y = input_box_y + input_box_height // 2 - input_box_surface.get_height() // 2
    screen.blit(input_box_surface, (input_box_text_x, input_box_text_y))

    # Draw the bad guesses list
    bad_guesses_surface = font.render("Bad guesses: " + ", ".join(bad_guesses), True, (255, 0, 0))
    bad_guesses_text_x = center_x - bad_guesses_surface.get_width() // 2
    bad_guesses_text_y = center_y + 50
    screen.blit(bad_guesses_surface, (bad_guesses_text_x, bad_guesses_text_y))

    # Draw the word squares
    display_letters_surface = font.render(" ".join(display_letters), True, (0, 0, 0))
    display_letters_x = center_x - display_letters_surface.get_width() // 2
    display_letters_y = center_y - 100
    screen.blit(display_letters_surface, (display_letters_x, display_letters_y))

    # Draw the feedback message
    feedback_text_surface = font.render(feedback_text, True, (0, 0, 255))
    feedback_text_x = center_x - feedback_text_surface.get_width() // 2
    feedback_text_y = center_y + 100
    screen.blit(feedback_text_surface, (feedback_text_x, feedback_text_y))

    # Draw the remaining guesses count
    remaining_guesses_surface = font.render(f"Remaining guesses: {num_guesses}", True, (0, 0, 0))
    remaining_guesses_x = center_x - remaining_guesses_surface.get_width() // 2
    remaining_guesses_y = center_y + 150
    screen.blit(remaining_guesses_surface, (remaining_guesses_x, remaining_guesses_y))

    pygame.display.update()

def handle_guess(guess):
    global num_guesses, feedback_text, display_letters, input_box_text, bad_guesses

    if guess == "":
        feedback_text = "Please enter a guess."
        return

    if guess == secret_word:
        feedback_text = "Congratulations! You guessed the word!"
        display_letters = list(secret_word)
        return

    if guess in secret_word:
        for i in range(len(secret_word)):
            if secret_word[i] == guess:
                if display_letters[i * 2] == "-":
                    display_letters[i * 2] = guess
                else:
                    display_letters[i * 2 + 1] = "x"
        feedback_text = f"Good guess! '{guess}' is in the word."
    else:
        if guess not in bad_guesses:
            bad_guesses.append(guess)
            num_guesses -= 1
        feedback_text = f"This guess was bad! You have {num_guesses} guesses left."

    if num_guesses == 0:
        feedback_text = f"Game over! The word was '{secret_word}'. Press any key to play again."

    display_word_and_feedback()
    input_box_text = ""

    # Game loop
while True:
        # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
            elif event.key == pygame.K_BACKSPACE:
                    input_box_text = input_box_text[:-1]
            elif event.key == pygame.K_RETURN:
                    handle_guess(input_box_text.lower())
                    input_box_text = ""
            else:
                    input_box_text += event.unicode

        # Call the function to display the word squares and the feedback message
        display_word_and_feedback()

        # Check if the player has won or lost
        if "-" not in display_letters:
            feedback_text = "Congratulations! You guessed the word!"
        elif num_guesses == 0:
            feedback_text = f"Game over! The word was '{secret_word}'. Press any key to play again."

        # Update the display
        pygame.display.update()