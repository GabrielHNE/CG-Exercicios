#include <windows.h>
#include <GL/glut.h>
#include <stdlib.h>
#include <math.h>
#include <stdio.h>
#include <string.h>

#define PONTO 1
#define LINHA 2
#define POLIGONO 3

GLfloat win, r, g, b;
GLfloat mouseX, mouseY;
GLint primitiva, allow = 1;
GLfloat grossura = 3.0;
char text[100];

void myInit(void);
void display(void);
void keyboard(unsigned char key, int x, int y);

void drawInfos(char* string);

// Primitivas
void ponto();
void linha();
void poligono();
void quadrado();
void triangulo();

// Handle mouse events;
void handle_mouse(GLint button, GLint action, GLint x, GLint y);
void handle_passivemotion(GLint x, GLint y);
void handle_motion(GLint x, GLint y);
void handle_mouse_click_motion(GLint x, GLint y);

// Menus
void create_menu();
void handle_menu(GLint op);
void handle_espessura(GLint op);
void handle_cor(GLint op);



int main(int argc, char** argv){
    glutInit(&argc, argv);
    glutInitDisplayMode (GLUT_SINGLE | GLUT_RGB);
    glutInitWindowSize (640, 480);
    glutInitWindowPosition (100, 100);
    glutCreateWindow ("Primeiro programa");


    glutDisplayFunc(display);
    glutMouseFunc(handle_mouse);
    glutMotionFunc(handle_mouse_click_motion);
    glutKeyboardFunc(keyboard);
    myInit();
    glutMainLoop( );

    return 0;
}

void myInit(void){

    glClearColor(0.0,0.0,0.0,1.0);
    glClear(GL_COLOR_BUFFER_BIT);
    glColor3f(0.0f, 0.0f, 0.0f);
    glPointSize(grossura);
    glMatrixMode(GL_PROJECTION);
    glLoadIdentity();

    primitiva = PONTO;
    r = 0.0f;
    g = 0.0f;
    b = 1.0f;

    gluOrtho2D(0.0, 640.0, 480.0, 0.0);
}

void display(void)
{
    glMatrixMode(GL_MODELVIEW);
    glLoadIdentity();
//    glClear(GL_COLOR_BUFFER_BIT);

    // Define a cor corrente
    glColor3f(r,g,b);
    printf("Current: %d\n", primitiva);
    // Desenha uma primitiva

    if(allow){
        ponto();
    }else{
        allow=1;
    }

    glColor3f(1.0f,1.0f,1.0f);

    printf("Current text %s\n", text);
    drawInfos(text);

    glutSwapBuffers();
}

void drawInfos(char* string){
    glPushMatrix();
    glRasterPos2f(10.0,10.0);
    while(*string)
        glutBitmapCharacter(GLUT_BITMAP_TIMES_ROMAN_10,*string++);
    glPopMatrix();
}

// PRIMITIVAS
void ponto(void){
    glPointSize(grossura);
    glBegin(GL_POINTS);
        glVertex2f(mouseX, mouseY);
    glEnd();
}

void linha(void){
    glBegin(GL_POINT);
        glVertex2f(mouseX, mouseY);
    glEnd();
}

void poligono(void){
    glBegin(GL_POINT);
        glVertex2f(mouseX, mouseY);
    glEnd();
}

void quadrado(void)
{
    glBegin(GL_QUADS);
        glVertex2f(0.0f, 100.0f);
        glVertex2f(0.0f, 0.0f);
        glVertex2f(100.0f, 0.0f);
        glVertex2f(100.0f, 100.0f);
    glEnd();
}

void triangulo(void){
    glBegin(GL_TRIANGLES);
        glVertex2f(-25.0f, -25.0f);
        glVertex2f(0.0f, 25.0f);
        glVertex2f(25.0f, -25.0f);
    glEnd();
}
//***********************************************//

// Handle mouse events
void handle_mouse(GLint button, GLint action, GLint x, GLint y){

    if(button == GLUT_RIGHT_BUTTON && action == GLUT_DOWN){
        create_menu();
    }

    if(button == GLUT_LEFT_BUTTON && action == GLUT_DOWN){
        printf("Click: (%d, %d)\n", x, y);
        mouseX = (GLfloat) x;
        mouseY = (GLfloat) y;
    }

    glutPostRedisplay();
}

void handle_passivemotion(GLint x, GLint y){

}

void handle_motion(GLint x, GLint y){

}

void handle_mouse_click_motion(GLint x, GLint y){
    sprintf(text, "Botao pressionado (%d,%d)", x, y);
    mouseX = (GLfloat) x;
    mouseY = (GLfloat) y;
    glutPostRedisplay();
}

// A rotina a seguir termina o programa com a tecla Esc
void keyboard(unsigned char key, int x, int y){
    switch (key) {
        case 27:
            exit(0);
            break;
        // Letra d ou D => limpa tela
        case 68:
        case 100:
            glClear(GL_COLOR_BUFFER_BIT);
            glutPostRedisplay();
            allow = 0;
            break;

    }
}

// Menus
void create_menu(){
    GLint menu, submenu1, submenu2;

    submenu1 = glutCreateMenu(handle_espessura);
    glutAddMenuEntry("1px", 0);
    glutAddMenuEntry("3px", 1);
    glutAddMenuEntry("5px", 2);

    submenu2 = glutCreateMenu(handle_cor);
    glutAddMenuEntry("Vermelho", 0);
    glutAddMenuEntry("Verde", 1);
    glutAddMenuEntry("Azul", 2);

    menu = glutCreateMenu(handle_menu);
    glutAddSubMenu("Espessura", submenu1);
    glutAddSubMenu("Cor", submenu2);

    glutAttachMenu(GLUT_RIGHT_BUTTON);
}

void handle_menu(GLint op){
}

void handle_espessura(GLint op){
    switch(op) {
        case 0:
                 grossura = 1.0;
                 break;
        case 1:
                 grossura = 3.0;
                 break;
        case 2:
                 grossura = 5.0;
                 break;
    }

    allow = 0;
    glutPostRedisplay();
}

void handle_cor(GLint op){
    switch(op) {
        case 0:
             r = 1.0f;
             g = 0.0f;
             b = 0.0f;
             break;
        case 1:
             r = 0.0f;
             g = 1.0f;
             b = 0.0f;
             break;
        case 2:
             r = 0.0f;
             g = 0.0f;
             b = 1.0f;
             break;
    }

    allow = 0;
    glutPostRedisplay();
}
