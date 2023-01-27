# Kris Vuong
# April 29 2022
# Pygame drawing of Recursive Maze Solver

import pygame

pygame.init()


class Draw:
    def __init__(self):
        pygame.font.init()  # Initialize fonts
        self.screen = ""
        self.maze = ""  # Defined later in code
        self.my_font = pygame.font.SysFont('Helvetica', 30)  # Choose font and size
        self.start_text = self.my_font.render("S", False, (0, 0, 0))  # Set start text
        self.end_text = self.my_font.render("E", False, (0, 0, 0))  # Set end text

    def draw_rect(self):  # Called everytime redraw is called
        surf = pygame.Surface((30, 30))  # One coordinate in maze = 30px x 30px

        for i in range(len(self.maze)):  # Iterate through entire 2D maze
            for j in range(len(self.maze[i])):
                # Set walls of maze to black
                if self.maze[i][j] == "#":
                    surf.fill((0, 0, 0))
                    self.screen.blit(surf, (j * 30, i * 30))
                # Set START of maze as green
                if self.maze[i][j] == "S":
                    surf.fill((0, 204, 0))
                    self.screen.blit(surf, (j * 30, i * 30))
                    self.screen.blit(self.start_text, (j * 30 + 5, i * 30 + 1))  # Blit "S" to start
                # Set END of maze as yellow
                if self.maze[i][j] == "G":
                    surf.fill((0, 204, 0))
                    self.screen.blit(surf, (j * 30, i * 30))
                    self.screen.blit(self.end_text, (j * 30 + 6, i * 30 + 2))  # Blit "E" to end
                # Set correct paths as dark green
                if self.maze[i][j] == "+":
                    surf.fill((0, 102, 0))
                    self.screen.blit(surf, (j * 30, i * 30))
                # Set incorrect paths as red
                if self.maze[i][j] == "X":
                    surf.fill((204, 0, 0))
                    self.screen.blit(surf, (j * 30, i * 30))

    def setup(self, row, col):  # Called ONCE everytime code is ran
        screen = pygame.display.set_mode((col * 30, row * 30))  # Set up pygame window
        screen.fill((255, 255, 255))  # Fill window with white (background)
        self.screen = screen  # Assign screen attribute
        pygame.display.set_caption("Maze Solver")

    def redraw(self, maze):  # Called everytime find_path() is called
        clock = pygame.time.Clock()
        clock.tick(240)
        self.maze = maze  # Maze attribute assigned
        self.draw_rect()  # Redraw maze with updated moves
        for event in pygame.event.get():  # If user quits pygame window
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return False

        pygame.display.update()  # Update pygame window
        return True

    def end(self):  # Show solved maze on display
        running = True
        while running:
            running = self.redraw(self.maze)


pygame.quit()
