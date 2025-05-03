from OpenGL.GL import *
from OpenGL.GLUT import *
import random
import math

# Screen dimensions
WIDTH, HEIGHT = 800, 600

class Particle:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.size = random.uniform(4, 10)
        self.alpha = random.uniform(0.3, 1.0)
        self.speed_x = random.uniform(-2.0, 2.0)
        self.speed_y = random.uniform(-2.0, 2.0)
        self.color = (random.uniform(0.4, 0.7), random.uniform(0.6, 0.9), 1.0)  # Blue aura

    def update(self):
        self.x += self.speed_x
        self.y += self.speed_y
        self.alpha -= 0.008
        self.size *= 0.96

particles = []

def create_particles(x, y, num_particles):
    for _ in range(num_particles):
        particles.append(Particle(x, y))

def draw_particles():
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE)
    
    for particle in particles[:]:
        glColor4f(particle.color[0], particle.color[1], particle.color[2], particle.alpha)
        glPointSize(particle.size)
        
        glBegin(GL_POINTS)
        glVertex2f(particle.x, particle.y)
        glEnd()
        
        particle.update()
        if particle.alpha <= 0:
            particles.remove(particle)

def draw_goku():
    # Muscular torso with shading
    # Main torso
    glBegin(GL_QUADS)
    glColor3f(0.9, 0.8, 0.7)  # Skin tone (lighter center)
    glVertex2f(360, 150)  # Extended lower to show more of the body
    glVertex2f(440, 150)
    glColor3f(0.8, 0.7, 0.6)  # Slightly darker for shading
    glVertex2f(440, 300)
    glVertex2f(360, 300)
    glEnd()

    # Chest definition
    glBegin(GL_QUADS)
    glColor3f(0.95, 0.85, 0.75)  # Highlight
    glVertex2f(370, 280)
    glVertex2f(430, 280)
    glColor3f(0.85, 0.75, 0.65)  # Shadow
    glVertex2f(430, 300)
    glVertex2f(370, 300)
    glEnd()

    # Abs definition (multiple sections for more detail)
    glBegin(GL_QUADS)
    # Upper abs
    glColor3f(0.95, 0.85, 0.75)
    glVertex2f(380, 240)
    glVertex2f(420, 240)
    glColor3f(0.85, 0.75, 0.65)
    glVertex2f(420, 260)
    glVertex2f(380, 260)
    # Middle abs
    glColor3f(0.95, 0.85, 0.75)
    glVertex2f(380, 220)
    glVertex2f(420, 220)
    glColor3f(0.85, 0.75, 0.65)
    glVertex2f(420, 240)
    glVertex2f(380, 240)
    # Lower abs
    glColor3f(0.95, 0.85, 0.75)
    glVertex2f(380, 200)
    glVertex2f(420, 200)
    glColor3f(0.85, 0.75, 0.65)
    glVertex2f(420, 220)
    glVertex2f(380, 220)
    glEnd()

    # Shoulders and arms with shading
    glBegin(GL_QUADS)
    # Left shoulder
    glColor3f(0.9, 0.8, 0.7)
    glVertex2f(340, 280)
    glVertex2f(360, 280)
    glColor3f(0.8, 0.7, 0.6)
    glVertex2f(360, 320)
    glVertex2f(340, 320)
    # Right shoulder
    glColor3f(0.9, 0.8, 0.7)
    glVertex2f(440, 280)
    glVertex2f(460, 280)
    glColor3f(0.8, 0.7, 0.6)
    glVertex2f(460, 320)
    glVertex2f(440, 320)
    # Left arm
    glColor3f(0.9, 0.8, 0.7)
    glVertex2f(340, 200)
    glVertex2f(360, 200)
    glColor3f(0.8, 0.7, 0.6)
    glVertex2f(360, 280)
    glVertex2f(340, 280)
    # Right arm
    glColor3f(0.9, 0.8, 0.7)
    glVertex2f(440, 200)
    glVertex2f(460, 200)
    glColor3f(0.8, 0.7, 0.6)
    glVertex2f(460, 280)
    glVertex2f(440, 280)
    glEnd()

    # Head
    glBegin(GL_TRIANGLE_FAN)
    glColor3f(0.9, 0.8, 0.7)  # Skin tone
    center_x, center_y = 400, 340
    radius = 30
    for i in range(20):
        angle = 2 * math.pi * i / 20
        x = center_x + radius * math.cos(angle)
        y = center_y + radius * math.sin(angle)
        glVertex2f(x, y)
    glEnd()

    # Facial features
    # Left eye (white part)
    glColor3f(1.0, 1.0, 1.0)
    glBegin(GL_QUADS)
    glVertex2f(390, 340)
    glVertex2f(400, 340)
    glVertex2f(400, 350)
    glVertex2f(390, 350)
    glEnd()
    # Right eye (white part)
    glBegin(GL_QUADS)
    glVertex2f(400, 340)
    glVertex2f(410, 340)
    glVertex2f(410, 350)
    glVertex2f(400, 350)
    glEnd()
    # Left pupil
    glColor3f(0.0, 0.0, 0.0)
    glBegin(GL_QUADS)
    glVertex2f(394, 342)
    glVertex2f(398, 342)
    glVertex2f(398, 346)
    glVertex2f(394, 346)
    glEnd()
    # Right pupil
    glBegin(GL_QUADS)
    glVertex2f(402, 342)
    glVertex2f(406, 342)
    glVertex2f(406, 346)
    glVertex2f(402, 346)
    glEnd()
    # Eyebrows (simplified as lines)
    glColor3f(0.0, 0.0, 0.0)
    glLineWidth(2.0)
    glBegin(GL_LINES)
    glVertex2f(388, 355)
    glVertex2f(400, 355)
    glVertex2f(400, 355)
    glVertex2f(412, 355)
    glEnd()

    # Ultra Instinct silver hair with gradient
    glBegin(GL_TRIANGLES)
    # Main hair spikes
    glColor3f(0.9, 0.9, 0.95)  # Lighter silver at tips
    glVertex2f(400, 400)  # Center top
    glColor3f(0.7, 0.7, 0.8)  # Darker at base
    glVertex2f(380, 340)
    glVertex2f(420, 340)
    
    glColor3f(0.9, 0.9, 0.95)
    glVertex2f(400, 420)  # Upper spike
    glColor3f(0.7, 0.7, 0.8)
    glVertex2f(390, 360)
    glVertex2f(410, 360)
    
    glColor3f(0.9, 0.9, 0.95)
    glVertex2f(380, 400)  # Left spike
    glColor3f(0.7, 0.7, 0.8)
    glVertex2f(360, 340)
    glVertex2f(390, 350)
    
    glColor3f(0.9, 0.9, 0.95)
    glVertex2f(420, 400)  # Right spike
    glColor3f(0.7, 0.7, 0.8)
    glVertex2f(410, 350)
    glVertex2f(440, 340)
    
    glColor3f(0.9, 0.9, 0.95)
    glVertex2f(370, 380)  # Additional left spike
    glColor3f(0.7, 0.7, 0.8)
    glVertex2f(350, 330)
    glVertex2f(380, 340)
    
    glColor3f(0.9, 0.9, 0.95)
    glVertex2f(430, 380)  # Additional right spike
    glColor3f(0.7, 0.7, 0.8)
    glVertex2f(420, 340)
    glVertex2f(450, 330)
    glEnd()

    # Outlines for body (to mimic line art style)
    glColor3f(0.0, 0.0, 0.0)
    glLineWidth(2.0)
    glBegin(GL_LINE_LOOP)
    # Torso outline
    glVertex2f(360, 150)
    glVertex2f(440, 150)
    glVertex2f(440, 300)
    glVertex2f(360, 300)
    glEnd()
    # Left arm outline
    glBegin(GL_LINE_LOOP)
    glVertex2f(340, 200)
    glVertex2f(360, 200)
    glVertex2f(360, 280)
    glVertex2f(340, 280)
    glEnd()
    # Right arm outline
    glBegin(GL_LINE_LOOP)
    glVertex2f(440, 200)
    glVertex2f(460, 200)
    glVertex2f(460, 280)
    glVertex2f(440, 280)
    glEnd()

    # Layered aura effect
    # Inner aura (more opaque)
    glColor4f(0.5, 0.7, 1.0, 0.6)
    glBegin(GL_TRIANGLE_FAN)
    for i in range(50):
        angle = 2 * math.pi * i / 50
        x = 400 + 100 * math.cos(angle) * random.uniform(0.7, 1.0)
        y = 250 + 120 * math.sin(angle) * random.uniform(0.7, 1.0)
        glVertex2f(x, y)
    glEnd()

    # Outer aura (less opaque, more flame-like)
    glColor4f(0.4, 0.6, 1.0, 0.3)
    glBegin(GL_LINE_LOOP)
    for i in range(70):
        angle = 2 * math.pi * i / 70
        x = 400 + 150 * math.cos(angle) * random.uniform(0.8, 1.3)
        y = 250 + 180 * math.sin(angle) * random.uniform(0.8, 1.3)
        glVertex2f(x, y)
    glEnd()

def display():
    glClear(GL_COLOR_BUFFER_BIT)
    
    # Dark background with blue gradient
    glBegin(GL_QUADS)
    glColor3f(0.0, 0.0, 0.1)  # Dark blue at bottom
    glVertex2f(0, 0)
    glVertex2f(WIDTH, 0)
    glColor3f(0.1, 0.2, 0.5)  # Lighter blue at top
    glVertex2f(WIDTH, HEIGHT)
    glVertex2f(0, HEIGHT)
    glEnd()
    
    # More intense particle spawning for aura
    if random.random() < 0.8:
        create_particles(400 + random.uniform(-100, 100), 
                        250 + random.uniform(-100, 100), 
                        10)
    
    draw_goku()
    draw_particles()
    
    glutSwapBuffers()

def reshape(width, height):
    glViewport(0, 0, width, height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0, WIDTH, 0, HEIGHT, -1, 1)
    glMatrixMode(GL_MODELVIEW)  # Fixed typo: GL_MODEVIEW -> GL_MODELVIEW
    glLoadIdentity()

def idle():
    glutPostRedisplay()

def main():
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB)
    glutInitWindowSize(WIDTH, HEIGHT)
    glutCreateWindow(b"Goku Ultra Instinct")
    
    glClearColor(0.0, 0.0, 0.0, 1.0)
    glEnable(GL_POINT_SMOOTH)
    glEnable(GL_LINE_SMOOTH)
    
    glutDisplayFunc(display)
    glutReshapeFunc(reshape)
    glutIdleFunc(idle)
    
    glutMainLoop()

if __name__ == "__main__":
    main()