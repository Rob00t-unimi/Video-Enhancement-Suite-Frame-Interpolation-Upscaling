import cv2
from BilinearUpscaling import bilinear_upscale
import sys
import numpy as np
import time
import imageio

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


    # # Crea un oggetto VideoWriter per scrivere il video di output
    # fourcc = cv2.VideoWriter_fourcc(*'XVID')
    # out = cv2.VideoWriter(output_video_path, fourcc, originalFps, frame_size, isColor=True)
    out = imageio.get_writer(output_video_path, fps=originalFps, quality=8, codec='h264')

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
            blur_k_dim = int(filtersValues["blur_k_dim"])
            blur_sigma_x = filtersValues["blur_sigma_x"]
            sharp_k_center = filtersValues["sharp_k_center"]
            Laplacian_k_size = int(filtersValues["Laplacian_k_size"])
            threshold_value = int(filtersValues["threshold_value"])
                
            # Applica il filtro gaussiano a upscaledImage (blurring)
            blurred_image = cv2.GaussianBlur(tmp, (blur_k_dim, blur_k_dim), blur_sigma_x)      # smoothing

            # Applico lo sharpening all'immagine upscalata
            sh_val = (sharp_k_center - 1)/8
            sharpening_kernel = np.array([[-sh_val, -sh_val, -sh_val],
                                        [-sh_val, sharp_k_center, -sh_val],
                                        [-sh_val, -sh_val, -sh_val]], dtype=np.float32)
            sharpened_image = cv2.filter2D(tmp, -1, sharpening_kernel, borderType=cv2.BORDER_DEFAULT)

            # Edge detector dell'immagine upscalata
            laplacian = cv2.Laplacian(tmp, cv2.CV_16S, ksize=Laplacian_k_size)
            laplacian = cv2.convertScaleAbs(laplacian)

            # Creo un'immagine binarizzata da usare come maschera a partire dall'edge detector
            _, binary_mask = cv2.threshold(laplacian, threshold_value, 255, cv2.THRESH_BINARY)

            result = blurred_image.copy()

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
        # out.write(filteredImage)

        if len(frame.shape)==2:
            filteredImage = cv2.cvtColor(filteredImage, cv2.COLOR_BGR2GRAY)
        else:
            filteredImage = cv2.cvtColor(filteredImage, cv2.COLOR_BGR2RGB)

        out.append_data(filteredImage)
        state += 1
        loopState(state)

    # Rilascia la capture
    cap.release()
    # out.release()
    out.close()

    end_time = time.time()
    elapsed_time = end_time - start_time

    print("Upscaling Completed.")
    print(f"Tempo impiegato: {elapsed_time} secondi")
