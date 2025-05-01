from tkinter import Tk, BOTH, Canvas

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
    
    def wait_for_close(self):
        self.__win_running = True
        while self.__win_running:
            self.redraw()
        print('window closed')

    def close(self):
        self.__win_running = False

    def draw_line(self, line, fill_color):
        line.draw(self.canva,fill_color)

    
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

