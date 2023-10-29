import numpy as np
import cv2

def bilinear_upscale (framePath, zoom_factor, num):
    #framePath : stringa path del frame
    #zoom_factor : decimale fattore di upscale dell'immagine
    #num : numero intero che indentifica il frame

    def upscale(img, zoom_factor):

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



    frame = cv2.imread(framePath)

    upscaledImage = upscale(frame, zoom_factor)


    if upscaledImage is not None:

        # Applica il filtro bilaterale a upscaledImage
        bilateral_filtered_image = cv2.bilateralFilter(upscaledImage, d=11, sigmaColor=150, sigmaSpace=150)

        # Applica il miglioramento della nitidezza (sharpening) con il filtro Unsharp Mask 
        sharpened_image = cv2.addWeighted(upscaledImage, 0.5, bilateral_filtered_image, 0.5, 0)

        cv2.imwrite("progetto-principi/materials/output/img_upscaledBilinear"+str(num)+".png", sharpened_image)  # Salva l'immagine elaborata su disco
    
    return frame, bilateral_filtered_image, sharpened_image
