import numpy as np
import cv2

def bilinear_upscale (frame, zoom_factor):
    #frame : frame da upscalare
    #zoom_factor : decimale fattore di upscale dell'immagine

    def upscale(img, zoom_factor):

        if img is not None:
            # Calcola le dimensioni della nuova immagine in base al fattore di zoom
            new_width = int(img.shape[1] * zoom_factor)
            new_height = int(img.shape[0] * zoom_factor)

            y, x = np.indices((new_height, new_width))

            # Calcola le coordinate nell'immagine di input
            xi = x / zoom_factor
            yi = y / zoom_factor

            # Calcola i quattro punti più vicini nell'immagine di input
            xi0 = xi.astype(int)
            xi1 = np.minimum(xi0 + 1, img.shape[1] - 1)
            yi0 = yi.astype(int)
            yi1 = np.minimum(yi0 + 1, img.shape[0] - 1)

            # Calcola i pesi per l'interpolazione
            dx = xi - xi0
            dy = yi - yi0

            # Esegui l'interpolazione bilineare separatamente per i canali R, G, e B
            I0 = img[yi0, xi0, :] * (1 - dx[:, :, np.newaxis]) + img[yi0, xi1, :] * dx[:, :, np.newaxis]
            I1 = img[yi1, xi0, :] * (1 - dx[:, :, np.newaxis]) + img[yi1, xi1, :] * dx[:, :, np.newaxis]

            new_image = I0 * (1 - dy[:, :, np.newaxis]) + I1 * dy[:, :, np.newaxis]

            # Clip ai valori validi (0-255) e converti in uint8
            new_image = np.clip(new_image, 0, 255).astype(np.uint8)

            return new_image
        else:
            print("Impossibile leggere l'immagine di input.")
            return None


    # upscaledImage = upscale(frame, zoom_factor)
    
    # Nonostante sia stato abbattuto il costo computazionale evitando cicli for e agendo direttamente su tutti i pixel applicando operazioni su array con numpy
    # i benchmark hanno mostrato come un tempo di esecuzione migliorato di 7.59 minuti viene eseguito in 12 secondi con l'operazione di upscaling bilineare da libreria opencv
    #Codice equivalente che utilizza la libreria openCV --> stesso risultato ma molto più veloce
    def cv2Upscale(img, zoom_factor):
        new_width = int(img.shape[1] * zoom_factor)
        new_height = int(img.shape[0] * zoom_factor)
        upscaled_image = cv2.resize(img, (new_width, new_height), interpolation=cv2.INTER_LINEAR)
        # upscaled_image = cv2.resize(img, (new_width, new_height), interpolation=cv2.INTER_CUBIC)     # --> Bicubico di cv2 è più preciso
        return upscaled_image
    
    upscaledImage = cv2Upscale(frame, zoom_factor)

    return upscaledImage
