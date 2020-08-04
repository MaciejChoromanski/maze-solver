from utlis import Maze


def main() -> None:
    """Entry point of the script"""

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
        print('The solution has been saved!')


if __name__ == '__main__':
    main()
