from pathlib import Path
from unittest import TestCase
from unittest.mock import Mock, patch

from PIL.Image import Image

from maze_solver.utils import Maze, Position


class TestMaze(TestCase):
    """Tests for the Maze class"""

    def setUp(self) -> None:
        """Creates the maze for the tests"""

        self.maze = Maze('test_mazes/maze_01.png')

    def test_name_property_maze_name_not_provided(self) -> None:
        """
        Tests if name property is properly set when
        the maze is created with no name
        """

        self.assertEqual(self.maze.name, 'maze_01')

    def test_name_property_maze_name_provided(self) -> None:
        """
        Tests if name property is properly set when
        the maze is created with a name
        """

        maze = Maze('test_mazes/maze_02.png', name='test')

        self.assertEqual(maze.name, 'test')

    def test_size_property(self) -> None:
        """Test if size property is properly set"""

        size = (202, 202)
        self.maze._size = size

        self.assertEqual(self.maze.size, size)

    def test_entrance_property_raises_ValueError(self) -> None:
        """
        Tests if calling entrance property raises
        ValueError when conditions are met
        """

        self.maze._image_loaded[0, 0] = (0, 0, 0, 255)

        with self.assertRaises(ValueError):
            self.maze.entrance

    def test_entrance_property_set_properly(self) -> None:
        """
        Tests if calling entrance property returns the entrance coordinates
        """

        entrance = self.maze.entrance

        self.assertEqual(entrance, (0, 0))

    def test_exit_property_raises_ValueError(self) -> None:
        """
        Tests if calling exit property raises
        ValueError when conditions are met
        """

        x, y = self.maze.size[0] - 1, self.maze.size[1] - 1
        self.maze._image_loaded[x, y] = (0, 0, 0, 255)

        with self.assertRaises(ValueError):
            self.maze.exit

    def test_exit_property_set_properly(self) -> None:
        """
        Tests if calling exit property returns the entrance coordinates
        """

        exit_ = self.maze.exit
        expected_result = (self.maze.size[0] - 1, self.maze.size[1] - 1)

        self.assertEqual(exit_, expected_result)

    def test_maze_solved_properly(self) -> None:
        """Tests if maze was solved properly"""

        self.maze.solve()

        self.assertNotEqual(self.maze._moves, [])
        self.assertEqual(self.maze._moves[0], self.maze.entrance)
        self.assertEqual(self.maze._moves[-1], self.maze.exit)
        self.assertTrue(self.maze._solved)

    def test_path_drawn_properly(self) -> None:
        """Tests if path of the maze is drawn properly"""

        self.maze._moves = [Mock(x=5, y=7)]
        self.maze.draw_path()

        self.assertEqual(self.maze._image_loaded[5, 7], (255, 0, 0, 255))

    @patch.object(Image, 'show')
    def test_image_showed_successfully(self, mock_show) -> None:
        """Tests if image of the maze is shown successfully"""

        self.maze.show()

        mock_show.assert_called()

    def test_save_solution_raises_ValueError(self) -> None:
        """Tests if ValueError is raise when conditions are met"""

        with self.assertRaises(ValueError):
            self.maze.save_solution()

    @patch.object(Path, 'mkdir')
    @patch.object(Image, 'save')
    def test_maze_saved_successfully(self, mock_save, mock_mkdir) -> None:
        """Tests if maze is saved successfully"""

        self.maze._solved = True
        self.maze.save_solution()

        mock_mkdir.assert_called()
        mock_save.assert_called()


class TestPosition(TestCase):
    """Tests for the Position class"""

    def test_eq_position_to_tuple(self) -> None:
        """Tests if tuple is compared to position properly"""

        self.assertTrue(Position(1, 2) == (1, 2))

    def test_eq_position_to_position(self) -> None:
        """Tests if position is compared to position properly"""

        self.assertTrue(Position(1, 2) == Position(1, 2))

    def test_add_position_to_tuple(self) -> None:
        """Tests if tuple is added to position properly"""

        result = Position(1, 2) + (2, 1)

        self.assertEqual(result, Position(3, 3))

    def test_add_position_to_position(self) -> None:
        """Tests if position is added to position properly"""

        result = Position(1, 2) + Position(1, 1)

        self.assertEqual(result, Position(2, 3))

    def test_sub_position_and_tuple(self) -> None:
        """Tests if tuple is subtracted properly from position"""

        result = Position(4, 4) - (1, 2)

        self.assertEqual(result, Position(3, 2))

    def test_sub_position_and_position(self) -> None:
        """Tests if position is subtracted properly from position"""

        result = Position(4, 4) - Position(2, 3)

        self.assertEqual(result, Position(2, 1))
