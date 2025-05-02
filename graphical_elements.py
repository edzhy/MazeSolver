from tkinter import Tk, BOTH, Canvas
import time
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
        time.sleep(0.001)
    
    def wait_for_close(self):
        self.__win_running = True
        while self.__win_running:
            self.redraw()
            
        print('window closed')

    def close(self):
        self.__win_running = False

    def draw_line(self, line, fill_color):
        line.draw(self.canva, fill_color)

    def draw_cell(self, cell, fill_color):
       cell.draw(fill_color)

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
    
    def draw(self, fill_color):
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
        if self.has_top_wall:
            self._win.draw_line(tw,fill_color)
        if self.has_right_wall:
            self._win.draw_line(rw,fill_color)
        if self.has_bottom_wall:
            self._win.draw_line(bw,fill_color)
        if self.has_left_wall:
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
        
class Maze():
    def __init__(self, x1, y1, num_rows, num_cols, cell_size_x, cell_size_y, win=None):
        self.x1 = x1
        self.y1 = y1
        self.num_rows = num_rows
        self.num_cols = num_cols
        self.cell_size_x = cell_size_x
        self.cell_size_y = cell_size_y
        self.win = win
        self._cells = []
        self._create_cells()
        self._draw_cells()

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