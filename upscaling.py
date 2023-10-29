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
        for y in range(new_height):
            for x in range(new_width):
                # Calcola le coordinate nell'immagine di input
                xi = x / zoom_factor
                yi = y / zoom_factor

                # Calcola i quattro punti più vicini nell'immagine di input
                xi0 = int(xi)
                xi1 = min(xi0 + 1, img.shape[1] - 1)
                yi0 = int(yi)
                yi1 = min(yi0 + 1, img.shape[0] - 1)

                # Calcola i pesi per l'interpolazione
                dx = xi - xi0
                dy = yi - yi0

                # Esegue l'interpolazione bilineare
                I0 = img[yi0, xi0] * (1 - dx) + img[yi0, xi1] * dx
                I1 = img[yi1, xi0] * (1 - dx) + img[yi1, xi1] * dx
                new_image[y, x] = I0 * (1 - dy) + I1 * dy

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
