from tkinter import Tk, BOTH, Canvas
import time
import random
class Window():
    def __init__(self, width, height):
        self.__root = Tk()
        self.__root.title("Maze Solver 3000")
        self.__root.protocol("WM_DELETE_WINDOW", self.close)
        self.__win_running = False
        self.canva = Canvas(self.__root,bg="white", height=height, width=width)
        self.canva.pack(fill=BOTH, expand=1)

    def redraw(self):
        self.__root.update_idletasks()
        self.__root.update()
        time.sleep(0.025)
    
    def wait_for_close(self):
        self.__win_running = True
        while self.__win_running:
            self.redraw()
            
        print('window closed')

    def close(self):
        self.__win_running = False

    def draw_line(self, line, fill_color):
        line.draw(self.canva, fill_color)

    def draw_cell(self, cell, fill_color, breaking_w=False):
       cell.draw(fill_color,breaking_w)

    def draw_cell_move(self, current_cell, to_cell, undo=False):
        current_cell.draw_move(to_cell, undo)
    
class Point():
    def __init__(self,x=0,y=0):
        self.x=x
        self.y=y
    
class Line():
    def __init__(self,point1, point2):
        self.l_start = point1
        self.l_end = point2

    def draw(self, canvas, fill_color):
        #fill_color will be a string, ex.: "red"
        canvas.create_line(self.l_start.x,self.l_start.y,self.l_end.x,self.l_end.y, fill=fill_color, width=2)

class Cell():
    def __init__(self, x1, y1, x2, y2, win=None, lw=True, rw=True, tw=True, bw=True):
        self.has_left_wall = lw
        self.has_right_wall = rw
        self.has_top_wall = tw
        self.has_bottom_wall = bw
        #top-left corner coordinates
        self._x1 = x1
        self._y1 = y1
        #bottom-right corner coordinates
        self._x2 = x2
        self._y2 = y2
        self._win = win
        self._visited = False
    
    def draw(self, fill_color, breaking_w=False):
        p1, p2 = Point(self._x1, self._y1), Point(self._x2, self._y2)
        #opposite corner creation math
        #top-right p3 corner will have x as x2, y as y1,
        #bottom-left p4 corner x as x1, y as y2
        p3, p4 = Point(self._x2, self._y1), Point(self._x1, self._y2)
        #
        #   p1              p3
        #
        #       cell center
        #
        #   p4              p2
        #
        #topwall rightwall bottomwall leftwall creation
        tw, rw, bw, lw = Line(p1,p3),Line(p3,p2),Line(p2,p4),Line(p1,p4)
        if not breaking_w:
            if self.has_top_wall:
                self._win.draw_line(tw,fill_color)
            if self.has_right_wall:
                self._win.draw_line(rw,fill_color)
            if self.has_bottom_wall:
                self._win.draw_line(bw,fill_color)
            if self.has_left_wall:
                self._win.draw_line(lw,fill_color)
        else:
            if not self.has_top_wall:
                self._win.draw_line(tw,fill_color)
            if not self.has_right_wall:
                self._win.draw_line(rw,fill_color)
            if not self.has_bottom_wall:
                self._win.draw_line(bw,fill_color)
            if not self.has_left_wall:
                self._win.draw_line(lw,fill_color)
        

    def draw_move(self, to_cell, undo=False):
        #cell center math
        cc_x = (self._x1 + self._x2)/2
        cc_y = (self._y1 + self._y2)/2
        cc = Point(cc_x, cc_y)

        to_cc_x = (to_cell._x1 + to_cell._x2)/2
        to_cc_y = (to_cell._y1 + to_cell._y2)/2
        to_cc = Point(to_cc_x, to_cc_y)

        line = Line(cc, to_cc)
        if not undo:
            self._win.draw_line(line,"red")
        else:
            self._win.draw_line(line,"grey")
    
    def _break_wall(self, direction, chosen_cell):
        #self
        p1, p2 = Point(self._x1, self._y1), Point(self._x2, self._y2)
        p3, p4 = Point(self._x2, self._y1), Point(self._x1, self._y2)
        tw, rw, bw, lw = Line(p1,p3),Line(p3,p2),Line(p2,p4),Line(p1,p4)
        #chosen cell
        #ccp1, ccp2 = Point(chosen_cell._x1, chosen_cell._y1), Point(chosen_cell._x2, chosen_cell._y2)
        #ccp3, ccp4 = Point(chosen_cell._x2, chosen_cell._y1), Point(chosen_cell._x1, chosen_cell._y2)
        #cctw, ccrw, ccbw, cclw = Line(ccp1,ccp3),Line(ccp3,ccp2),Line(ccp2,ccp4),Line(ccp1,ccp4)
        match direction:
            case "top":
                self.has_top_wall = False
                chosen_cell.has_bottom_wall = False
            case "bot":
                chosen_cell.has_top_wall = False
                self.has_bottom_wall = False
            case "lw":
                self.has_left_wall = False
                chosen_cell.has_right_wall = False
            case "rw":
                chosen_cell.has_left_wall = False
                self.has_right_wall = False
        if self._win is not None:
            if direction == "top":
                self._win.draw_line(tw,"white")
            elif direction == "bot":
                self._win.draw_line(bw,"white")
            elif direction == "rw":
                self._win.draw_line(rw,"white")
            elif direction == "lw":
                self._win.draw_line(lw,"white")
        else:
            return
        
class Maze():
    def __init__(self, x1, y1, num_rows, num_cols, cell_size_x, cell_size_y, win=None, seed=None):
        self.x1 = x1
        self.y1 = y1
        self.num_rows = num_rows
        self.num_cols = num_cols
        self.cell_size_x = cell_size_x
        self.cell_size_y = cell_size_y
        self.win = win
        self._cells = []
        #seed allows to reproduce the exact same maze layout
        if seed:
            random.seed(seed)
        self._create_cells()
        self._draw_cells()

        self._break_entrance_and_exit()
        self._break_walls_r(0,0)
        self._reset_cells_visited()

    def _create_cells(self):
        #self.num_cols determines how many Cells are needed in a list
        #self.num_rows determines how many lists of Cells are needed
        #need math for cell gen
        #x1, y1 will represent top-left corner of the maze, hence the first cell as well
        px1 = self.x1
        py1 = self.y1
        px2 = self.x1 + self.cell_size_x 
        py2 = self.x1 + self.cell_size_y
        for i in range(self.num_rows):
            self._cells.append([])
            for j in range(self.num_cols):
                self._cells[i].append(Cell(px1,py1,px2,py2,self.win))
                px1 += self.cell_size_x
                px2 += self.cell_size_x
            #check if this was the last row, if yes, don't need to update cell coordinates
            #if i+1 != self.num_rows:
                #after row is completed, need to reset x values for next row
            px1 = self.x1
            px2 = self.x1 + self.cell_size_x
            #need to adjust y values for next row
            py1 += self.cell_size_y
            py2 += self.cell_size_y
    

    def _draw_cells(self):
        if self.win is None:
            return
        for i in range(self.num_rows):
            for cell in self._cells[i]:
                self.win.draw_cell(cell, "black")
                self._animate()
                
    def _animate(self):
        self.win.redraw()

    def _break_entrance_and_exit(self, fill_color="white"):
        exit_index_col = self.num_cols - 1
        exit_index_row = self.num_rows - 1
        #need to break top left cells left wall-Line( Point(self._cells._x1, self._y1), Point(self._x1, self._y2) )
        #and bottom right cells right wall-Line( Point(self._x2, self._y1), Point(self._x2, self._y2) )
        entrance_cell = self._cells[0][0]
        exit_cell = self._cells[exit_index_row][exit_index_col]
        entrance_cell.has_left_wall = False
        if self.win is not None:
            self.win.draw_cell(entrance_cell, fill_color, True)
        exit_cell.has_right_wall = False
        if self.win is not None:
            self.win.draw_cell(exit_cell, fill_color, True)

    def _break_walls_r(self, i, j):
        current_cell = self._cells[i][j]
        current_cell._visited = True
        while True:
            to_visit = []
            #checking current cells adjacent cells for visitation status
            #checking to the left
            if j > 0:
                if not self._cells[i][j-1]._visited:
                    to_visit.append([i,j-1,'lw'])
            #checking to the right
            if j < self.num_cols - 1:
                if not self._cells[i][j+1]._visited:
                    to_visit.append([i,j+1,'rw'])
            #checking up
            if i > 0:
                if not self._cells[i-1][j]._visited:
                    to_visit.append([i-1,j,'top'])
            #checking down
            if i < self.num_rows - 1:
                if not self._cells[i+1][j]._visited:
                    to_visit.append([i+1,j,'bot'])
            if len(to_visit) == 0:
                #current_cell.draw("black")
                return
            else:
                random_direction = random.randrange(0,len(to_visit))
                #chosen cell location
                ccl = to_visit[random_direction]
                chosen_cell = self._cells[ccl[0]][ccl[1]]
                current_cell._break_wall(ccl[2],chosen_cell)
                if self.win is not None:
                    self._animate()
                self._break_walls_r(ccl[0],ccl[1])
                
    def _reset_cells_visited(self):
        for i in range(self.num_rows):
            for cell in self._cells[i]:
                cell._visited = False

    def solve(self):
        end_cell = self._cells[self.num_rows-1][self.num_cols-1]
        if self._solve_r(end_cell,i=0,j=0):
            return True
        return False
    
    def _solve_r(self, end_cell, i, j):
        current_cell = self._cells[i][j]
        self._animate()
        current_cell._visited = True
        if current_cell == end_cell:
            return True
        #checking to the left
        if j > 0:
            if not self._cells[i][j-1].has_right_wall:
                if not self._cells[i][j-1]._visited:
                    current_cell.draw_move(self._cells[i][j-1])
                    if self._solve_r(end_cell, i, j-1):
                        return True
                    else:
                        current_cell.draw_move(self._cells[i][j-1], True)
        #checking to the right
        if j < self.num_cols - 1:
            if not self._cells[i][j+1].has_left_wall:
                if not self._cells[i][j+1]._visited:
                    current_cell.draw_move(self._cells[i][j+1])
                    if self._solve_r(end_cell, i, j+1):
                        return True
                    else:
                        current_cell.draw_move(self._cells[i][j+1], True)
        #checking up
        if i > 0:
            if not self._cells[i-1][j].has_bottom_wall:
                if not self._cells[i-1][j]._visited:
                    current_cell.draw_move(self._cells[i-1][j])
                    if self._solve_r(end_cell, i-1, j):
                        return True
                    else:
                        current_cell.draw_move(self._cells[i-1][j], True)
        #checking down
        if i < self.num_rows - 1:
            if not self._cells[i+1][j].has_top_wall:
                if not self._cells[i+1][j]._visited:
                    current_cell.draw_move(self._cells[i+1][j])
                    if self._solve_r(end_cell, i+1, j):
                        return True
                    else:
                        current_cell.draw_move(self._cells[i+1][j], True)
        
        return False