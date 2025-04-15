import pygame
import random
from typing import List, Tuple, Optional

# Инициализация констант
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE
CENTER_POSITION = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)

# Направления движения
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Цвета
BACKGROUND_COLOR = (0, 0, 0)
BORDER_COLOR = (93, 216, 228)
SNAKE_COLOR = (0, 255, 0)
APPLE_COLOR = (255, 0, 0)

# Скорость игры
SPEED = 10

class GameObject:
    def __init__(self) -> None:
        self.position = CENTER_POSITION
        self.body_color: Optional[Tuple[int, int, int]] = None

    def draw(self, surface: pygame.Surface) -> None:
        raise NotImplementedError("Метод draw должен быть реализован в подклассах")


class Apple(GameObject):
    def __init__(self, snake_positions: List[Tuple[int, int]]) -> None:
        super().__init__()
        self.body_color = APPLE_COLOR
        self.randomize_position(snake_positions)

    def randomize_position(self, snake_positions: List[Tuple[int, int]]) -> None:
        
        while True:
            self.position = (
                random.randint(0, GRID_WIDTH - 1) * GRID_SIZE,
                random.randint(0, GRID_HEIGHT - 1) * GRID_SIZE
            )
            if self.position not in snake_positions:
                break

    def draw(self, surface: pygame.Surface) -> None:
        """Отрисовывает яблоко на поверхности"""
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(surface, self.body_color, rect)
        pygame.draw.rect(surface, BORDER_COLOR, rect, 1)


class Snake(GameObject):
    """Класс для змейки"""
    def __init__(self) -> None:
        super().__init__()
        self.positions: List[Tuple[int, int]] = [self.position]
        self.direction = RIGHT
        self.next_direction = None
        self.body_color = SNAKE_COLOR
        self.length = 1
        self.last_position = None

    def update_direction(self) -> None:
        """Обновляет направление движения змейки"""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self) -> None:
        """Перемещает змейку"""
        head_x, head_y = self.positions[0]
        dir_x, dir_y = self.direction
        
        new_position = (
            (head_x + dir_x * GRID_SIZE) % SCREEN_WIDTH,
            (head_y + dir_y * GRID_SIZE) % SCREEN_HEIGHT
        )

        # Проверка на самопересечение
        if new_position in self.positions:
            self.reset()
        else:
            self.positions.insert(0, new_position)
            if len(self.positions) > self.length:
                self.last_position = self.positions.pop()

    def reset(self) -> None:
        """Сбрасывает змейку в начальное состояние"""
        self.positions = [CENTER_POSITION]
        self.direction = RIGHT
        self.next_direction = None
        self.length = 1

    def draw(self, surface: pygame.Surface) -> None:
        """Отрисовывает змейку на поверхности"""
        # Отрисовка головы
        head_rect = pygame.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(surface, self.body_color, head_rect)
        pygame.draw.rect(surface, BORDER_COLOR, head_rect, 1)
        
        # Отрисовка тела
        for position in self.positions[1:]:
            rect = pygame.Rect(position, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(surface, self.body_color, rect)
            pygame.draw.rect(surface, BORDER_COLOR, rect, 1)
        
        # Затирание последнего сегмента
        if self.last_position:
            last_rect = pygame.Rect(self.last_position, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(surface, BACKGROUND_COLOR, last_rect)


def handle_keys(snake: Snake) -> bool:
    """Обрабатывает нажатия клавиш"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            return True
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and snake.direction != DOWN:
                snake.next_direction = UP
            elif event.key == pygame.K_DOWN and snake.direction != UP:
                snake.next_direction = DOWN
            elif event.key == pygame.K_LEFT and snake.direction != RIGHT:
                snake.next_direction = LEFT
            elif event.key == pygame.K_RIGHT and snake.direction != LEFT:
                snake.next_direction = RIGHT
            elif event.key == pygame.K_ESCAPE:
                return True
    return False


def main() -> None:
    """Основная функция игры"""
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption('Змейка')
    clock = pygame.time.Clock()
    
    snake = Snake()
    apple = Apple(snake.positions)
    
    running = True
    while running:
        clock.tick(SPEED)
        
        if handle_keys(snake):
            running = False
        
        snake.update_direction()
        snake.move()
        
        # Проверка съедания яблока
        if snake.positions[0] == apple.position:
            snake.length += 1
            apple.randomize_position(snake.positions)
        
        # Отрисовка
        screen.fill(BACKGROUND_COLOR)
        snake.draw(screen)
        apple.draw(screen)
        pygame.display.update()
    
    pygame.quit()


if __name__ == "__main__":
    main()
