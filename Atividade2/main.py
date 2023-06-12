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

def main():
    Im = Imagem("vandao.jpg")

    imagem = Im.open()

    # cv2.imshow("Imagem", imagem)
    # cv2.waitKey(0)

    pixelsR = Im.getChannelInGrey(0) # red
    pixelsG = Im.getChannelInGrey(1) # green
    pixelsB = Im.getChannelInGrey(2) # blue

    Im.calculateEqHist(pixelsR)
    Im.calculateEqHist(pixelsG)
    Im.calculateEqHist(pixelsB)

if(__name__ == "__main__"):
    print("ou")
    main()
