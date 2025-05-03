#task-01:
#w or W= speed increase
#s or S= speed decrease
#d or D= right direction
#a or A= left direction
#q or Q= Original position of rain
#n or N= Changes day to night and viceversa
#f or F= Changes day to night gradually


from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import random
import math
import time


rain_drops = []
rain_angle = 0.0
rain_speed_factor = 1.0  
day_night_factor = 0.0  
auto_cycle = False
last_time = time.time()


def raindef():
    global rain_drops
    rain_drops = []
    for _ in range(300): 
        x = random.uniform(-100, 600)  
        y = random.uniform(0, 600)  
        speed = random.uniform(3.0, 3.0)
        length = random.uniform(20.0, 20.0)  
        rain_drops.append([x, y, speed, length])


def draw_triangle(x1, y1, x2, y2, x3, y3):
    glBegin(GL_TRIANGLES)
    glVertex2f(x1, y1)
    glVertex2f(x2, y2)
    glVertex2f(x3, y3)
    glEnd()


def draw_point(x, y):
    glBegin(GL_POINTS)
    glVertex2f(x, y)
    glEnd()


def draw_raindrop(x, y, length, angle):
    end_x = x + length * math.sin(math.atan(angle))
    end_y = y - length * math.cos(math.atan(angle))
    
    glBegin(GL_LINES)
    glVertex2f(x, y)
    glVertex2f(end_x, end_y)
    glEnd()

def draw_house():
    house_width = 200
    house_height = 150
    center_x = 250
    house_bottom = 120
    
    glColor3f(0.9, 0.9, 0.9)
    house_left = center_x - house_width/2
    house_right = center_x + house_width/2
    house_top = house_bottom + house_height
    
    draw_triangle(house_left, house_bottom, house_left, house_top, house_right, house_bottom)
    draw_triangle(house_left, house_top, house_right, house_top, house_right, house_bottom)
    
    glColor3f(0.6, 0.1, 0.8)
    roof_height = 80
    roof_top = house_top + roof_height
    
    draw_triangle(house_left, house_top, center_x, roof_top, house_right, house_top)
    
    glColor3f(0.2, 0.4, 0.8)
    window_width = 40
    window_height = 40
    left_window_left = house_left + 40
    window_bottom = house_bottom + 60
    
   
    draw_triangle(left_window_left, window_bottom, 
                  left_window_left, window_bottom + window_height, 
                  left_window_left + window_width, window_bottom)
    draw_triangle(left_window_left, window_bottom + window_height, 
                  left_window_left + window_width, window_bottom + window_height, 
                  left_window_left + window_width, window_bottom)
    
    
    glColor3f(0.0, 0.0, 0.0)
    glLineWidth(2.0)
    glBegin(GL_LINES)
    glVertex2f(left_window_left, window_bottom + window_height/2)
    glVertex2f(left_window_left + window_width, window_bottom + window_height/2)
    glVertex2f(left_window_left + window_width/2, window_bottom)
    glVertex2f(left_window_left + window_width/2, window_bottom + window_height)
    glEnd()
    
    
    glColor3f(0.2, 0.4, 0.8)
    right_window_left = house_right - 40 - window_width
    
    
    draw_triangle(right_window_left, window_bottom, 
                  right_window_left, window_bottom + window_height, 
                  right_window_left + window_width, window_bottom)
    draw_triangle(right_window_left, window_bottom + window_height, 
                  right_window_left + window_width, window_bottom + window_height, 
                  right_window_left + window_width, window_bottom)
    
    
    glColor3f(0.0, 0.0, 0.0)
    glBegin(GL_LINES)
    glVertex2f(right_window_left, window_bottom + window_height/2)
    glVertex2f(right_window_left + window_width, window_bottom + window_height/2)
    glVertex2f(right_window_left + window_width/2, window_bottom)
    glVertex2f(right_window_left + window_width/2, window_bottom + window_height)
    glEnd()
    
   
    glColor3f(0.2, 0.4, 0.8)
    door_width = 40
    door_height = 70
    door_left = center_x - door_width/2
    
    
    draw_triangle(door_left, house_bottom, 
                  door_left, house_bottom + door_height, 
                  door_left + door_width, house_bottom)
    draw_triangle(door_left, house_bottom + door_height, 
                  door_left + door_width, house_bottom + door_height, 
                  door_left + door_width, house_bottom)
    
    
    glColor3f(0.0, 0.0, 0.0)
    glPointSize(5)
    draw_point(door_left + door_width*0.8, house_bottom + door_height/2)


def draw_ground():
    
    glColor3f(0.6, 0.4, 0.2)
    ground_height = 20
    ground_bottom = 100
    
   
    draw_triangle(0, ground_bottom, 
                  0, ground_bottom + ground_height, 
                  500, ground_bottom)
    draw_triangle(0, ground_bottom + ground_height, 
                  500, ground_bottom + ground_height, 
                  500, ground_bottom)
    
    
    house_width = 200
    center_x = 250
    house_left = center_x - house_width/2
    house_right = center_x + house_width/2
    
    for i in range(20):
        x = i * 25
       
        if x > house_left - 25 and x < house_right + 25:
            continue
        
        
        glColor3f(0.1, 0.8, 0.2)
        tree_width = 30
        tree_height = 50
        
        draw_triangle(x - tree_width/2, ground_bottom + ground_height,
                      x, ground_bottom + ground_height + tree_height,
                      x + tree_width/2, ground_bottom + ground_height)


def draw_rain():
    global rain_drops, rain_angle
    
    
    blue_value = 1.0 - day_night_factor * 0.3
    glColor3f(0.2, 0.2, blue_value)
    
   
    glLineWidth(1.0)
    
    for drop in rain_drops:
        x, y, _, length = drop
        draw_raindrop(x, y, length, rain_angle)


def update_rain():
    global rain_drops, rain_speed_factor, rain_angle
    
    for i in range(len(rain_drops)):
        x, y, base_speed, length = rain_drops[i]
        
       
        speed = base_speed * rain_speed_factor
        dx = speed * rain_angle
        dy = speed
        
        
        y -= dy
        x += dx
        
        
        if y < 0:
            y = 600  
            x = random.uniform(-100, 600)  
        
        if x < -100:
            x = 600
        elif x > 600:
            x = -100
            
        rain_drops[i] = [x, y, base_speed, length]


def showScreen():
    global day_night_factor, auto_cycle, last_time
    
    
    current_time = time.time()
    if auto_cycle:
        time_diff = current_time - last_time
        day_night_factor = (math.sin(current_time * 0.2) + 1) / 2  
    
    
    bg_r = 0.53 * (1 - day_night_factor) + 0.05 * day_night_factor
    bg_g = 0.81 * (1 - day_night_factor) + 0.05 * day_night_factor
    bg_b = 0.92 * (1 - day_night_factor) + 0.2 * day_night_factor
    
    glClearColor(bg_r, bg_g, bg_b, 1.0)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    glViewport(0, 0, 500, 500)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0.0, 500, 0.0, 500, 0.0, 1.0)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    
    
    draw_ground()
    draw_house()
    
    
    update_rain()
    draw_rain()
    
    glutSwapBuffers()
    last_time = current_time


def adjust_the_angle(key, x, y):
    global rain_angle
    
    if key == GLUT_KEY_LEFT:
        rain_angle = max(rain_angle - 0.1, -1.0)
    elif key == GLUT_KEY_RIGHT:
        rain_angle = min(rain_angle + 0.1, 1.0)
    
    glutPostRedisplay()


def keyboard(key, x, y):
    global day_night_factor, auto_cycle, rain_speed_factor, rain_angle
    
    key = key.decode('utf-8') if isinstance(key, bytes) else key
    
    if key == 'f' or key == 'F':
        auto_cycle = not auto_cycle

    elif key == 'n' or key == 'N':
        if day_night_factor < 0.5:
            day_night_factor = 1.0
        else:
            day_night_factor = 0.0
        auto_cycle = False
    elif key == 'w' or key == 'W':
        
        rain_speed_factor = min(rain_speed_factor + 0.2, 3.0)
    elif key == 's' or key == 'S':
       
        rain_speed_factor = max(rain_speed_factor - 0.2, 0.2)
    elif key == 'a' or key == 'A':
       
        rain_angle = -0.8
    elif key == 'd' or key == 'D':
       
        rain_angle = 0.8

    elif key == 'q' or key == 'Q':

        if rain_angle == 0.0:
            rain_angle = 0.0
        
        elif rain_angle > 0.0:
            rain_angle -=0.8
    
        else:
            rain_angle +=0.8
    
    glutPostRedisplay()


def timer(value):
    glutPostRedisplay()
    glutTimerFunc(16, timer, 0)  


raindef()


glutInit()
glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE)
glutInitWindowSize(500, 500)
glutInitWindowPosition(0, 0)
wind = glutCreateWindow(b"Rainy Day")

glutDisplayFunc(showScreen)
glutSpecialFunc(adjust_the_angle)
glutKeyboardFunc(keyboard)
glutTimerFunc(0, timer, 0)


glutMainLoop()
