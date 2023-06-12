
#include <GL/glut.h>
#include <stdlib.h>

void myInit(void){
    glClearColor(1.0, 1.0, 1.0, 0.0); // cor de fundo
    glColor3f(0.0f, 0.0f, 0.0f); // cor de desenho

    glPointSize(4.0); // Define o tamanho do ponto

    glMatrixMode(GL_PROJECTION);
    glLoadIdentity(); // Janela com resolucao de 640 por 480
    gluOrtho2D(0.0, 640.0, 0.0, 480.0);
}

void myDisplay(void){
    glClear(GL_COLOR_BUFFER_BIT); // limpa a janela

    glBegin(GL_POINTS);
        glVertex2f(100, 50); // desenha 3 pontos
        glVertex2f(100, 130);
        glVertex2i(150, 130);
    glEnd();

    glFlush(); // Garante a execucao de todas as rotinas de desenho, sempre usar
}

int main(int argc, char *argv[])
{
    glutInit(&argc, argv);
    glutInitDisplayMode(GLUT_SINGLE | GLUT_RGB);
    glutInitWindowSize(640,480);
    glutInitWindowPosition(100,100);

    glutCreateWindow("Primeiro Programa");

    myInit();

    glutDisplayFunc(myDisplay);

    glutMainLoop();

    return EXIT_SUCCESS;
}
