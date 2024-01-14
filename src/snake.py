import random
import curses
import logging
import time

# Set up logging
logging.basicConfig(filename='snake_game.log', level=logging.INFO, format='%(asctime)s:%(levelname)s:%(message)s')

def create_initial_state(screen_height, screen_width):
    # Place the initial snake position so it has room to move to the right
    snake_initial_position = [[screen_height // 2, screen_width // 4 - i] for i in range(3)]
    food_initial_position = [screen_height // 2, screen_width // 2]
    return {
        'snake': snake_initial_position,
        'food': food_initial_position,
        'score': 0,
        'game_over': False
    }

def place_food(state, screen_height, screen_width):
    while True:
        food = [random.randint(1, screen_height - 2), random.randint(1, screen_width - 2)]
        if food not in state['snake']:
            return food

def move_snake(state, direction, screen_height, screen_width):
    head_y, head_x = state['snake'][0]
    if direction == curses.KEY_DOWN:
        head_y += 1
    elif direction == curses.KEY_UP:
        head_y -= 1
    elif direction == curses.KEY_LEFT:
        head_x -= 1
    elif direction == curses.KEY_RIGHT:
        head_x += 1

    # Ensure the new head position wraps around the screen
    head_y = head_y % screen_height
    head_x = head_x % screen_width

    new_head = [head_y, head_x]
    new_snake = [new_head] + state['snake'][:-1]
    return new_snake

def check_collision(state, screen_height, screen_width):
    # Get the snake's head position
    head = state['snake'][0]
    # Check if the snake has collided with the walls
    if head[0] >= screen_height or head[0] < 0 or head[1] >= screen_width or head[1] < 0:
        return True
    # Check if the snake has collided with itself
    if head in state['snake'][1:]:
        return True
    return False

def update_state(state, key, screen_height, screen_width):
    new_state = state.copy()
    new_state['snake'] = move_snake(state, key, screen_height, screen_width)
    if new_state['snake'][0] == state['food']:
        new_state['food'] = place_food(state, screen_height, screen_width)
        new_state['score'] += 1
        new_state['snake'].append(state['snake'][-1])
    if check_collision(new_state, screen_height, screen_width):
        new_state['game_over'] = True
    return new_state

def render(state, window):
    window.clear()
    for y, x in state['snake']:
        window.addch(y % window.getmaxyx()[0], x % window.getmaxyx()[1], curses.ACS_CKBOARD)
    window.addch(state['food'][0] % window.getmaxyx()[0], state['food'][1] % window.getmaxyx()[1], curses.ACS_PI)
    score_text = f"Score: {state['score']}"
    window.addstr(0, 0, score_text)
    window.refresh()

def game_loop(window, state):
    screen_height, screen_width = window.getmaxyx()
    key = curses.KEY_RIGHT  # Start by moving to the right
    last_key = key  # Keep track of the last key pressed

    # Set the window to non-blocking mode
    window.nodelay(True)

    # Set the speed of the snake
    speed = 0.1  # Adjust this value to make the snake faster or slower

    while not state['game_over']:
        # Get the next key press
        try:
            key = window.getch()
        except Exception as e:
            logging.error(f"Error getting character: {e}")

        # If no key is pressed, -1 is returned
        # Only update the last_key if a valid key (arrow key) is pressed
        if key in [curses.KEY_RIGHT, curses.KEY_LEFT, curses.KEY_UP, curses.KEY_DOWN]:
            last_key = key

        # Update the game state based on the last key pressed
        state = update_state(state, last_key, screen_height, screen_width)

        # Render the current state
        render(state, window)

        # Check for collision with the snake or the walls
        if check_collision(state, screen_height, screen_width):
            state['game_over'] = True

        # Sleep to control the speed of the game loop
        time.sleep(speed)

    # Print the final score after the game is over
    print(f"Game Over! Your score was: {state['score']}")

def main(window):
    # Initialize the game state
    screen_height, screen_width = window.getmaxyx()
    state = create_initial_state(screen_height, screen_width)
    
    try:
        game_loop(window, state)  # Pass the state to the game loop
    except Exception as e:
        # Terminate curses application before printing to console
        curses.endwin()
        print("The game has crashed due to an unexpected error.")
        print("Error details:", str(e))
        # Log the error
        logging.error(f"Game crashed with error: {e}")
    finally:
        # Ensure the terminal is restored to its original state
        curses.endwin()
        print(f"Game Over! Your score was: {state['score']}")

if __name__ == "__main__":
    try:
        # Initialize curses
        curses.wrapper(main)
    except KeyboardInterrupt:
        # Ensure the terminal is restored to its original state
        curses.endwin()
        print("Game closed by user.")