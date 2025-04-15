from the_snake import Snake

def test_snake_reset():
    snake = Snake()
    snake.length = 5
    snake.reset()
    assert snake.length == 1

def test_self_collision():
    snake = Snake()
    snake.positions = [(100, 100), (120, 100), (140, 100), (120, 100)]
    snake.move()
    assert len(snake.positions) == 1
