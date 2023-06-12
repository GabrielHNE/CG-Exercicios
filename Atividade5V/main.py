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

    def calculateHist(self, pixels):
        histogram = np.zeros(256, dtype=int)

        for i in range(pixels.shape[0]):
            for j in range(pixels.shape[1]):
                histogram[pixels[i,j]] = histogram[pixels[i,j]] + 1
        
        showHistogram(histogram)

        return histogram

def showHistogram(histogram):
    plt.bar(range(0,256), histogram)
    plt.show()

def threshold(histogram, div: int):
    acumulado1 = 0
    den1 = 0
    acumulado2 = 0
    den2 = 0
    for i in range(0, len(histogram)):

        if i < div:
            acumulado1 += histogram[i] * i
            den1 +=histogram[i]
        else:
            acumulado2 += histogram[i] * i
            den2 +=histogram[i]
    
    mean = ((acumulado1/den1) + (acumulado2/den2) ) / 2

    if round(mean) == div:
        return div
    
    return threshold(histogram, round(mean))

def limiarizacao(imagem: np.array, threshold: int) -> np.array:
    
    lin = imagem.shape[0]
    col = imagem.shape[1]
    lim = np.zeros(shape=(lin, col))

    for i in range(0,lin):
        for j in range(0,col):
            if imagem[i,j] <= threshold:
                lim[i,j] = 0
            else:
                lim[i,j] = 1

    return lim

def main():
    Im = Imagem("vandao.jpg", mode=0)

    imagem = Im.open()

    hist = Im.calculateHist(imagem)
    t = threshold(hist, len(hist)/2 )

    lim = limiarizacao(imagem, t)
    cv2.imshow("Imagem", lim)
    cv2.waitKey(0)

if(__name__ == "__main__"):
    main()
