import numpy as np
import cv2

def bicubic_upscale (framePath, zoom_factor, num):
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

            # Fattore di interpolazione
            a = -0.5

            for y in range(new_height):
                for x in range(new_width):
                    # Calcola le coordinate nell'immagine di input
                    xi = x / zoom_factor
                    yi = y / zoom_factor

                    # Calcola i punti nell'immagine di input
                    xi0 = int(xi)
                    xi1 = min(xi0 + 1, img.shape[1] - 1)
                    yi0 = int(yi)
                    yi1 = min(yi0 + 1, img.shape[0] - 1)

                    # Calcola i pesi per l'interpolazione bicubica
                    dx = xi - xi0
                    dy = yi - yi0

                    # Calcola i valori interpolati usando l'interpolazione bicubica
                    interpolated_value = 0
                    for channel in range(img.shape[2]):
                        p = 0
                        for j in range(-1, 3):
                            for i in range(-1, 3):
                                x_val = min(max(xi0 + i, 0), img.shape[1] - 1)
                                y_val = min(max(yi0 + j, 0), img.shape[0] - 1)
                                interpolated_value += img[y_val, x_val, channel] * (
                                    (1 - abs(xi0 - x_val - a)) ** 3
                                ) * ((1 - abs(yi0 - y_val - a)) ** 3)
                                p += 1

                        new_image[y, x, channel] = max(0, min(int(interpolated_value), 255))

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

        cv2.imwrite("progetto-principi/materials/output/img_upscaledBicubic"+str(num)+".png", sharpened_image)  # Salva l'immagine elaborata su disco
    
    return frame, bilateral_filtered_image, sharpened_image
