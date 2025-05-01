from graphical_elements import *

def main():
    win = Window(920, 920)

    #drawing some lines:
    #point1, point2 = Point(700,600), Point(600,500)
    #point3, point4 = Point(400,300), Point(500,400)
    #line1, line2 = Line(point1, point2), Line(point3, point4)
    #win.draw_line(line1, "red")
    #win.draw_line(line2, "black")
    #cell1 = Cell(500,500,400,400,win,lw=False)
    #win.draw_cell(cell1, "red")
    #cell2 = Cell(490,490,410,410,win,rw=False)
    #win.draw_cell(cell2, "black")
    #cell3 = Cell(100,500,200,400,win)
    #win.draw_cell(cell3, "red")
    #cell4 = Cell(400,100,300,200,win)
    #win.draw_cell(cell4, "black")
    #win.draw_cell_move(cell1, cell3)
    #win.draw_cell_move(cell4, cell3, True)
    maze = Maze(10,10,30,30,30,30,win)
    win.wait_for_close()

main()