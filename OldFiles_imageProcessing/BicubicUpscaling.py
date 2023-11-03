import numpy as np
import cv2
import math 
import sys, time

def bicubic_upscale (framePath, zoom_factor, num):
    #framePath : stringa path del frame
    #zoom_factor : decimale fattore di upscale dell'immagine
    #num : numero intero che indentifica il frame

    def buildKernel(s, a): 
        if (abs(s) >= 0) & (abs(s) <= 1): 
            return (a+2)*(abs(s)**3)-(a+3)*(abs(s)**2)+1
            
        elif (abs(s) > 1) & (abs(s) <= 2): 
            return a*(abs(s)**3)-(5*a)*(abs(s)**2)+(8*a)*abs(s)-4*a 
        return 0


    def upscale(img, zoom_factor):
        if img is not None:
            # Calcola le dimensioni della nuova immagine in base al fattore di zoom
            new_width = int(img.shape[1] * zoom_factor)
            new_height = int(img.shape[0] * zoom_factor)
            C = int (img.shape[2])

            # Crea una nuova immagine vuota con le dimensioni calcolate
            new_image = np.zeros((new_height, new_width, img.shape[2]), dtype=np.uint8)

            # estendo i bordi dell'immagine con un padding di 2px su ogni lato
            img = cv2.copyMakeBorder(img, 2, 2, 2, 2, cv2.BORDER_CONSTANT, value=[0, 0, 0])

            # Fattore di interpolazione (parametro che influisce sulla forma della funzione di interpolazione bicubica.)
            a = -0.5

            h = 1/zoom_factor

            inc = 0
  
            for c in range(C): 
                for j in range(new_height): 
                    for i in range(new_width): 
        
                        # Getting the coordinates of the 
                        # nearby values 
                        x, y = i * h + 2, j * h + 2
        
                        x1 = 1 + x - math.floor(x) 
                        x2 = x - math.floor(x) 
                        x3 = math.floor(x) + 1 - x 
                        x4 = math.floor(x) + 2 - x 
        
                        y1 = 1 + y - math.floor(y) 
                        y2 = y - math.floor(y) 
                        y3 = math.floor(y) + 1 - y 
                        y4 = math.floor(y) + 2 - y 
        
                        # Considering all nearby 16 values 
                        mat_l = np.matrix([[buildKernel(x1, a), buildKernel(x2, a), buildKernel(x3, a), buildKernel(x4, a)]]) 
                        mat_m = np.matrix([[img[int(y-y1), int(x-x1), c], 
                                            img[int(y-y2), int(x-x1), c], 
                                            img[int(y+y3), int(x-x1), c], 
                                            img[int(y+y4), int(x-x1), c]], 
                                        [img[int(y-y1), int(x-x2), c], 
                                            img[int(y-y2), int(x-x2), c], 
                                            img[int(y+y3), int(x-x2), c], 
                                            img[int(y+y4), int(x-x2), c]], 
                                        [img[int(y-y1), int(x+x3), c], 
                                            img[int(y-y2), int(x+x3), c], 
                                            img[int(y+y3), int(x+x3), c], 
                                            img[int(y+y4), int(x+x3), c]], 
                                        [img[int(y-y1), int(x+x4), c], 
                                            img[int(y-y2), int(x+x4), c], 
                                            img[int(y+y3), int(x+x4), c], 
                                            img[int(y+y4), int(x+x4), c]]]) 
                        mat_r = np.matrix( 
                            [[buildKernel(y1, a)], [buildKernel(y2, a)], [buildKernel(y3, a)], [buildKernel(y4, a)]]) 
                        
                        # Here the dot function is used to get the dot  
                        # product of 2 matrices 
                        new_image[j, i, c] = np.dot(np.dot(mat_l, mat_m), mat_r) 

            return new_image
        else:
            print("Errore.")
            return None



    frame = cv2.imread(framePath)

    upscaledImage = upscale(frame, zoom_factor)


    if upscaledImage is not None:

        # Applica il filtro bilaterale a upscaledImage
        bilateral_filtered_image = cv2.bilateralFilter(upscaledImage, d=9, sigmaColor=150, sigmaSpace=150)

        # Applica il miglioramento della nitidezza (sharpening) con il filtro Unsharp Mask 
        sharpened_image = cv2.addWeighted(upscaledImage, 0.5, bilateral_filtered_image, 0.5, 0)

        cv2.imwrite("progetto-principi/materials/output/upscaling/bicubic/img_upscaledBicubic"+str(num)+".png", upscaledImage)  # Salva l'immagine elaborata su disco
        cv2.imwrite("progetto-principi/materials/output/upscaling/bicubic/img_upscaledBicubic_bilateral"+str(num)+".png", bilateral_filtered_image)  # Salva l'immagine elaborata su disco
        cv2.imwrite("progetto-principi/materials/output/upscaling/bicubic/img_upscaledBicubic_bilateral_sharpened"+str(num)+".png", sharpened_image)  # Salva l'immagine elaborata su disco
        
    return frame, upscaledImage, bilateral_filtered_image, sharpened_image
