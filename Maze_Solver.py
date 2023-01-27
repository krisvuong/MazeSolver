# Kris Vuong
# April 29 2022
# Recursive Maze Solver

from random import randint
import Draw_Maze

# QUESTIONS
"""
What happens if instead of searching in the order North, East, South, West, FIND PATH searches North, South, East, West?
- A solution will still be found, but the algorithm searches the possible paths in a different order
- The time taken to find the solution path may vary

When FIND-PATH returns False, does that mean there is no path from the start to the goal?
- False is returned when the CURRENT path meets a wall or a pathway already taken
- A False return value means that the current path is not the correct solution
- The find_path method recurses until it finds the correct pathway, then it returns True
- If the FINAL return of find_path is False, then there is no path from the start to the goal
    - But the maze generator provided always has a solution 

Can parts of the maze be searched by FIND-PATH more than once? How does the algorithm deal with this situation?
- No
- Everytime a path is reached, the string in this position is changed to "+"
- One of the base cases checks if the next desired position is "+"
    - If this is True, then this pathway is returned as False
    - This prevents the algorithm from traversing the same path more than once
"""


class MazeSolver:
    def __init__(self):
        self.row = ""  # Starting position row
        self.col = ""  # Starting position column
        self.start = ""
        self.maze_list = ""
        self.drawing = Draw_Maze.Draw()
        self.count = 0  # Used to debug specific problem in find_path
        print(self.load_maze.__doc__)

    def load_maze(self, file_name):
        """
        Loads maze from text file, returns as list

        :param file_name: name of text file containing 2D maze
        :type file_name: str
        :rtype: list
        :return: maze as a list of strings
        """
        file_in = open(file_name)  # Open maze text file
        lines = file_in.readlines()  # Save each line in list
        file_in.close()  # CLose maze text file
        lines = [i[0:-1] for i in lines]  # Get rid of blank lines
        return lines  # Return list of strings of maze

    def print_maze(self, maze_list):
        """
        Prints 2D maze to terminal

        :param maze_list: maze as list of strings
        :type maze_list: list
        """
        for i in maze_list:
            print(i)

    def random_coordinates_generator(self, maze_list):
        """
        Generates two random points on maze as start/end points

        :param maze_list: maze as list of strings
        :type maze_list: list
        :rtype: list
        :return: two coordinates representing start/end points
        """
        temp_coords = []

        for i in range(2):  # Repeat twice to get two positions
            valid = False
            while not valid:  # Validates that position is blank (not '#')
                row = randint(0, len(maze_list) - 1)  # Get random number within number of rows
                col = randint(0, len(maze_list[0]) - 1)  # Get random number within number of columns
                if maze_list[row][col] == ' ':  # If position is blank
                    temp_coords.append([row, col])  # Append this position to temporary list
                    valid = True  # Exit while loop

        label = ['S', 'G']  # Labels for set "S" and "G" on maze
        for i in range(2):  # Repeat twice (for start and end)
            temp = list(maze_list[temp_coords[i][0]])  # Convert row with start/end coordinates to list
            temp[temp_coords[i][1]] = label[i]  # Replace coordinates with "S" or "G"
            temp = ''.join(temp)  # Convert list back to string
            maze_list[temp_coords[i][0]] = temp  # Update actual maze list

        return temp_coords  # Return list with start and end positions

    def find_path(self, row, col):
        """
        Finds a path from the start to end position

        :param row: row of start point
        :type row: int
        :param col: col of start point
        :type col: int
        :rtype: bool
        :return: True if a path is found from start to end, otherwise False
        """
        self.count += 1  # Tracks number of moves (used to troubleshoot an issue)
        self.drawing.redraw(self.maze_list)  # Draw maze with pygame

        if self.maze_list[row][col] == "G":  # If reached the end goal (correct solution)
            return True
        elif self.maze_list[row][col] == "#":  # If reached a wall
            return False
        elif self.maze_list[row][col] == "X" or self.maze_list[row][col] == "+":  # If reached a course already taken
            return False
        elif self.count != 1 and self.maze_list[row][col] == "S":  # Prevent error where one step is taken in wrong dir
            return False
        else:  # A valid move can be made
            self.draw_path(row, col, "+")  # Change current position to "+"
            if self.find_path(row - 1, col):  # Try moving NORTH
                return True  # Calls draw function to change solution path to "+"
            if self.find_path(row, col + 1):  # Try moving EAST
                return True
            if self.find_path(row + 1, col):  # Try moving SOUTH
                return True
            if self.find_path(row, col - 1):  # Try moving WEST
                return True
            self.draw_path(row, col, "X")  # If no valid paths are found, change current position to "X"
            return False

    def draw_path(self, row, col, char):  # Only called when correct path is found
        """
        Marks traversed path with an indicator ("+" or "X")

        :param row: row of current position
        :type row: int
        :param col: col of current position
        :type col: int
        :param char: character to replace current position ("+" for valid paths, "X" otherwise)
        :type char: str
        """
        if not ((row, col) == (self.row, self.col)):  # If current pos is not starting pos (so it doesn't replace "S")
            self.maze_list[row] = list(self.maze_list[row])  # Change row to list
            self.maze_list[row][col] = char  # Change current position to "+"
            self.maze_list[row] = ''.join(self.maze_list[row])  # Join list as string


# Get user input for maze text file
file = str(input("Enter maze file name: "))

# Find path
solve = MazeSolver()  # Create class object

# Load maze
maze = solve.load_maze(file)  # Returns list of maze as strings

# Print blank maze
print("BLANK MAZE:")
solve.print_maze(maze)

# Find random coordinates (of start and end points)
coords = solve.random_coordinates_generator(maze)
start = coords[0]
end = coords[1]

# Assign attributes to class
solve.start = start
solve.row = start[0]  # Starting position row
solve.col = start[1]  # Starting position column
solve.maze_list = maze  # List of maze

# Print maze with start and end positions
print()
print("MAZE WITH START/END POSITIONS:")
solve.print_maze(maze)

# SETUP PYGAME WINDOW
solve.drawing.setup(len(maze), len(maze[0]))

# Find solution path in maze
solve.find_path(solve.row, solve.col)  # Returns True when finished

# Print maze with solution
print()
print("MAZE WITH SOLUTION:")
solve.print_maze(maze)

# Show solved maze on display
solve.drawing.end()
