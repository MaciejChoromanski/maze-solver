from utils import (
    get_input_data,
    solve_maze_from_file,
    solve_test_mazes,
    display_help,
)


def main() -> None:
    """Entry point of the script"""

    mode, value = get_input_data()
    if mode == 'file':
        solve_maze_from_file(value)
    elif mode == 'test':
        solve_test_mazes()
    else:
        display_help()


if __name__ == '__main__':
    main()
