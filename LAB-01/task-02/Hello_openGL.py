from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import sys
import random
import math
import time

WIDTH, HEIGHT = 400, 400
POINT_RADIUS = 0.02
MIN_SPEED = 0.5
MAX_SPEED = 3.0
DEFAULT_SPEED = 0.5
SPEED_CHANGE = 0.5
BLINK_DURATION = 0.2

BLACK = (0.0, 0.0, 0.0)
WHITE = (1.0, 1.0, 1.0)
RED = (1.0, 0.0, 0.0)
GREEN = (0.0, 1.0, 0.0)
BLUE = (0.0, 0.0, 1.0)
YELLOW = (1.0, 1.0, 0.0)
CYAN = (0.0, 1.0, 1.0)
MAGENTA = (1.0, 0.0, 1.0)
ORANGE = (1.0, 0.65, 0.0)
PURPLE = (0.5, 0.0, 0.5)

COLORS = [RED, GREEN, BLUE, YELLOW, CYAN, MAGENTA, ORANGE, PURPLE, WHITE]

points = []
is_frozen = False
last_time = 0
mouse_x, mouse_y = 0, 0
current_speed = DEFAULT_SPEED
blink_start_time = 0
is_blinking = False

def create_point(x, y):
    color = random.choice(COLORS)
    opengl_x = (x / WIDTH) * 2 - 1
    opengl_y = -((y / HEIGHT) * 2 - 1)
    angle = random.choice([40, 130, 200, 300])
    angle_rad = math.radians(angle)
    dx = math.cos(angle_rad) * current_speed
    dy = math.sin(angle_rad) * current_speed
    return {
        'x': opengl_x,
        'y': opengl_y,
        'color': color,
        'dx': dx,
        'dy': dy,
        'prev_dx': dx,
        'prev_dy': dy,
        'prev_speed': current_speed
    }

def draw_point(point):
    global is_blinking, blink_start_time
    current_time = time.time()
    
    if is_blinking and current_time - blink_start_time < BLINK_DURATION:
        glColor3f(*BLACK)
    else:
        if is_blinking and current_time - blink_start_time >= BLINK_DURATION:
            is_blinking = False
        glColor3f(*point['color'])
    
    glBegin(GL_QUADS)
    glVertex2f(point['x'] - POINT_RADIUS, point['y'] - POINT_RADIUS)
    glVertex2f(point['x'] + POINT_RADIUS, point['y'] - POINT_RADIUS)
    glVertex2f(point['x'] + POINT_RADIUS, point['y'] + POINT_RADIUS)
    glVertex2f(point['x'] - POINT_RADIUS, point['y'] + POINT_RADIUS)
    glEnd()

def update_point(point, delta_time):
    if is_frozen:
        return point
    point['x'] += point['dx'] * delta_time
    point['y'] += point['dy'] * delta_time
    if point['x'] <= -1 + POINT_RADIUS or point['x'] >= 1 - POINT_RADIUS:
        point['dx'] = -point['dx']
    if point['y'] <= -1 + POINT_RADIUS or point['y'] >= 1 - POINT_RADIUS:
        point['dy'] = -point['dy']
    return point

def change_point_speed(point, increase=True):
    if is_frozen:
        return point
    magnitude = math.sqrt(point['dx']**2 + point['dy']**2)
    if increase and magnitude < MAX_SPEED:
        new_magnitude = min(magnitude + SPEED_CHANGE, MAX_SPEED)
    elif not increase and magnitude > MIN_SPEED:
        new_magnitude = max(magnitude - SPEED_CHANGE, MIN_SPEED)
    else:
        new_magnitude = magnitude
    if magnitude != 0:  
        point['dx'] = point['dx'] / magnitude * new_magnitude
        point['dy'] = point['dy'] / magnitude * new_magnitude
    return point

def display():
    global points, last_time
    current_time = time.time()
    delta_time = current_time - last_time
    last_time = current_time
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    points = [update_point(point, delta_time) for point in points]
    for point in points:
        draw_point(point)
    glutSwapBuffers()
    glutPostRedisplay()

def reorder(width, height):
    global WIDTH, HEIGHT
    WIDTH, HEIGHT = width, height
    glViewport(0, 0, width, height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluOrtho2D(-1, 1, -1, 1)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

def keyboard(key, x, y):
    global is_frozen, points
    key = key.decode('utf-8') if isinstance(key, bytes) else key
    if key == ' ':
        is_frozen = not is_frozen

def adjust_angle(key, x, y):
    global points, current_speed
    if is_frozen:
        return
    if key == GLUT_KEY_UP:
        for point in points:
            change_point_speed(point, True)
        current_speed = min(current_speed + SPEED_CHANGE, MAX_SPEED)
    elif key == GLUT_KEY_DOWN:
        for point in points:
            change_point_speed(point, False)
        current_speed = max(current_speed - SPEED_CHANGE, MIN_SPEED)

def mouse(button, state, x, y):
    global points, mouse_x, mouse_y, is_blinking, blink_start_time
    if is_frozen:
        return
        
    opengl_x = (x / WIDTH) * 2 - 1
    opengl_y = -((y / HEIGHT) * 2 - 1)
    mouse_x, mouse_y = opengl_x, opengl_y
    
    if state == GLUT_DOWN:
        if button == GLUT_RIGHT_BUTTON:
            points.append(create_point(x, y))
        elif button == GLUT_LEFT_BUTTON:
            is_blinking = True
            blink_start_time = time.time()

glutInit(sys.argv)
glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB)
glutInitWindowSize(WIDTH, HEIGHT)
glutCreateWindow(b"Ball Game")
glutDisplayFunc(display)
glutReshapeFunc(reorder)
glutKeyboardFunc(keyboard)
glutSpecialFunc(adjust_angle)
glutMouseFunc(mouse)
glClearColor(*BLACK, 1.0)
last_time = time.time()
glutMainLoop()