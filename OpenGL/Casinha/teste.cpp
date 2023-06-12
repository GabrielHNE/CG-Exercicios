
//
//  main.cpp
//  opengl_aula1
//
//  Created by Gilberto Fernandes Junior on 27/03/23.
//



#include <windows.h>
#include <GL/glut.h>
#include <stdlib.h>
#include <math.h>
#include <stdio.h>

void myInit(void);
void myDisplay(void);
void keyboard(unsigned char key, int x, int y);

int main(int argc, char** argv){
    glutInit(&argc, argv); // Inicializa o GLUT e processa qualquer par�metro passado pela linha de comandos. Deve ser chamada antes de qualquer outra rotina GLUT.
    glutInitDisplayMode (GLUT_SINGLE | GLUT_RGB); // Especifica como o v�deo ser� utilizado, no caso ser� alocado um buffer e o sistema de cor ser� RGB.
    glutInitWindowSize (640, 480); // Especifica as dimens�es da janela em pixels.
    glutInitWindowPosition (100, 100); // Especifica a coordenada superior esquerda da janela. Define a localiza��o da janela dentro da tela
    glutCreateWindow ("Primeiro programa"); // Cria a janela e devolve um identificador �nico para a janela. At� que o comando glutMainLoop seja chamado, a janela n�o ser� mostrada.
    myInit(); // Rotina que implementa as configura��es iniciais do programa.
    glutDisplayFunc(myDisplay); // Chamada para a fun��o de desenho
        // Toda vez que o GLUT determinar que a janela tem de ser desenhada, ele chamar� a fun��o aqui determinada.
    glutKeyboardFunc(keyboard); // Determinam as fun��es que usaremos para ler o teclado e o mouse respectivamente.
    glutMainLoop( ); // � o �ltimo comando que chamamos. Ele faz com que todas as janelas criadas sejam mostradas. Uma vez que entramos neste loop, s� sa�mos quando o programa se encerra.
    return 0;

}

void myInit(void){

    glClearColor(1.0,1.0,1.0,0.0);     // cor de fundo branco
    glColor3f(0.0f, 0.0f, 0.0f);          // Define cor corrente de desenho
    glPointSize(4.0);             // Define o tamanho do ponto: 4 por 4 pixels
    glMatrixMode(GL_PROJECTION);
    glLoadIdentity();
                                           // janela com resolu��o de 640 por 480
    gluOrtho2D(0.0, 640.0, 0.0, 480.0);
}



void myDisplay(void)
{
        glClear(GL_COLOR_BUFFER_BIT); // limpa a janela
        glBegin(GL_POINTS);
            glVertex2f(100, 50); // desenha 3 pontos
            glVertex2f(100, 130);
            glVertex2i(150, 130);
        glEnd();
        glFlush(); // Garante a execu��o de todas as rotinas de desenho
}


// A rotina a seguir termina o programa com a tecla Esc
void keyboard(unsigned char key, int x, int y){
     switch (key) {
         case 27:
         exit(0);
         break;
     }
}
