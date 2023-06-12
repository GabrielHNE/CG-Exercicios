import cv2
import numpy as np
import math
import random
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
    return ( 1.0 / N ** 0.5) if x == 0 else (2.0 / (N ** 0.5)) 

def DCT(imagem):
    assert imagem.shape[0] == imagem.shape[1]

    N = imagem.shape[0]
    saida = np.zeros((N,N), dtype=float)

    for i in range(0, N):
        for j in range(0, N):
            soma = 0
            
            for x in range(0, N):
                for y in range(0, N):
                    soma += imagem[x, y] * math.cos( ((2*x+1)*i*math.pi)/(2*N) ) * math.cos( ((2*y+1)*j*math.pi)/(2*N) )
            
            saida[i,j] = alpha(i, N) * alpha(j, N) * soma
    
    return saida

def DCT_inversa(imagem):
    assert imagem.shape[0] == imagem.shape[1]

    N = imagem.shape[0]
    saida = np.zeros(shape=(N,N), dtype=float)

    for x in range(0, N):
        for y in range(0, N):
            soma = 0
            
            for i in range(0, N):
                alphai = alpha(i,N)
                for j in range(0, N):
                    soma += alphai * alpha(j, N) * imagem[i,j] * math.cos( (((2.0*x)+1)*i*math.pi)/(2*N) ) * math.cos( (((2*y)+1)*j*math.pi)/(2*N) )

            saida[x,y] = soma
    
    return saida

def nthOdd(number: int):
    cont = 0

    while( number > 1 ):
        number -= 2
        cont += 1 

    return cont

def convolucao(imagem, filtro) -> np.array:
    img_size = imagem.shape[0]
    newImg = np.zeros(shape=(img_size,img_size))

    n = filtro.shape[0]
    gap = nthOdd(n)

    # Loop through the image
    for i in range(gap, img_size - gap):
        for j in range(gap, img_size - gap):
            subMat = imagem[i-gap: i+gap+1, j-gap:j+gap+1]

            newImg[i,j] = np.sum(np.multiply(subMat, filtro))

    return newImg

def normalize_maxmin(img):
    return (img-img.min())/(img.max()-img.min())*255

def get_subsection(array, size=10, i = 0, j = 0):
    return array[i : i+size, j : j+size]

def centralize_dct(img):
    '''
        Cria 3 copias de img e centraliza a imagem formada no canto superior esquerdo
    '''
    assert img.shape[0] == img.shape[1]

    size = img.shape[0]
    out = np.zeros(shape=(size*2,size*2))

    leftup = np.flip(img.copy())
    rightup = np.flipud(img.copy())
    leftdown = np.fliplr(img.copy())
    rightdown = img.copy()

    for i in range(size*2):
        for j in range(size*2):
            
            # i: 0 ate size; j: 0 ate size
            if i < size and j < size: 
                out[i,j] = leftup[i, j]

            elif i < size and j >=size:
                out[i,j] = rightup[i, j-size]

            
            if i >= size and j < size:
                out[i,j] = leftdown[i-size, j]
            
            elif i >= size and j >= size:
                out[i,j] = rightdown[i-size, j-size]

    return out

def cria_ruido(img, noise=255, lim=10):
    size = img.shape[0]
    
    out = np.zeros(shape=(size,size))

    i = random.randint(0,size-1)
    j = random.randint(0,size-1)

    for u in range(i, lim):
        for v in range(j, lim):
            x = random.randint(1,3)

            if x == 2:
                out[u,v] = noise
    
    return out

def filtros_ideais(freq: np.array, raio = 0.7):
    size = freq.shape[0]
    passaBaixa = np.zeros(shape=(size, size), dtype=np.float32)
    passaAlta = np.zeros(shape=(size, size), dtype=np.float32)

    dr = raio*size

    for x in range(size):
        for y in range(size):
            d = math.sqrt(x**2 + y**2)

            if( int(d) <= dr):
                passaBaixa[x,y] = freq[x,y]
            else:
                passaAlta[x,y] = freq[x,y]
    
    return passaBaixa, passaAlta

def cria_ruido_periodico(img, direcao=0, gap=5):
    size = img.shape[0]
    img_ruido = img

    # horizontal
    if direcao == 0:
        for x in range(0, size, gap):
            for y in range(size):
                img_ruido[x,y] = 255
    # vertical
    elif direcao == 1:
        for x in range(size):
            for y in range(0, size, gap):
                img_ruido[x,y] = 255

    return img_ruido


def main():
    Im = Imagem("testes/circle.png", mode=0)
    imagem = Im.open()

    imagem = cria_ruido_periodico(imagem)
    cv2.imwrite('imagem_ruido.png', imagem)
    
    # calcula discrete cousine tranformation
    dct = DCT(imagem)
    cv2.imwrite('dct.png', dct)

    # # centraliza a frequencia
    # combined_pic = centralize_dct(dct)
    # cv2.imwrite('combined.png',combined_pic)

    # recupera a imagem original
    # a original está no rightdown
    # filtered = get_subsection(filteredCombined, size=dct.shape[0], i = dct.shape[0], j = dct.shape[0])

    passaBaixa, passaAlta = filtros_ideais(dct)

    # calcula dct inversa passa baixa
    imgSaida = DCT_inversa(passaBaixa)
    # normaliza entre 0-255 com base no max e min de imgSaida
    normalizedPB = normalize_maxmin(imgSaida)
    cv2.imwrite('dcti_PB.png', normalizedPB)

    # calcula dct inversa passa alta
    imgSaida = DCT_inversa(passaAlta)
    # normaliza entre 0-255 com base no max e min de imgSaida
    normalizedPA = normalize_maxmin(imgSaida)
    cv2.imwrite('dcti_PA.png', normalizedPA)
    
if(__name__ == "__main__"):
    main()
