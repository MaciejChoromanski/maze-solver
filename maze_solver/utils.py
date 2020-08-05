from __future__ import annotations

import getopt
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Tuple, List, Union

from PIL import Image, ImageFile


def get_input_data() -> Tuple[str, Union[str, None]]:
    """Returns the data with which the script should was run"""

    short_options = "hf:t"
    long_options = ["help", "file=", 'test']
    cmd_arguments = sys.argv
    argument_list = cmd_arguments[1:] or ['-t']

    try:
        arguments, values = getopt.getopt(
            argument_list, short_options, long_options
        )
    except getopt.error as err:
        print(str(err))
        sys.exit(2)

    for argument, value in arguments:
        if argument in ("-f", "--file"):
            return 'file', value
        elif argument in ("-h", "--help"):
            return 'help', None
        else:
            return 'test', None


def solve_maze_from_file(path: str) -> None:
    """Reads, solves and saves the solution of the custom maze"""

    def check_response(message: str) -> bool:
        """Returns whether user agrees to proceed or not"""

        response = input(message)

        return response.upper() == 'Y'

    maze = Maze(path)
    print(f'The maze \'{maze.name}\' has been loaded!')
    print('Solving the maze...')
    maze.solve()
    print('The maze has been solved!')
    print('Drawing path...')
    maze.draw_path()
    print('The path has been drawn!')

    if check_response('Would you like to see the solution? y/n default: n\n'):
        maze.show()

    if check_response('Would you like to save the solution? y/n default: n\n'):
        print('Saving solution...')
        maze.save_solution()
        print('The solution has been saved in \'solutions\' directory!')


def solve_test_mazes() -> None:
    """Reads, solves and saves the solution of the test mazes"""

    for i in range(1, 5):
        maze = Maze(f'test_mazes/maze_0{i}.png')
        print(f'The maze \'{maze.name}\' has been loaded!')
        print('Solving the maze...')
        maze.solve()
        print('The maze has been solved!')
        print('Drawing path...')
        maze.draw_path()
        print('The path has been drawn!')
        print('Saving solution...')
        maze.save_solution()
        print('The solution has been saved in \'solutions\' directory!')


def display_help() -> None:
    """Displays the help text"""

    print("""
    This script solves mazes from images. The method used to determine where
    the exit is relies on always sticking with the right wall of the maze. The 
    width and the height of the image doesn't matter. However, the image must 
    contain only 3 colors: 
        1. Grey - this one represents entrance and exit of the maze, 
        2. Black - this one represents the walls of the maze,
        3. White - this one represents the walking space of the maze.
        
    Additional info: 
        1. The entrance of the maze must be located at (0, 0) pixel.
        2. The exit of the maze must be located at (<max_width>, <max_height>) 
           pixel.
        
    Options:
        -t --test - default option, solves mazes from 'test_mazes' directory,
        -f --file - enables solving custom maze if the path to it is provided,
        -h --help - displays the help text.
    """)


def _solve_the_maze(maze: Maze) -> None:
    """Runs the necessary operations to solve the maze"""


class Maze:
    """Represents a maze based on an image"""

    _path: str = None
    _name: str = None
    _image: ImageFile = None
    _image_loaded = None
    _size: Tuple[int, int] = None
    _entrance: Tuple[int, int] = None
    _exit: Tuple[int, int] = None
    _moves: List[Position] = None
    _solved: bool = False

    def __init__(self, path: str = None, name: str = None) -> None:
        """Initializes Maze object based on the given path"""

        self._path = path
        self._name = name
        self._image = Image.open(path)
        self._image_loaded = self._image.load()
        self._size = self._image.size
        self._moves = []

    def __repr__(self) -> str:
        """Representation of the Maze"""

        return f'<Maze: {self._path}>'

    @property
    def name(self) -> str:
        """Returns the name of the maze"""

        if not self._name:
            self._name = self._path.split('/')[-1].split('.')[0]

        return self._name

    @property
    def size(self) -> Tuple[int, int]:
        """Returns the size of the maze"""

        return self._size

    @property
    def entrance(self) -> Tuple[int, int]:
        """Returns the coordinates of the entrance"""

        if not self._entrance:
            if self._get_pixel_color(0, 0) != 'grey':
                raise ValueError('The entrance must be located at (0, 0)')

            self._entrance = (0, 0)

        return self._entrance

    @property
    def exit(self) -> Tuple[int, int]:
        """Returns the coordinates of the entrance"""

        if not self._exit:
            exit_position = (self.size[0] - 1, self.size[1] - 1)
            if self._get_pixel_color(*exit_position) != 'grey':
                message = f'The exit must be located at {self._size}'
                raise ValueError(message)

            self._exit = exit_position

        return self._exit

    def solve(self) -> None:
        """Tries to find the path from the entrance to the exit of the maze"""

        current_position = Position(*self.entrance)
        current_direction = None
        while current_position != self.exit:
            self._moves.append(current_position)
            move_by, direction = self._get_next_step(
                current_position, current_direction
            )
            current_position += move_by
            if direction != current_direction:
                current_direction = direction

        self._moves.append(Position(*self.exit))
        self._solved = True

    def draw_path(self) -> None:
        """Changes pixel color to show the path"""

        red = (255, 0, 0, 255)
        for position in self._moves:
            self._image_loaded[position.x, position.y] = red

    def show(self) -> None:
        """Shows the maze in it's current state"""

        self._image.show()

    def save_solution(self, extension: str = 'png') -> None:
        """Saves the solution of the maze as an image file"""

        if not self._solved:
            raise ValueError('The maze is not solved yet.')

        Path('maze_solutions').mkdir(parents=True, exist_ok=True)
        self._image.save(f'maze_solutions/{self.name}.{extension}')

    def _get_pixel_color(self, x: int, y: int) -> str:
        """Returns the color of the pixel located on (x, y)"""

        colors = {
            (0, 0, 0): 'black',
            (128, 128, 128): 'grey',
            (255, 255, 255): 'white',
            (255, 0, 0): 'red',
        }
        color = self._image_loaded[x, y][:-1]

        return colors[color]

    def _get_next_step(
        self, current_position: Position, current_direction: str = None
    ) -> Tuple[Tuple[int, int], str]:
        """Makes a move based on position and direction"""

        if current_direction is None:
            current_direction = 'right'

        possible_steps = {
            'down': (0, 1),
            'right': (1, 0),
            'up': (0, -1),
            'left': (-1, 0),
        }
        paths_prioritized_by_direction = {
            'down': ['left', 'down', 'right', 'up'],
            'left': ['up', 'left', 'down', 'right'],
            'up': ['right', 'up', 'left', 'down'],
            'right': ['down', 'right', 'up', 'left'],
        }
        ordered_paths = paths_prioritized_by_direction[current_direction]
        walls = {}
        for step in possible_steps:
            walls[step] = not self._is_path(
                current_position + possible_steps[step]
            )

        for path in ordered_paths:
            if not walls[path]:
                return possible_steps[path], path

    def _is_path(self, pixel: Position) -> bool:
        """Checks whether a pixel is a path or not"""

        try:
            is_white = self._get_pixel_color(pixel.x, pixel.y) == 'white'
            is_exit = (pixel.x, pixel.y) == self.exit
            return is_white or is_exit
        except IndexError:
            return False


@dataclass
class Position:
    """Defines the position in the maze"""

    x: int
    y: int

    def __eq__(self, other: Union[Tuple[int, int], Position]) -> bool:
        """Defines how the Position should be compared"""

        if isinstance(other, tuple):
            return (self.x, self.y) == other

        return self.x == other.x and self.y == other.y

    def __add__(self, other: Union[Tuple[int, int], Position]) -> Position:
        """Defines how the '+' should be handled when used with Position"""

        if isinstance(other, tuple):
            return Position(self.x + other[0], self.y + other[1])

        return Position(self.x + other.x, self.y + other.y)

    def __sub__(self, other: Union[Tuple[int, int], Position]) -> Position:
        """Defines how the '-' should be handled when used with Position"""

        if isinstance(other, tuple):
            return Position(self.x - other[0], self.y - other[1])

        return Position(self.x - other.x, self.y - other.y)

    def __repr__(self) -> str:
        """Representation of the Position"""

        return f'<Position: ({self.x}, {self.y})>'
