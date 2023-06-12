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

class Filter:

    def _init_(self):
        pass

def showHistogram(histogram):
    plt.bar(range(0,256), histogram)
    plt.show()

def nthOdd(number: int):
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

def main():
    Im = Imagem("teste_2.png")

    imagem = Im.open()

    filtroMedia = np.ones((3,3), dtype=int) * (1.0/9.0)  
    
    filtroPassaAlta = np.array([
        [-1, -1, -1],
        [-1, +8, -1],
        [-1, -1, -1]
    ], dtype=int)
    
    newImg = convolucao(imagem, blur)

    cv2.imshow("Imagem", newImg)
    cv2.imwrite("filtered.png", newImg)
    cv2.waitKey(0)

if(__name__ == "__main__"):
    main()