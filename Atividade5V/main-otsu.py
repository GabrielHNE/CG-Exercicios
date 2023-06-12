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

def histProbabiliade(histogram: np.array, pixels: int) -> np.array:
    prob = np.zeros(len(histogram))
    for i in range(0, len(histogram)):
        prob[i] = histogram[i] / pixels

    return prob

def getIntensidadesOtsu(histProb, t):

    # prob
    p1 = np.sum(histProb[:t])
    p2 = np.sum(histProb[t:])

    # intensidade media
    m1 = 0
    m2 = 0
    mg = 0
    for i in range(0, len(histProb)):
        if i <= t:
            m1 += i*histProb[i]
        else:
            m2 += i*histProb[i]

        mg += i*histProb[i]

    m1 = m1/p1
    m2 = m2/p2

    return m1, m2, mg

# def otsu(histProb):
#     t = 1
#     tMax = -1
#     oMax = -1

#     for i in range(len(histProb)):
#         m1, m2, mg = getIntensidadesOtsu(histProb, t)

#         a1 = 0 if m1-mg < 0 else m1-mg
#         a2 = 0 if m2-mg <0 else m2-mg 
#         oAux = histProb[a1]**2 + histProb[a2]**2

#         if oAux > oMax:
#             oMax = oAux
#             tMax = t

#         t +=1
#     return tMax

def otsu(gray):
    pixel_number = gray.shape[0] * gray.shape[1]
    mean_weight = 1.0/pixel_number
    his, bins = np.histogram(gray, np.arange(0,257))

    final_thresh = -1
    final_value = -1

    intensity_arr = np.arange(256)
    for t in bins[1:-1]: # This goes from 1 to 254 uint8 range (Pretty sure wont be those values)
        pcb = np.sum(his[:t])
        pcf = np.sum(his[t:])
        Wb = pcb * mean_weight
        Wf = pcf * mean_weight

        mub = np.sum(intensity_arr[:t]*his[:t]) / float(pcb)
        muf = np.sum(intensity_arr[t:]*his[t:]) / float(pcf)
        #print mub, muf
        value = Wb * Wf * (mub - muf) ** 2

        if value > final_value:
            final_thresh = t
            final_value = value
    final_img = gray.copy()
    return final_thresh

def main():
    Im = Imagem("vandao.jpg", mode=0)

    imagem = Im.open()
    t = otsu(imagem)

    lim = limiarizacao(imagem, t)
    cv2.imshow("Imagem", lim)
    cv2.waitKey(0)

if(__name__ == "__main__"):
    main()
