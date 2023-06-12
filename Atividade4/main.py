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

def alpha(x, N):
    return ( 1 / math.sqrt(N)) if x == 0 else math.sqrt(2 / N) 

def DCT(imagem):
    assert imagem.shape[0] == imagem.shape[1]

    N = imagem.shape[0]
    saida = np.zeros((N,N), dtype=float)

    for i in range(0, N):
        for j in range(0, N):
            soma = 0
            
            for x in range(0, N):
                for y in range(0, N):
                    soma += imagem[x, y] * math.cos( ((2*i+1)*x*math.pi)/(2*N) ) * math.cos( ((2*j+1)*y*math.pi)/(2*N) )
            
            saida[i,j] = alpha(i, N) * alpha(j, N) * soma
    
    return saida

def DCT_inversa(imagem):
    assert imagem.shape[0] == imagem.shape[1]

    N = imagem.shape[0]
    saida = np.zeros((N,N), dtype=float)

    for i in range(0, N):
        for j in range(0, N):
            soma = 0
            
            for x in range(0, N):
                alphai = alpha(x,N)
                for y in range(0, N):
                    soma += alphai * alpha(y, N) * imagem[x,y] * math.cos( ((2*i+1)*x*math.pi)/(2*N) ) * math.cos( ((2*j+1)*y*math.pi)/(2*N) )

            saida[i,j] = soma
    
    return saida

def main():
    Im = Imagem("teste.png", mode=0)

    imagem = Im.open()
    
    imSaida = DCT(imagem)

    cv2.imwrite('cossine_frequency.jpg', imSaida)

    imSaida = DCT_inversa(imSaida)

    cv2.imwrite('inverse.jpg', imSaida)
    
if(__name__ == "__main__"):
    main()
