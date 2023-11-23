import cv2
from BilinearUpscaling import bilinear_upscale
import sys
import numpy as np
import time 
import skimage
from skimage import filters, color, feature

def video_upscaling(input_video_path, output_video_path, zoom_factor, upscaleIterations, filtersValues, increaseContrast, updateProgress2):

    # Apri la capture del video
    cap = cv2.VideoCapture(input_video_path)

    if not cap.isOpened():
        print("Impossibile aprire il video di input.")
        return
    
    # Estraggo le captures del video originale
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    originalFps = int(cap.get(cv2.CAP_PROP_FPS))

    start_time = time.time()
    # Funzione per stampare la % di export
    def loopState(num):
        if num != 0:
            for _ in range(2):
                    sys.stdout.write("\033[F")  # Move the cursor up one line
                    sys.stdout.write("\033[K")  # Clear the line
        print("Video Upscaling: {:.2f}%".format(num / frame_count * 100))
        print("Elaborated frames: ", num , "/", frame_count)
        updateProgress2(num, frame_count)

    # Estraggo dimensioni dei frame e le moltiplico per il fattore di zoom elevato al numero di iterazioni di upscaling
    dWidth = int(int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))*(zoom_factor**upscaleIterations))
    dHeight = int(int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))*(zoom_factor**upscaleIterations))
    frame_size = (dWidth, dHeight)

    # Crea un oggetto VideoWriter per scrivere il video di output
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter(output_video_path, fourcc, originalFps, frame_size, isColor=True)

    # Cicla su ogni frame del video
    state = 0
    # testing

    while True:
        if state == 0:
            loopState(0)
        ret, frame = cap.read()

        if not ret:
            break
        
        # in base a upscaleIterations esegue una o più volte l'upscaling al frame selezionato
        tmp = frame
        for _ in range(upscaleIterations):
            # Applica la tua funzione di upscaling al frame
            upscaled_frame = bilinear_upscale(tmp, zoom_factor)
            tmp = upscaled_frame

        # Applicazione di filtri
        filteredImage = tmp

        if filtersValues is not None:

            #estraggo le informazioni da applicare ai filtri:
            sharp_k_center = filtersValues["sharp_k_center"]
            sharp_k_dim = int(filtersValues["sharp_k_dim"])

            # Applico lo sharpening all'immagine upscalata            
            sh_val = (sharp_k_center - 1)/(sharp_k_dim * sharp_k_dim -1)          

            sharpening_kernel = np.zeros((sharp_k_dim, sharp_k_dim), dtype=np.float32)
            for i in range(sharp_k_dim):
                for j in range(sharp_k_dim):
                    sharpening_kernel[i][j] = - sh_val
            sharpening_kernel[sharp_k_dim//2, sharp_k_dim//2] = sharp_k_center

            sharpened_image = cv2.filter2D(tmp, -1, sharpening_kernel, borderType=cv2.BORDER_DEFAULT)
           

            gray_img = color.rgb2gray(tmp)
            binary_mask = feature.canny(gray_img)

            result = tmp.copy()

            # Sostituisci solo gli edge rilevati dalla maschera binaria con gli edge sharpened
            if filtersValues["showEdges"] is False:
                result[binary_mask == 255] = sharpened_image[binary_mask == 255]
            else:
                result[binary_mask == 255] = 255

            filteredImage = result 

        # if upscaledImage is not None:

        #     if bilateralFilter is not None:
        #         # Applica il filtro bilaterale a upscaledImage
        #         bilateral_filtered_image = cv2.bilateralFilter(upscaledImage, d=bilateralFilter["d"], sigmaColor=bilateralFilter["sigmaColor"], sigmaSpace=bilateralFilter["sigmaSpace"])
        #         outputImage = bilateral_filtered_image

        #     if sharpening is not None:
                
        #         # Applica il miglioramento della nitidezza (sharpening) con il filtro Unsharp Mask 
        #         sharpened_image = cv2.addWeighted(outputImage, sharpening["weight_edge_mask"], outputImage, sharpening["weight_current_image"], 0)
        #         outputImage = sharpened_image


        if increaseContrast is not None:
            contrastedImage = cv2.convertScaleAbs(filteredImage, alpha=increaseContrast["alpha"], beta=increaseContrast["beta"])
            filteredImage = contrastedImage

        # Scrivi il frame elaborato nel video di output
        out.write(filteredImage)
        state += 1
        loopState(state)

    # Rilascia la capture
    cap.release()
    out.release()

    end_time = time.time()
    elapsed_time = end_time - start_time

    print("Upscaling Completed.")
    print(f"Tempo impiegato: {elapsed_time} secondi")
