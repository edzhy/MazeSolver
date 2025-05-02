import unittest
from graphical_elements import *

class Tests(unittest.TestCase):
    def test_maze_create_cells(self):
        num_rows = 12
        num_cols = 10
        m1 = Maze(0, 0, num_rows, num_cols, 10, 10)
        self.assertEqual(
            len(m1._cells),
            num_rows,
        )
        self.assertEqual(
            len(m1._cells[0]),
            num_cols,
        )

    def test_last_maze_cells_bottom_right_corner(self):
        num_rows, num_cols = 30, 30
        x_cell_size, y_cell_size = 25, 30
        maze = Maze(10,10,num_rows,num_cols,x_cell_size,y_cell_size)
        row_index, col_index = num_rows-1, num_cols-1
        x_expected_size = maze.x1 + x_cell_size * num_rows
        y_expected_size = maze.y1 + y_cell_size * num_cols
        #access the last cell in the maze
        self.assertEqual(maze._cells[row_index][col_index]._x2,
                         x_expected_size)
        self.assertEqual(maze._cells[row_index][col_index]._y2,
                         y_expected_size)

    def test_breaking_entrance_exit(self):
        num_rows, num_cols = 30, 30
        x_cell_size, y_cell_size = 25, 30
        maze = Maze(10,10,num_rows,num_cols,x_cell_size,y_cell_size)
        row_index, col_index = num_rows-1, num_cols-1
        maze._break_entrance_and_exit()
        self.assertEqual(maze._cells[0][0].has_left_wall,
                         False)
        self.assertEqual(maze._cells[row_index][col_index].has_right_wall,
                         False)

if __name__ == "__main__":
    unittest.main()