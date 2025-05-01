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
    

