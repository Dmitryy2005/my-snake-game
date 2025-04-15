import pytest
from the_snake import Snake, Apple, SCREEN_WIDTH, GRID_SIZE

def test_snake_wraparound():
    snake = Snake()
    snake.positions = [(0, 0)]
    snake.direction = (LEFT := (-1, 0))
    snake.move()
    assert snake.positions[0] == (SCREEN_WIDTH - GRID_SIZE, 0)

def test_apple_generation():
    snake = Snake()
    occupied = set(snake.positions)
    apple = Apple(occupied)
    assert apple.position not in occupied
