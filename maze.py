import pygame
import random
import time

WIDTH, HEIGHT = 600, 600
GRID = 20
ROWS, COLS = HEIGHT // GRID, WIDTH // GRID
WHITE, BLACK, GREEN, RED, BLUE = (255, 255, 255), (0, 0, 0), (0, 255, 0), (255, 0, 0), (0, 0, 255)

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
font = pygame.font.Font(None, 30)

def generate_maze():
    maze = [[0 for _ in range(COLS)] for _ in range(ROWS)]
    for _ in range(50): #50 walls
        x, y = random.randint(0, COLS-1), random.randint(0, ROWS-1)
        maze[y][x] = 1 #walls
    return maze


class Player:
    def __init__(self):
        self.x, self.y = 0, 0 

    def move(self, dx, dy, maze):
        if 0 <= self.x + dx < COLS and 0 <= self.y + dy < ROWS and maze[self.y + dy][self.x + dx] == 0:
            self.x += dx
            self.y += dy


def main():
    player = Player()
    maze = generate_maze()
    exit_x, exit_y = COLS-1, ROWS-1  
    maze[exit_y][exit_x] = 2 

    start_time = time.time()
    running = True

    while running:
        screen.fill(WHITE)

   
        for y in range(ROWS):
            for x in range(COLS):
                if maze[y][x] == 1:
                    pygame.draw.rect(screen, BLACK, (x * GRID, y * GRID, GRID, GRID))
                elif maze[y][x] == 2:
                    pygame.draw.rect(screen, GREEN, (x * GRID, y * GRID, GRID, GRID))

        pygame.draw.rect(screen, RED, (player.x * GRID, player.y * GRID, GRID, GRID))


        escape_time = round(time.time() - start_time, 1)
        timer_text = font.render(f"Time: {escape_time} sec", True, BLUE)
        screen.blit(timer_text, (10, 10))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    player.move(-1, 0, maze)
                elif event.key == pygame.K_RIGHT:
                    player.move(1, 0, maze)
                elif event.key == pygame.K_UP:
                    player.move(0, -1, maze)
                elif event.key == pygame.K_DOWN:
                    player.move(0, 1, maze)

        if player.x == exit_x and player.y == exit_y-1 or player.x == exit_x-1 and player.y == exit_y:
            win_text = font.render(f"🎉 Escaped in {escape_time} sec!", True, (0, 200, 0))
            screen.blit(win_text, (WIDTH // 2 - 100, HEIGHT // 2))
            pygame.display.flip()
            pygame.time.delay(3000)  
            pygame.quit() 
            return  

        if escape_time >= 100:
            lose_text = font.render("⏳ Time's up! Try again.", True, (200, 0, 0))
            screen.blit(lose_text, (WIDTH // 2 - 100, HEIGHT // 2))
            pygame.display.flip()
            pygame.time.delay(3000)
            pygame.quit()  # **Properly exits when time is up**
            return  # Exit function

        pygame.display.flip()
        clock.tick(10)  # Limit FPS

    pygame.quit()

# Run the game
if __name__ == "__main__":
    main()
