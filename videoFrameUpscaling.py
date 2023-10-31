import cv2
from BilinearUpscaling import bilinear_upscale
import os

def video_upscaling(input_video_path, output_video_path, zoom_factor, upscaleIterations, bilateralFilter, sharpening, increaseContrast):

    # Apri la capture del video
    cap = cv2.VideoCapture(input_video_path)

    if not cap.isOpened():
        print("Impossibile aprire il video di input.")
        return
    
    # Estraggo le captures del video originale
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    originalFps = int(cap.get(cv2.CAP_PROP_FPS))

    # Funzione per stampare la % di export
    def loopState(num):
        os.system('cls' if os.name == 'nt' else 'clear')
        print("Video Upscaling: {:.2f}%".format(num / frame_count * 100))
        print("Elaborated frames: ", num , "/", frame_count)

    # Estraggo dimensioni dei frame e le moltiplico per il fattore di zoom elevato al numero di iterazioni di upscaling
    dWidth = int(int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))*(zoom_factor**upscaleIterations))
    dHeight = int(int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))*(zoom_factor**upscaleIterations))
    frame_size = (dWidth, dHeight)

    # Crea un oggetto VideoWriter per scrivere il video di output
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter(output_video_path, fourcc, originalFps, frame_size, isColor=True)

    # Cicla su ogni frame del video
    state = 0
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
            upscaled_frame = bilinear_upscale(tmp, zoom_factor, bilateralFilter, sharpening, increaseContrast)
            tmp = upscaled_frame

        # Scrivi il frame elaborato nel video di output
        out.write(tmp)
        state += 1
        loopState(state)

    # Rilascia la capture
    cap.release()
    out.release()

    print("Upscaling Completed.")
