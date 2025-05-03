from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import math
import random
import time


camera_pos = (0, 500, 500)
camera_angle = 0
camera_height = 500
camera_mode = 0

GRID_LENGTH = 600
paused = False 
fovY = 120
player_pos = [0, 0, 0]
player_angle = 0
life = 5
score = 0
missed_bullets = 0
game_over = False
cheat_mode = False
cheat_vision = False
rand_var = 423

bullets = []
enemies = []
last_shot_time = 0
animation_time = 0


class Bullet:
    def __init__(self, pos, angle):
        self.pos = list(pos)
        self.angle = angle
        self.speed = 10


class Enemy:
    def __init__(self):
        self.pos = self.generate_random_position()
        self.speed = 0.5
        self.scale = 1.0

    # Generates random position for enemy spawn
    def generate_random_position(self):
        edge = random.choice(['top', 'bottom', 'left', 'right'])
        if edge == 'top':
            return [random.uniform(-GRID_LENGTH, GRID_LENGTH), GRID_LENGTH, 0]
        elif edge == 'bottom':
            return [random.uniform(-GRID_LENGTH, GRID_LENGTH), -GRID_LENGTH, 0]
        elif edge == 'left':
            return [-GRID_LENGTH, random.uniform(-GRID_LENGTH, GRID_LENGTH), 0]
        else:
            return [GRID_LENGTH, random.uniform(-GRID_LENGTH, GRID_LENGTH), 0]


def render_text(x, y, text, font=GLUT_BITMAP_HELVETICA_18):
    glColor3f(1, 1, 1)
    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    gluOrtho2D(0, 1000, 0, 800)
    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()
    glRasterPos2f(x, y)
    for ch in text:
        glutBitmapCharacter(font, ord(ch))
    glPopMatrix()
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    glMatrixMode(GL_MODELVIEW)


def render_player():
    glPushMatrix()
    glTranslatef(player_pos[0], player_pos[1], player_pos[2])
    
    if camera_mode != 2 and camera_mode != 3 and camera_mode != 4:
        glRotatef(player_angle, 0, 0, 1)
    else:
        if camera_mode == 2:
            glRotatef(0, 0, 0, 1)
        elif camera_mode == 4:
            glRotatef(180, 0, 0, 1)
    
    glScalef(1.5, 1.5, 1.5)
    
    if game_over:
        glRotatef(player_angle, 0, 1, 0)
    else:
        glRotatef(90, 1, 0, 0)
    
    # Render head
    glPushMatrix()
    glTranslatef(0, 60, 0)
    glColor3f(0.5, 0.5, 0.5)
    gluSphere(gluNewQuadric(), 20, 10, 10)
    glPopMatrix()
    
    # Render body
    glPushMatrix()
    glTranslatef(0, 30, 0)
    glScalef(30, 40, 20)
    glColor3f(0, 0.5, 0)
    glutSolidCube(1)
    glPopMatrix()
    
    # Render right arm
    glPushMatrix()
    glTranslatef(15, 40, 0)
    glRotatef(90, 0, 1, 0)
    glColor3f(0.2, 0.2, 0.2)
    gluCylinder(gluNewQuadric(), 4, 4, 20, 10, 10)
    glPopMatrix()
    
    # Render left leg
    glPushMatrix()
    glTranslatef(-10, 10, 0)
    glRotatef(90, 1, 0, 0)
    glColor3f(0, 0, 0.5)
    gluCylinder(gluNewQuadric(), 8, 8, 20, 10, 10)
    glPopMatrix()
    
    # Render right leg
    glPushMatrix()
    glTranslatef(10, 10, 0)
    glRotatef(90, 1, 0, 0)
    gluCylinder(gluNewQuadric(), 8, 8, 20, 10, 10)
    glPopMatrix()
    
    # Render right 
    glPushMatrix()
    glTranslatef(15, 40, -20)
    glRotatef(90, 0, 1, 0)
    glScalef(10, 10, 20)
    glColor3f(1, 0.8, 0.6)
    glutSolidSphere(0.5, 20, 20)
    glPopMatrix()

    # Render left 
    glPushMatrix()
    glTranslatef(15, 40, 20)
    glRotatef(90, 0, 1, 0)
    glScalef(10, 10, 20)
    glColor3f(1, 0.8, 0.6)
    glutSolidSphere(0.5, 20, 20)
    glPopMatrix()
        
    glPopMatrix()


def render_enemy(enemy):
    glPushMatrix()
    glTranslatef(enemy.pos[0], enemy.pos[1], enemy.pos[2])
    glScalef(enemy.scale, enemy.scale, enemy.scale)
    
    # Render main body
    glColor3f(1, 0, 0)
    glTranslatef(0, 0, 20)
    gluSphere(gluNewQuadric(), 20, 10, 10)
    
    # Render head
    glColor3f(0, 0, 0)
    glTranslatef(0, 0, 30)
    gluSphere(gluNewQuadric(), 15, 10, 10)
    
    glPopMatrix()

# Renders a bullet as a cube
def render_bullet(bullet):
    glPushMatrix()
    glTranslatef(bullet.pos[0], bullet.pos[1], bullet.pos[2])
    glColor3f(0.8, 0.8, 0)
    glutSolidCube(10)
    glPopMatrix()


def render_grid():
    glBegin(GL_QUADS)
    step = GRID_LENGTH / 10
    for i in range(-10, 10):
        for j in range(-10, 10):
            x1 = i * step
            x2 = (i + 1) * step
            y1 = j * step
            y2 = (j + 1) * step
            glColor3f(0.8, 0.8, 0.8) if (i + j) % 2 == 0 else glColor3f(0.5, 0.0, 0.5)
            glVertex3f(x1, y1, 0)
            glVertex3f(x2, y1, 0)
            glVertex3f(x2, y2, 0)
            glVertex3f(x1, y2, 0)
    glEnd()
    
    # Render boundary walls
    glBegin(GL_QUADS)
    glColor3f(0.0, 0.0, 1.0)
    glVertex3f(-GRID_LENGTH, GRID_LENGTH, 0)
    glVertex3f(GRID_LENGTH, GRID_LENGTH, 0)
    glVertex3f(GRID_LENGTH, GRID_LENGTH, 100)
    glVertex3f(-GRID_LENGTH, GRID_LENGTH, 100)
    
    glColor3f(0.0, 1.0, 0.0)
    glVertex3f(-GRID_LENGTH, -GRID_LENGTH, 0)
    glVertex3f(GRID_LENGTH, -GRID_LENGTH, 0)
    glVertex3f(GRID_LENGTH, -GRID_LENGTH, 100)
    glVertex3f(-GRID_LENGTH, -GRID_LENGTH, 100)
    
    glColor3f(0.5, 0.8, 1.0)
    glVertex3f(-GRID_LENGTH, -GRID_LENGTH, 0)
    glVertex3f(-GRID_LENGTH, GRID_LENGTH, 0)
    glVertex3f(-GRID_LENGTH, GRID_LENGTH, 100)
    glVertex3f(-GRID_LENGTH, -GRID_LENGTH, 100)
    
    glColor3f(1.0, 1.0, 1.0)
    glVertex3f(GRID_LENGTH, -GRID_LENGTH, 0)
    glVertex3f(GRID_LENGTH, GRID_LENGTH, 0)
    glVertex3f(GRID_LENGTH, GRID_LENGTH, 100)
    glVertex3f(GRID_LENGTH, -GRID_LENGTH, 100)
    glEnd()


def handle_keyboard_input(key, x, y):
    global player_pos, player_angle, cheat_mode, cheat_vision, life, score, missed_bullets, game_over, paused
    PLAYER_SIZE = 50  

    if game_over:
        if key == b'r':
            # Reset game state
            player_pos = [0, 0, 0]
            player_angle = 0
            life = 5
            score = 0
            missed_bullets = 0
            game_over = False
            bullets.clear()
            enemies.clear()
            for _ in range(5):
                enemies.append(Enemy())
        return
    
    if key == b'p':
        paused = not paused
    
    if not paused:
        if key == b'w':
            # Move player forward
            rad = math.radians(player_angle)
            new_x = player_pos[0] + 10 * math.cos(rad)
            new_y = player_pos[1] + 10 * math.sin(rad)
            
            if -GRID_LENGTH + PLAYER_SIZE < new_x < GRID_LENGTH - PLAYER_SIZE and -GRID_LENGTH + PLAYER_SIZE < new_y < GRID_LENGTH - PLAYER_SIZE:
                player_pos[0] = new_x
                player_pos[1] = new_y
        
        if key == b's':
            # Move player backward
            rad = math.radians(player_angle)
            new_x = player_pos[0] - 10 * math.cos(rad)
            new_y = player_pos[1] - 10 * math.sin(rad)
            
            if -GRID_LENGTH + PLAYER_SIZE < new_x < GRID_LENGTH - PLAYER_SIZE and -GRID_LENGTH + PLAYER_SIZE < new_y < GRID_LENGTH - PLAYER_SIZE:
                player_pos[0] = new_x
                player_pos[1] = new_y
        
        if key == b'a':
            # Rotate player left
            player_angle += 10
        
        if key == b'd':
            # Rotate player right
            player_angle -= 10
        
        if key == b'c':
            # Toggle cheat mode
            cheat_mode = not cheat_mode
        
        if key == b'v':
            # Toggle cheat vision 
            if cheat_mode:
                cheat_vision = not cheat_vision

def handle_special_keys(key, x, y):
    global camera_height, camera_angle
    if key == GLUT_KEY_UP:
        
        camera_height += 10
    if key == GLUT_KEY_DOWN:
        
        camera_height = max(100, camera_height - 10)
    if key == GLUT_KEY_LEFT:
       
        camera_angle += 5
    if key == GLUT_KEY_RIGHT:
        
        camera_angle -= 5


def process_mouse_input(button, state, x, y):
    global camera_mode, last_shot_time
    if game_over:
        return
    
    current_time = time.time()
    if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN and (current_time - last_shot_time) > 0.5:
        # Fire bullet
        rad = math.radians(player_angle)
        bullet_pos = [
            player_pos[0] + 50 * math.cos(rad),
            player_pos[1] + 50 * math.sin(rad),
            50
        ]
        bullets.append(Bullet(bullet_pos, player_angle))
        last_shot_time = current_time
        print("Player Bullet Fired!")  
    
    if button == GLUT_RIGHT_BUTTON and state == GLUT_DOWN:
        
        if camera_mode == 1:
            camera_mode = 0
        else:
            camera_mode = 1
            camera_angle = 0
            camera_height = 50

# Configures the camera position
def configure_camera():
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(fovY, 1.25, 0.1, 1500)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    
    if cheat_vision and cheat_mode:
        # Cheat vision camera (behind player)
        rad = math.radians(player_angle)
        eye_x = player_pos[0] - 100 * math.cos(rad)
        eye_y = player_pos[1] - 100 * math.sin(rad)
        eye_z = 180
        target_x = player_pos[0] + 100 * math.cos(rad)
        target_y = player_pos[1] + 100 * math.sin(rad)
        target_z = player_pos[2]
        gluLookAt(eye_x, eye_y, eye_z, target_x, target_y, target_z, 0, 0, 1)
    
    elif camera_mode == 1:
        # First-person camera
        rad = math.radians(player_angle)
        eye_x = player_pos[0] - 0 * math.cos(rad)
        eye_y = player_pos[1] - 0 * math.sin(rad)
        eye_z = 150
        target_x = player_pos[0] + 40 * math.cos(rad)
        target_y = player_pos[1] + 40 * math.sin(rad)
        target_z = 50
        gluLookAt(eye_x, eye_y, eye_z, target_x, target_y, target_z, 0, 0, 1)
    
    else:
        # Third-person camera
        rad = math.radians(camera_angle)
        eye_x = camera_height * math.cos(rad)
        eye_y = camera_height * math.sin(rad)
        gluLookAt(eye_x, eye_y, camera_height, 0, 0, 0, 0, 0, 1)


def update_game_state():
    global missed_bullets, life, score, game_over, animation_time, player_angle, last_shot_time
    if game_over:
        return
    
    # Update bullet positions
    for bullet in bullets[:]:
        rad = math.radians(bullet.angle)
        bullet.pos[0] += bullet.speed * math.cos(rad)
        bullet.pos[1] += bullet.speed * math.sin(rad)
        if abs(bullet.pos[0]) > GRID_LENGTH or abs(bullet.pos[1]) > GRID_LENGTH:
            bullets.remove(bullet)
            missed_bullets += 1
            print(f"Bullet Missed: {missed_bullets}") 
    
    # Update animation time for enemy scaling
    animation_time += 0.05
    for enemy in enemies[:]:
        # Move enemy towards player
        dx = player_pos[0] - enemy.pos[0]
        dy = player_pos[1] - enemy.pos[1]
        dist = math.sqrt(dx**2 + dy**2)
        if dist > 0:
            enemy.pos[0] += (dx / dist) * enemy.speed
            enemy.pos[1] += (dy / dist) * enemy.speed
        enemy.scale = 1.0 + 0.2 * math.sin(animation_time)
    
    #bullet-enemy collisions
    for bullet in bullets[:]:
        for enemy in enemies[:]:
            dist = math.sqrt((bullet.pos[0] - enemy.pos[0])**2 + (bullet.pos[1] - enemy.pos[1])**2)
            if dist < 40 * enemy.scale:
                if bullet in bullets:
                    bullets.remove(bullet)
                if enemy in enemies:
                    enemies.remove(enemy)
                    enemies.append(Enemy())
                    score += 1
                    print(f"Score: {score}")
                break
    
    #player-enemy collisions
    for enemy in enemies[:]:
        dist = math.sqrt((player_pos[0] - enemy.pos[0])**2 + (player_pos[1] - enemy.pos[1])**2)
        if dist < 50:
            life -= 1
            print(f"Life: {life}")
            if enemy in enemies:
                enemies.remove(enemy)
                enemies.append(Enemy())
    
    #game over conditions
    if life <= 0 or missed_bullets >= 10:
        game_over = True
        print("Game Over!")
        print(f"Final Score: {score}")
    
    #cheat mode auto-aim and shooting
    if cheat_mode:
        player_angle += 2
        current_time = time.time()
        if (current_time - last_shot_time) > 1:
            for enemy in enemies:
                dx = enemy.pos[0] - player_pos[0]
                dy = enemy.pos[1] - player_pos[1]
                angle_to_enemy = math.degrees(math.atan2(dy, dx))
                rad = math.radians(angle_to_enemy)
                bullet_pos = [
                    player_pos[0] + 50 * math.cos(rad),
                    player_pos[1] + 50 * math.sin(rad),
                    50
                ]
                bullets.append(Bullet(bullet_pos, angle_to_enemy))
            last_shot_time = current_time

#pause
def manage_idle_state():
    if not paused:
        update_game_state()
    glutPostRedisplay()

#special key inputs for camera control
def process_special_input(key, x, y):
    global camera_pos, camera_angle, camera_height
    if key == GLUT_KEY_UP:
        
        camera_height += 10
    elif key == GLUT_KEY_DOWN:
        
        camera_height = max(100, camera_height - 10)
    elif key == GLUT_KEY_LEFT:
        
        camera_angle += 5
    elif key == GLUT_KEY_RIGHT:
        
        camera_angle -= 5

# Renders the entire game scene
def display_game():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    glViewport(0, 0, 1000, 800)
    
    configure_camera()
    
    render_grid()
    render_player()
    for enemy in enemies:
        render_enemy(enemy)
    for bullet in bullets:
        render_bullet(bullet)
    
    # Render HUD text
    render_text(10, 770, f"Score: {score}")
    render_text(10, 740, f"Life: {life}")
    render_text(10, 710, f"Missed Bullets: {missed_bullets}")
    
    camera_mode_names = ["Third Person", "First Person", "Side View", "Top View", "Front View"]
    
    if game_over:
        render_text(400, 700, "Game Over! Press R to Restart")
    if cheat_mode:
        render_text(10, 680, "Cheat Mode: ON")
    if cheat_vision:
        render_text(10, 650, "Cheat Vision: ON")
    if paused:
        render_text(400, 700, "Paused! Press P to Resume")
    
    glutSwapBuffers()

# game status to console
def log_game_status():
    camera_mode_names = ["First Person"]
    print(f"Score: {score}")
    print(f"Life: {life}")
    print(f"Missed Bullets: {missed_bullets}")
    print(f"Camera Mode: {camera_mode_names[camera_mode]}")
    if game_over:
        print("Game Over! Press R to Restart")
    if cheat_mode:
        print("Cheat Mode: ON")
    if cheat_vision:
        print("Cheat Vision: ON")
    if paused:
        print("Paused! Press P to Resume")

# Initializing the game 
def initialize_game():
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
    glutInitWindowSize(1000, 800)
    glutInitWindowPosition(0, 0)
    glutCreateWindow(b"Bullet Frenzy")
    
    for _ in range(5):
        enemies.append(Enemy())
    
    glEnable(GL_DEPTH_TEST)
    glutDisplayFunc(display_game)
    glutKeyboardFunc(handle_keyboard_input)
    glutSpecialFunc(process_special_input)
    glutMouseFunc(process_mouse_input)
    glutIdleFunc(manage_idle_state)
    glutMainLoop()

if __name__ == "__main__":
    initialize_game()