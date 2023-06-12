#include <GL/glut.h>  // Include the GLUT library

// Variaveis
float translateX = 0.0f, translateY = 0.0f, scale = 1.0f, rotateAngle = 0.0f;

// Handle keyboard
void keyboard(unsigned char key, int x, int y);
void specialkey(int key, int x, int y);

void myInit(void);
void display();

int main(int argc, char** argv) {
    glutInit(&argc, argv);
    glutInitDisplayMode(GLUT_SINGLE | GLUT_RGB);
    glutInitWindowSize(800, 600);
    glutCreateWindow("Atividade 3");

    glutDisplayFunc(display);
    glutKeyboardFunc(keyboard);
    glutSpecialFunc(specialkey);
    myInit();

    glutMainLoop();

    return 0;
}
void myInit(void){
    glClearColor(0.0f, 0.0f, 0.0f, 1.0f);
    gluOrtho2D(0.0f, 800.0f, 0.0f, 600.0f);
}
void display() {

    glClear(GL_COLOR_BUFFER_BIT);

    // Adiciona as transformações na matriz
    glPushMatrix();
    glTranslatef(translateX, translateY, 0.0f);
    glScalef(scale, scale, 1.0f);
    glRotatef(rotateAngle, 0.0f, 0.0f, 1.0f);

    glBegin(GL_QUADS);
    glColor3f(1.0f, 0.0f, 0.0f);
        glVertex2f(0.0f, 100.0f);
        glVertex2f(0.0f, 0.0f);
        glVertex2f(100.0f, 0.0f);
        glVertex2f(100.0f, 100.0f);
    glEnd();

    glPopMatrix();

    glFlush();
}


// Handle keyboard
void keyboard(unsigned char key, int x, int y) {
    switch (key) {
        case 'w':
        case 'W':
            scale += 1.0f;  // Increase the scale
            break;
        case 's':
        case 'S':
            scale -= 1.0f;  // Decrease the scale
            break;
        case 'a':
        case 'A':
            rotateAngle += 5.0f;  // Rotate counterclockwise
            break;
        case 'd':
        case 'D':
            rotateAngle -= 5.0f;  // Rotate clockwise
            break;
        case 27:
            exit(0);
        default:
            break;
    }
    glutPostRedisplay();  // Mark the window as needing to be redisplayed
}

void specialkey(int key, int x, int y) {
    switch (key) {
        case GLUT_KEY_UP:
            translateY += 1.0f;  // Translate up
            break;
        case GLUT_KEY_DOWN:
            translateY -= 1.0f;  // Translate down
            break;
        case GLUT_KEY_LEFT:
            translateX -= 1.0f;  // Translate left
            break;
        case GLUT_KEY_RIGHT:
            translateX += 1.0f;  // Translate right
            break;
        default:
            break;
    }
    glutPostRedisplay();  // Mark the window as needing to be redisplayed
}
