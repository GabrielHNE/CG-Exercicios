import cv2
import numpy as np
import math

def getChannelInGrey(img_src, channel):
    channels = [
        lambda : img_src[:,:,2], #red
        lambda : img_src[:,:,1], #green
        lambda : img_src[:,:,0]  #blue
    ]

    if channel >= len(channels):
        return None
    
    return channels[channel]()

def getChannelInRGB(img_src, channel):
    img = img_src.copy()

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

def toCMYK(R, G, B):
    # cv2.imshow('Red Channel', R)
    # cv2.imwrite('R_channel_colorido.jpg', R)

    # cv2.imshow('Green channel',G)
    # cv2.imwrite('G_channel_colorido.jpg', G)

    # cv2.imshow('Blue channel', B)
    # cv2.imwrite('B_channel_colorido.jpg', B)

    # normalizar R G B
    R = R / 255
    G = G / 255
    B = B / 255

    # * 255 para printar em RGB depois
    C = (1 - R[:,:, 2])
    M = (1 - G[:,:, 1])
    Y = (1 - B[:,:, 0])

    # salva em greyscale
    cv2.imwrite('C_channel_grey.jpg', C * 255)
    cv2.imwrite('M_channel_grey.jpg', M * 255)
    cv2.imwrite('Y_channel_grey.jpg', Y * 255)

    K = C.copy()

    for i in range(C.shape[0]):
        for j in range(C.shape[1]):
            K[i,j] = min(C[i,j], M[i,j], Y[i,j])

            if(K[i,j] == 1):
                C[i,j] = 1
                M[i,j] = 1
                Y[i,j] = 1
            else:
                C[i,j] = (C[i,j] - K[i,j]) / (1 - K[i,j])
                M[i,j] = (M[i,j] - K[i,j]) / (1 - K[i,j])
                Y[i,j] = (Y[i,j] - K[i,j]) / (1 - K[i,j])


    R[:,:, 0] = C[:,:] * 255
    R[:,:, 1] = C[:,:] * 255
    R[:,:, 2] = 0

    G[:,:, 1] = Y[:,:] * 255
    G[:,:, 2] = Y[:,:] * 255
    G[:,:, 0] = 0

    B[:,:, 0] = M[:,:] * 255
    B[:,:, 2] = M[:,:] * 255
    B[:,:, 1] = 0

    cK = R.copy()
    cK[:,:, 0] = K[:,:] * 255
    cK[:,:, 1] = K[:,:] * 255
    cK[:,:, 2] = K[:,:] * 255

    cv2.imwrite('C_channel.jpg', R)
    cv2.imwrite('M_channel.jpg', G)
    cv2.imwrite('Y_channel.jpg', B)
    cv2.imwrite('K_channel.jpg', cK)

    print("CMYK calculado!")

def toHSI(R, G, B):
    # normalizar R G B
    R = R / 255
    G = G / 255
    B = B / 255

    theta = R[:,:, 1] # apenas herdando o shape de R
    H = R[:,:,1]
    S = R[:,:,1]
    I = R[:,:,1]

    print("Shape: ",theta.shape)

    for i in range(theta.shape[0]):
        for j in range(theta.shape[1]):
            # obtendo theta
            val1 = 0.5 * ( (R[i,j,2] - G[i,j,1]) + (R[i,j,2] - B[i,j,0]) )
            val2 = (math.sqrt((R[i,j,2] - G[i,j,1] )**2 + (R[i,j,2] - B[i,j,0]) * (G[i,j,1] - B[i,j,0])) )

            #Assumindo que vai pra inf+
            if(val2 == 0): val2 = 1

            theta[i,j] = math.acos( val1 / val2 )

            #obtendo H
            if( B[i,j,0] <= G[i,j,1] ):
                H[i,j] = theta[i,j]
            
            elif( B[i,j,0] > G[i,j,1]):
                H[i,j] = 360 - theta[i,j]

            #obtendo S
            val1 = ( R[i,j,2] + G[i,j,1] + B[i,j,0] )
            if val1 == 0:
                S[i,j] = 1
            else:
                S[i,j] = 1 - (3/val1) * (min(R[i,j,2], G[i,j,1], B[i,j,0]))

            #obtendo I
            I[i,j] = ( R[i,j,2] + G[i,j,1] + B[i,j,0] ) / 3
            
    print("HSI calculado!")

# The function cv2.imread() is used to read an image.
ori_img = cv2.imread('UEL.jpg')

R = getChannelInRGB(ori_img, 'red') # RED
G = getChannelInRGB(ori_img, 'green') # GREEN
B = getChannelInRGB(ori_img, 'blue') # BLUE
 
toCMYK(R.copy(), G.copy(), B.copy())
toHSI(R.copy(), G.copy(), B.copy())
 
cv2.imwrite('red_channel_colorido.jpg', R)
cv2.imwrite('green_channel_colorido.jpg', G)
cv2.imwrite('Blue_channel_colorido.jpg', B)

cv2.destroyAllWindows()

