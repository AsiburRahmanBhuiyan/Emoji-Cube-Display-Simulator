from OpenGL.GL import *
from OpenGL.GLUT import *
from subprocess import call


#################### Midpoint Line ####################
def points(x, y):
    glPointSize(5)
    glBegin(GL_POINTS)
    glVertex2f(x, y)
    glEnd()


def find_zone(x1, y1, x2, y2):
    dx = x2 - x1
    dy = y2 - y1
    if abs(dx) >= abs(dy):
        if dx >= 0 and dy >= 0:
            return 0
        elif dx < 0 < dy:
            return 3
        elif dx < 0 and dy < 0:
            return 4
        elif dx > 0 > dy:
            return 7
    elif abs(dx) <= abs(dy):
        if dx >= 0 and dy >= 0:
            return 1
        elif dx < 0 < dy:
            return 2
        elif dx < 0 and dy < 0:
            return 5
        elif dx > 0 > dy:
            return 6


def convert_to_zone0(x1, y1, x2, y2, zone):
    if zone == 0:
        return x1, y1, x2, y2
    elif zone == 1:
        return y1, x1, y2, x2
    elif zone == 2:
        return -y1, x1, -y2, x2
    elif zone == 3:
        return -x1, y1, -x2, y2
    elif zone == 4:
        return -x1, -y1, -x2, -y2
    elif zone == 5:
        return -y1, -x1, -y2, -x2
    elif zone == 6:
        return y1, -x1, y2, -x2
    elif zone == 7:
        return x1, -y1, x2, -y2


def original_zone(x, y, zone):
    if zone == 0:
        return x, y
    elif zone == 1:
        return y, x
    elif zone == 2:
        return -y, x
    elif zone == 3:
        return -x, y
    elif zone == 4:
        return -x, -y
    elif zone == 5:
        return -y, -x
    elif zone == 6:
        return y, -x
    elif zone == 7:
        return x, -y


def mid_point_line(x1, y1, x2, y2):
    zone = find_zone(x1, y1, x2, y2)
    x1, y1, x2, y2 = convert_to_zone0(x1, y1, x2, y2, zone)
    dx = x2 - x1
    dy = y2 - y1
    d = (2 * dy) - dx
    NE = (2 * dy) - (2 * dx)
    E = 2 * dy
    x = x1
    y = y1
    while x <= x2:
        original_x, original_y = original_zone(x, y, zone)
        points(original_x, original_y)
        if d > 0:
            d = d + NE
            x = x + 1
            y = y + 1
        else:
            d = d + E
            x = x + 1


#################### Midpoint Circle ####################
def mid_point_circle(radius):
    x = 0
    y = radius
    d = 1 - radius
    pixels = []
    while x < y:
        pixels.append((x, y))
        x += 1
        if d >= 0:
            d += (2 * x) - (2 * y) + 5
            y -= 1
        else:
            d += (2 * x) + 3
    return pixels


def convert_to_zone_zero(x, y, zone):
    global newX, newY
    if zone == 0:
        newX = x
        newY = y
    elif zone == 1:
        newX = y
        newY = x
    elif zone == 2:
        newX = y
        newY = -x
    elif zone == 3:
        newX = -x
        newY = y
    elif zone == 4:
        newX = -x
        newY = -y
    elif zone == 5:
        newX = -y
        newY = -x
    elif zone == 6:
        newX = -y
        newY = x
    elif zone == 7:
        newX = x
        newY = -y
    return newX, newY


def zoneZeroToOriginal(x, y, zone):
    global Xorg, Yorg
    if zone == 0:
        Xorg = x
        Yorg = y
    elif zone == 1:
        Xorg = y
        Yorg = x
    elif zone == 2:
        Xorg = -y
        Yorg = x
    elif zone == 3:
        Xorg = -x
        Yorg = y
    elif zone == 4:
        Xorg = -x
        Yorg = -y
    elif zone == 5:
        Xorg = -y
        Yorg = -x
    elif zone == 6:
        Xorg = y
        Yorg = -x
    elif zone == 7:
        Xorg = x
        Yorg = -y
    return Xorg, Yorg


def draw_circle(x, y, radius):
    glPointSize(5)
    glBegin(GL_POINTS)
    zone_0 = []
    zone_1 = mid_point_circle(radius)
    zone_2 = []
    zone_3 = []
    zone_4 = []
    zone_5 = []
    zone_6 = []
    zone_7 = []
    for (i, j) in zone_1:
        zone_0.append(convert_to_zone_zero(i, j, 1))
    for (i, j) in zone_0:
        zone_2.append(zoneZeroToOriginal(i, j, 2))
        zone_3.append(zoneZeroToOriginal(i, j, 3))
        zone_4.append(zoneZeroToOriginal(i, j, 4))
        zone_5.append(zoneZeroToOriginal(i, j, 5))
        zone_6.append(zoneZeroToOriginal(i, j, 6))
        zone_7.append(zoneZeroToOriginal(i, j, 7))
    for (i, j) in zone_0:
        glVertex2f(x + i, y + j)
    for (i, j) in zone_1:
        glVertex2f(x + i, y + j)
    for (i, j) in zone_2:
        glVertex2f(x + i, y + j)
    for (i, j) in zone_3:
        glVertex2f(x + i, y + j)
    for (i, j) in zone_4:
        glVertex2f(x + i, y + j)
    for (i, j) in zone_5:
        glVertex2f(x + i, y + j)
    for (i, j) in zone_6:
        glVertex2f(x + i, y + j)
    for (i, j) in zone_7:
        glVertex2f(x + i, y + j)
    glEnd()


def iterate():
    glViewport(0, 0, 500, 500)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0, 500, 0, 500, 0, 1)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()


#################### Screen Print ####################
def showScreen():
    glClear(GL_COLOR_BUFFER_BIT)
    glLoadIdentity()
    iterate()
    glColor3f(1, 1, 1)
    if emoji == 1:
        # happy
        draw_circle(250, 250, 200)  # (x,y,r)
        mid_point_line(275, 300, 375, 350)
        mid_point_line(275, 300, 400, 250)
        mid_point_line(225, 300, 125, 350)
        mid_point_line(225, 300, 100, 250)
        mid_point_line(125, 200, 250, 150)
        mid_point_line(375, 200, 250, 150)
    elif emoji == 2:
        # sad
        draw_circle(250, 250, 200)  # (x,y,r)
        mid_point_line(275, 300, 400, 250)
        mid_point_line(225, 300, 100, 250)
        mid_point_line(150, 150, 250, 185)
        mid_point_line(350, 150, 250, 185)
    elif emoji == 3:
        # angry
        draw_circle(250, 250, 200)  # (x,y,r)
        glPointSize(30)
        glBegin(GL_POINTS)
        glVertex2f(300, 300)
        glVertex2f(200, 300)
        glEnd()
        mid_point_line(150, 350, 200, 320)
        mid_point_line(350, 350, 300, 320)
        mid_point_line(150, 150, 250, 185)
        mid_point_line(350, 150, 250, 185)
    elif emoji == 4:
        # senti
        draw_circle(250, 250, 200)  # (x,y,r)
        glPointSize(35)
        glBegin(GL_POINTS)
        glVertex2f(300, 300)
        glVertex2f(200, 300)
        glEnd()
        mid_point_line(125, 200, 250, 150)
        mid_point_line(375, 200, 250, 150)
    elif emoji == 5:
        # neutral
        draw_circle(250, 250, 200)  # (x,y,r)
        glPointSize(35)
        glBegin(GL_POINTS)
        glVertex2f(300, 300)
        glVertex2f(200, 300)
        glEnd()
        mid_point_line(150, 175, 350, 175)
    elif emoji == 6:
        # tongue
        draw_circle(250, 250, 200)  # (x,y,r)
        mid_point_line(275, 300, 375, 350)
        mid_point_line(275, 300, 400, 250)
        mid_point_line(225, 300, 125, 350)
        mid_point_line(225, 300, 100, 250)
        mid_point_line(125, 200, 375, 200)
        mid_point_line(200, 125, 200, 200)
        mid_point_line(300, 125, 300, 200)
        mid_point_line(200, 125, 250, 100)
        mid_point_line(300, 125, 250, 100)
        mid_point_line(250, 150, 250, 200)
    elif emoji == 7:
        # annoyance
        draw_circle(250, 250, 200)  # (x,y,r)
        mid_point_line(275, 300, 375, 350)
        mid_point_line(275, 300, 400, 250)
        mid_point_line(225, 300, 125, 350)
        mid_point_line(225, 300, 100, 250)
        mid_point_line(125, 150, 150, 175)
        mid_point_line(150, 175, 200, 140)
        mid_point_line(200, 140, 250, 175)
        mid_point_line(250, 175, 300, 140)
        mid_point_line(300, 140, 350, 175)
        mid_point_line(350, 175, 375, 150)
    elif emoji == 8:
        call(['python', 'cube.py'])
    elif emoji == 9:
        call(['python', 'rotating cube.py'])
    else:
        num = int(repr(emoji)[-1])
        glColor3f(69, 69, 69)
        if num == 0:
            mid_point_line(100, 350, 210, 350)  # a
            mid_point_line(100, 150, 210, 150)  # b
            mid_point_line(210, 150, 210, 350)  # r
            mid_point_line(100, 150, 100, 350)  # l
        elif num == 1:
            mid_point_line(210, 150, 210, 350)
        elif num == 2:
            mid_point_line(100, 350, 200, 350)  # a
            mid_point_line(100, 150, 200, 150)  # b
            mid_point_line(200, 250, 200, 350)  # r
            mid_point_line(100, 150, 100, 250)  # l
            mid_point_line(100, 250, 200, 250)  # m
        elif num == 3:
            mid_point_line(100, 350, 200, 350)  # a
            mid_point_line(100, 150, 200, 150)  # b
            mid_point_line(200, 150, 200, 350)  # r
            mid_point_line(100, 250, 200, 250)  # m
        elif num == 4:
            mid_point_line(200, 150, 200, 350)  # r
            mid_point_line(100, 250, 100, 350)  # l
            mid_point_line(100, 250, 200, 250)  # m

        elif num == 5:
            mid_point_line(100, 350, 200, 350)  # a
            mid_point_line(100, 150, 200, 150)  # b
            mid_point_line(200, 150, 200, 250)  # r
            mid_point_line(100, 250, 100, 350)  # l
            mid_point_line(100, 250, 200, 250)  # m
        elif num == 6:
            mid_point_line(100, 350, 200, 350)  # a
            mid_point_line(100, 150, 200, 150)  # b
            mid_point_line(200, 150, 200, 250)  # r
            mid_point_line(100, 150, 100, 350)  # l
            mid_point_line(100, 250, 200, 250)  # m
        elif num == 7:
            mid_point_line(100, 350, 210, 350)  # a
            mid_point_line(210, 150, 210, 350)  # r
        elif num == 8:
            mid_point_line(100, 350, 210, 350)  # a
            mid_point_line(100, 150, 210, 150)  # b
            mid_point_line(210, 150, 210, 350)  # r
            mid_point_line(100, 150, 100, 350)  # l
            mid_point_line(100, 250, 210, 250)  # m
        else:
            mid_point_line(100, 350, 200, 350)  # a
            mid_point_line(100, 150, 200, 150)  # b
            mid_point_line(200, 150, 200, 350)  # r
            mid_point_line(100, 250, 100, 350)  # l
            mid_point_line(100, 250, 200, 250)  # m
        print('Please enter a number within the above available options.')
    glutSwapBuffers()


print('1. Happy', '2. Sad', '3. Angry', '4. Senti', '5. Neutral', '6. Tongue', '7. Annoyance', '8. Cube', '9. Rotating cube', sep='\n')
emoji = int(input('PLease enter a number to see the desired output from the above available options: '))
glutInit()
glutInitDisplayMode(GLUT_RGBA)
glutInitWindowSize(500, 500)
glutInitWindowPosition(0, 0)
wind = glutCreateWindow("Project")
glutDisplayFunc(showScreen)
glutMainLoop()
