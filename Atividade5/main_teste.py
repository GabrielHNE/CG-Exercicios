import cv2
import numpy as np
import math
import matplotlib.pyplot as plt
from matplotlib import colors
from matplotlib.ticker import PercentFormatter

class Imagem:
    def __init__(self, path, mode = None):
        self.path = path 
        self.mode = mode

    def open(self):
        '''
            Abre a imagem e retorna um array do tipo NP.array
        '''
        try:
            if(self.mode != None):
                self.imgArr = cv2.imread(self.path, self.mode)
                return self.imgArr

            self.imgArr = cv2.imread(self.path)
            return self.imgArr
        except:
            print("Erro ao abrir arquivo de imagem.")
            return None
    
    def getChannelInGrey(self, channel):

        #check shape

        channels = [
            lambda : self.imgArr[:,:,2], #red
            lambda : self.imgArr[:,:,1], #green
            lambda : self.imgArr[:,:,0]  #blue
        ]

        if channel >= len(channels):
            return None
    
        return channels[channel]()

    def getChannelInRGB(self, channel):
        #check shape

        img = self.imgArr.copy()

        if channel == 'red':
            img[:, :, 0] = 0
            img[:, :, 1] = 0
        elif channel == 'green':
            img[:, :, 0] = 0
            img[:, :, 2] = 0
        elif channel == 'blue':
            img[:, :, 1] = 0
            img[:, :, 2] = 0

        return img

    def calculateEqHist(self, pixels):
        histogram = np.zeros(256, dtype=int)

        for i in range(pixels.shape[0]):
            for j in range(pixels.shape[1]):
                histogram[pixels[i,j]] = histogram[pixels[i,j]] + 1
        
        showHistogram(histogram)

        h_normalizado = np.zeros(256)
        
        n = pixels.shape[0] * pixels.shape[1] #n de pixels
        for i in range(256):
            h_normalizado[i] = histogram[i] / n
        
        acumulado = np.zeros(256)
        for i in range(256):
            if i == 0:
                acumulado[i] = h_normalizado[i]
            else:
                acumulado[i] = acumulado[i-1] + h_normalizado[i]

        for i in range(pixels.shape[0]):
            for j in range(pixels.shape[1]):
                pixels[i,j] = round(255 * acumulado[pixels[i,j]])

        cv2.imshow("imagem", pixels)
        cv2.waitKey(0)

        #Visualizar histograma equalizado
        histogram = np.zeros(256, dtype=int)
        for i in range(pixels.shape[0]):
            for j in range(pixels.shape[1]):
                histogram[pixels[i,j]] = histogram[pixels[i,j]] + 1

        showHistogram(histogram) 

def showHistogram(histogram):
    plt.bar(range(0,256), histogram)
    plt.show()

def nthOdd(number: int) -> int:
    cont = 0

    while( number > 1 ):
        number -= 2
        cont += 1 

    return cont

def convolucao(imagem, filtro) -> np.array:
    img_size = imagem.shape[0]
    newImg = np.zeros(shape=(img_size,img_size, imagem.shape[2]))

    n = filtro.shape[0]
    gap = nthOdd(n)

    # Loop through the image
    for i in range(gap, img_size - gap):
        for j in range(gap, img_size - gap):
            subMatB = imagem[i-gap: i+gap+1, j-gap:j+gap+1, 0]
            subMatG = imagem[i-gap: i+gap+1, j-gap:j+gap+1, 1]
            subMatR = imagem[i-gap: i+gap+1, j-gap:j+gap+1, 2]

            newImg[i,j, 0] = np.sum(np.multiply(subMatB, filtro))
            newImg[i,j, 1] = np.sum(np.multiply(subMatG, filtro))
            newImg[i,j, 2] = np.sum(np.multiply(subMatR, filtro))

    return newImg

def subplot_image(img: np.array, size = 3, channel = 0, i=0, j=0) -> np.array:
    return img[i: i+size, j:j+size, channel]

def alpha(x, a1, a2):
    return x == 0 if a1 else a2 

def cossenoDCT(x: int, i: int, N: int) -> np.float32:
    return math.cos( (((2.0*x) + 1)/(2*N)) )

def DCT(imagem):
    assert imagem.shape[0] == imagem.shape[1]

    N = imagem.shape[0]
    alfa1 = 1.0/math.sqrt(N)
    alfa2 = math.sqrt(2.0/N)

    saida = np.zeros((N,N), dtype=float)

    cosseno = np.zeros(shape=(N,N), dtype=np.float32)

    for i in range(N):
        for j in range(N):
            cosseno[i, j] = cossenoDCT(i, j, N)
            print(cosseno[i,j])

    exit()

    for i in range(0, N):
        for j in range(0, N):
            soma = 0
            
            for x in range(0, N):
                for y in range(0, N):
                    soma += imagem[x, y] * cosseno[x,i] * cosseno[y,j]
            print(soma)
            saida[i,j] = alpha(i, alfa1, alfa2) * alpha(j, alfa1, alfa2) * soma
    
    return saida

def DCT_inversa(imagem):
    assert imagem.shape[0] == imagem.shape[1]

    N = imagem.shape[0]
    alfa1 = 1.0/math.sqrt(N)
    alfa2 = math.sqrt(2.0/N)

    saida = np.zeros((N,N), dtype=float)
    
    cosseno = np.zeros(shape=(N,N), dtype=np.float32)

    for i in range(N):
        for j in range(N):
            cosseno[i, j] = cossenoDCT(i, j, N)

    for i in range(0, N):
        for j in range(0, N):
            soma = 0
            
            for x in range(0, N):
                alphai = alpha(x, alfa1, alfa2)

                for y in range(0, N):
                    soma += alphai * alpha(y, alfa1, alfa2) * imagem[x,y] * cosseno[i,x] * cosseno[j, y]

            saida[i,j] = soma
    
    return saida


def main():
    Im = Imagem("teste_2.png", mode=0)

    imagem = Im.open()

    print(imagem[0:10, 0:10])
    
    imgSaida = DCT(imagem)
    cv2.imwrite('dtc.png', imgSaida)

    exit()
    imSaida = DCT_inversa(imSaida)
    cv2.imwrite('inverse.jpg', imSaida)

if(__name__ == "__main__"):
    main()