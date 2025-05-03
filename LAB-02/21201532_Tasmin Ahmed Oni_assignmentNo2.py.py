from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLUT.fonts import GLUT_BITMAP_HELVETICA_18
import random
import time
import math


W_WIDTH, W_HEIGHT = 500, 700  
diamond_x = 0  
diamond_y = 350  
catcher_x = 0  
score = 0  
diamond_speed = 100  
freeze = False  
gameover = False  
last_frame_time = 0  
diamond_color = [1, 0, 0]  


def convert_coordinate(x, y):
    
    a = x - (W_WIDTH / 2)
    b = (W_HEIGHT / 2) - y
    return a, b

def midpoint_line(x1, y1, x2, y2):
    
    dx = x2 - x1
    dy = y2 - y1
    zone = 0
    if abs(dx) > abs(dy):
        if dx >= 0 and dy >= 0:
            zone = 0
        elif dx < 0 and dy >= 0:
            zone = 3
        elif dx < 0 and dy < 0:
            zone = 4
        elif dx >= 0 and dy < 0:
            zone = 7
    else:
        if dx >= 0 and dy >= 0:
            zone = 1
        elif dx < 0 and dy >= 0:
            zone = 2
        elif dx < 0 and dy < 0:
            zone = 5
        elif dx >= 0 and dy < 0:
            zone = 6

    def convert_to_zone0(x, y, zone):
        zone_map = {
            0: (x, y),
            1: (y, x),
            2: (y, -x),
            3: (-x, y),
            4: (-x, -y),
            5: (-y, -x),
            6: (-y, x),
            7: (x, -y)
        }
        return zone_map[zone]

    def convert_from_zone0(x, y, zone):
        zone_map = {
            0: (x, y),
            1: (y, x),
            2: (-y, x),
            3: (-x, y),
            4: (-x, -y),
            5: (-y, -x),
            6: (y, -x),
            7: (x, -y)
        }
        return zone_map[zone]

    x1, y1 = convert_to_zone0(x1, y1, zone)
    x2, y2 = convert_to_zone0(x2, y2, zone)
    dx = x2 - x1
    dy = y2 - y1
    d = 2 * dy - dx
    incrE = 2 * dy
    incrNE = 2 * (dy - dx)
    x, y = x1, y1
    x0, y0 = convert_from_zone0(x, y, zone)
    glVertex2f(x0, y0)
    while x < x2:
        if d <= 0:
            d += incrE
            x += 1
        else:
            d += incrNE
            x += 1
            y += 1
        x0, y0 = convert_from_zone0(x, y, zone)
        glVertex2f(x0, y0)

def draw_diamond_shape():
    
    global diamond_color
    glColor3f(diamond_color[0], diamond_color[1], diamond_color[2])
    glBegin(GL_POINTS)
    midpoint_line(diamond_x, diamond_y + 15, diamond_x + 10, diamond_y)
    midpoint_line(diamond_x + 10, diamond_y, diamond_x, diamond_y - 15)
    midpoint_line(diamond_x, diamond_y - 15, diamond_x - 10, diamond_y)
    midpoint_line(diamond_x - 10, diamond_y, diamond_x, diamond_y + 15)
    glEnd()

def draw_catcher():
    
    global gameover
    if not gameover:
        glColor3f(0.529, 0.808, 0.922)  
    else:
        glColor3f(1, 0, 0) 
    glBegin(GL_POINTS)
    midpoint_line(catcher_x - 50, -300, catcher_x + 50, -300)  # Bottom
    midpoint_line(catcher_x + 50, -300, catcher_x + 70, -280)  # Right 
    midpoint_line(catcher_x + 70, -280, catcher_x - 70, -280)  # Top
    midpoint_line(catcher_x - 70, -280, catcher_x - 50, -300)  # Left 
    glEnd()

def draw_visual():
    
    global freeze
    
    
    glColor3f(0, 0.8, 1)
    glBegin(GL_POINTS)
    midpoint_line(-208, 300, -160, 300)
    midpoint_line(-210, 300, -190, 320)
    midpoint_line(-210, 300, -190, 280)
    glEnd()

    
    glColor3f(1, 0.5, 0)
    glBegin(GL_POINTS)
    if freeze:
        midpoint_line(-15, 320, -15, 280)
        midpoint_line(-15, 320, 15, 300)
        midpoint_line(-15, 280, 15, 300)
    else:
        midpoint_line(-10, 320, -10, 280)
        midpoint_line(10, 320, 10, 280)
    glEnd()

    
    glColor3f(0.9, 0, 0)
    glBegin(GL_POINTS)
    midpoint_line(210, 315, 180, 285)
    midpoint_line(210, 285, 180, 315)
    glEnd()

    
    glColor3f(1, 1, 1)
    glRasterPos2f(-240, -340)
    for ch in f"Score: {score}":
        glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ord(ch))

    
    if gameover:
        glColor3f(1, 0, 0)
        glRasterPos2f(-150, 0)
        for ch in "Game Over! Better Luck Next Time :)":
            glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ord(ch))

def restart_game():
    
    global diamond_x, diamond_y, catcher_x, score, diamond_speed, freeze, gameover, diamond_color
    diamond_x = random.randint(-220, 220)
    diamond_y = 350
    catcher_x = 0
    score = 0
    diamond_speed = 100
    freeze = False
    gameover = False
    diamond_color = [random.random(), random.random(), random.random()]
    print("Starting Over")

def keyboardcontrolar(key, x, y):
    
    global catcher_x
    catcher_half_width = 70  

    
    key = key.decode('utf-8') if isinstance(key, bytes) else key

    if not freeze and not gameover:
        if (key =='a' or key=='A') and catcher_x > -250 + catcher_half_width:
            catcher_x -= 20
        elif (key =='d' or key=='D') and catcher_x < 250 - catcher_half_width:
            catcher_x += 20
    glutPostRedisplay()

def mousecontrolar(button, state, x, y):
    
    global freeze, gameover, score
    if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
        c_x, c_y = convert_coordinate(x, y)
        
        
        if -209 < c_x < -170 and 275 < c_y < 325:
            restart_game()
        
       
        elif -25 < c_x < 25 and 275 < c_y < 325:
            freeze = not freeze
        
        
        elif 170 < c_x < 216 and 280 < c_y < 320:
            print(f'Goodbye! Score: {score}')
            glutLeaveMainLoop()
    glutPostRedisplay()

def animate():
    
    global diamond_y, diamond_x, score, gameover, diamond_speed, diamond_color, last_frame_time
    
    current_time = time.time()
    delta_time = current_time - last_frame_time
    last_frame_time = current_time

    if not freeze and not gameover:
        diamond_y -= diamond_speed * delta_time
        
        if (catcher_x - 70 <= diamond_x <= catcher_x + 70) and diamond_y <= -280:
            score += 1
            print(f"Diamond Caught! Score: {score}")
            diamond_y = 350
            diamond_x = random.randint(-220, 220)
            diamond_color = [random.random(), random.random(), random.random()]
            diamond_speed *= 1.2
        
        if diamond_y < -350:
            gameover = True
            print(f"Game Over! Final Score: {score}")
    
    glutPostRedisplay()

def display():
    
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glClearColor(0, 0, 0, 0)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    
    draw_visual()
    draw_diamond_shape()
    draw_catcher()
    
    glutSwapBuffers()

def init():
    
    global last_frame_time
    glClearColor(0, 0, 0, 0)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(-250, 250, -350, 350, -1, 1)
    last_frame_time = time.time()

# Main game initialization ; Driver code
glutInit()
glutInitWindowSize(W_WIDTH, W_HEIGHT)
glutInitWindowPosition(0, 0)
glutInitDisplayMode(GLUT_DEPTH | GLUT_DOUBLE | GLUT_RGB)
wind = glutCreateWindow(b"Catch the Diamonds!")
init()

diamond_x = random.randint(-220, 220)

glutDisplayFunc(display)
glutIdleFunc(animate)
glutKeyboardFunc(keyboardcontrolar)
glutMouseFunc(mousecontrolar)
glutMainLoop()