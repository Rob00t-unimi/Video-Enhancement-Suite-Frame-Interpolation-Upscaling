import cv2
from BilinearUpscaling import bilinear_upscale
import os

def video_upscaling(input_video_path, output_video_path, zoom_factor, upscaleIterations):

    # Apri la capture del video
    cap = cv2.VideoCapture(input_video_path)
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    # Funzione per stampare la % di export
    def loopState(num):
        os.system('cls' if os.name == 'nt' else 'clear')
        print("Video Upscaling: {:.2f}%".format(num / frame_count * 100))
        print("Elaborated frames: ", num , "/", frame_count)

    if not cap.isOpened():
        print("Impossibile aprire il video di input.")
        return

    # Legge le dimensioni dei frame del video
    frame_width = int(cap.get(3))
    frame_height = int(cap.get(4))

    # Crea un oggetto VideoWriter per scrivere il video di output
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter(output_video_path, fourcc, 20.0, (frame_width, frame_height))

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
            upscaled_frame = bilinear_upscale(tmp, zoom_factor)
            tmp = upscaled_frame

        # Scrivi il frame elaborato nel video di output
        out.write(tmp)
        state += 1
        loopState(state)

    # Rilascia la capture
    cap.release()
    out.release()

    print("Upscaling Completed.")
