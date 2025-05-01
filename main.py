from graphical_elements import *

def main():
    win = Window(800, 600)

    #drawing some lines:
    point1, point2 = Point(700,600), Point(600,500)
    point3, point4 = Point(400,300), Point(500,400)
    line1, line2 = Line(point1, point2), Line(point3, point4)
    win.draw_line(line1)
    win.draw_line(line2, "black")

    win.wait_for_close()

main()