import unittest
import curses
from src.snake import create_initial_state, check_collision, update_state

class TestSnakeGame(unittest.TestCase):

    def test_create_initial_state(self):
        screen_height = 20
        screen_width = 40
        state = create_initial_state(screen_height, screen_width)
        self.assertEqual(len(state['snake']), 3)
        self.assertIn(state['snake'][0], [[screen_height // 2, screen_width // 4 - i] for i in range(3)])
        self.assertEqual(state['score'], 0)
        self.assertFalse(state['game_over'])

    def test_check_collision_with_walls(self):
        screen_height = 20
        screen_width = 40
        state = {
            'snake': [[0, 0], [1, 0], [2, 0]],
            'food': [5, 5],
            'score': 0,
            'game_over': False
        }
        # Simulate collision with the wall
        state['snake'][0] = [-1, 0]  # Top wall
        self.assertTrue(check_collision(state, screen_height, screen_width))
        state['snake'][0] = [0, -1]  # Left wall
        self.assertTrue(check_collision(state, screen_height, screen_width))
        state['snake'][0] = [screen_height, 0]  # Bottom wall
        self.assertTrue(check_collision(state, screen_height, screen_width))
        state['snake'][0] = [0, screen_width]  # Right wall
        self.assertTrue(check_collision(state, screen_height, screen_width))

    def test_check_collision_with_self(self):
        screen_height = 20
        screen_width = 40
        state = {
            'snake': [[5, 5], [5, 6], [5, 7]],
            'food': [5, 10],
            'score': 0,
            'game_over': False
        }
        # Simulate collision with itself
        state['snake'].insert(0, [5, 6])  # Head collides with second segment
        self.assertTrue(check_collision(state, screen_height, screen_width))

    def test_update_state(self):
        screen_height = 20
        screen_width = 40
        state = create_initial_state(screen_height, screen_width)
        initial_head_position = state['snake'][0][:]  # Copy the initial head position
        key = curses.KEY_RIGHT
        new_state = update_state(state, key, screen_height, screen_width)
        # Check if the snake has moved right
        self.assertEqual(new_state['snake'][0][1], initial_head_position[1] + 1)

# More tests can be added for other functions like update_state, render, etc.

if __name__ == '__main__':
    unittest.main()