import numpy as np
import cv2

frame = "progetto-principi/materials/input/frame1.png"

zoom_factor = 1.5

def bilinear_upscale(input_image, zoom_factor):

    img = cv2.imread(input_image)

    if img is not None:
        # Calcola le dimensioni della nuova immagine in base al fattore di zoom
        new_width = int(img.shape[1] * zoom_factor)
        new_height = int(img.shape[0] * zoom_factor)

        # Crea una nuova immagine vuota con le dimensioni calcolate
        new_image = np.zeros((new_height, new_width, img.shape[2]), dtype=np.uint8)

        # Riempie la nuova immagine con i pixel interpolati dall'immagine di input

        #data la posizione O(xo,yo) della nuova immagine il corrispondente nell'immagine in input I(xi,yi)
        #viene cosi calcolato (xi, yi) = (xo/zoom_factor, yo/zoom_factor)
        #una volta trovati il corripondente (xi,yi) posso calcolare quali sono i suoi vicini ovvero
        #xI0= int(xI)   -->  (xI0, yI0)
        #xI1= xI0+ 1    -->  (xI1, yI0)
        #yI0= int(yI)   -->  (xI0, yI1)
        #yI1= yI0+ 1    -->  (xI1, yI1)

        #l'interpolazione viene cosi calcolata:
        #I0 = I(xI0, yI0) ⋅ (xI1 − xI) + I(xI1, yI0) ⋅ (xI − xI0)
        #I1 = I(xI0, yI1) ⋅ (xI1 − xI) + I(xI1, yI1) ⋅ (xI − xI0)
        #O(xO, yO) = I0 ⋅ (yI1 − yI) + I1 ⋅ (yI − yI0)

        return new_image
    else:
        print("Impossibile leggere l'immagine di input.")
        return None


upscaledImage = bilinear_upscale(frame, zoom_factor)


if upscaledImage is not None:
    cv2.imwrite("progetto-principi/materials/output/img_upscaled.png", upscaledImage)  # Salva l'immagine elaborata su disco
    cv2.imshow("progetto-principi/materials/output/img_upscaled.png", upscaledImage)  # Mostra l'immagine elaborata
    cv2.waitKey(0)
    cv2.destroyAllWindows()
