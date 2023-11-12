import cv2
import numpy as np
import sys
import time

def frameInterpolation(input_video_path, output_video_path, num_adding_frames, updateProgress1, filtersValues):
    #NumAdiingFrames --> elaborazione di n frames tra ogni coppia di frame originali, gli originali vengono scartati

    blur_k_dim_2 = filtersValues["blur_k_dim_2"]

    capture = cv2.VideoCapture(input_video_path)

    if not capture.isOpened():
        print("ERROR: Failed to open the video")
        return

    # Estraggo le captures del video originale
    originalFps = float(capture.get(cv2.CAP_PROP_FPS))
    frame_count = int(capture.get(cv2.CAP_PROP_FRAME_COUNT))
    originalSeconds = frame_count / originalFps

    tot_finalFrames = num_adding_frames * (frame_count - 1)
    finalFps = tot_finalFrames / originalSeconds

    # Estraggo dimensioni dei frame
    dWidth = int(capture.get(cv2.CAP_PROP_FRAME_WIDTH))
    dHeight = int(capture.get(cv2.CAP_PROP_FRAME_HEIGHT))
    frame_size = (dWidth, dHeight)

    # Set del writer del nuovo video con codec XVID, captures e frame size calcolate
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter(output_video_path, fourcc, finalFps, frame_size, isColor=True)

    prev_frame = None   # parto dal primo frame quindi setto il precedente a None

    # Set di 3 matrici (frame) all zeros
    flowf = np.zeros((dHeight, dWidth, 3), dtype=np.uint8)
    flowb = np.zeros((dHeight, dWidth, 3), dtype=np.uint8)
    final = np.zeros((dHeight, dWidth, 3), dtype=np.uint8)
    fx, fy, bx, by = 0, 0, 0, 0

    # testing
    start_time = time.time()

    def loopState(num):
        if num != 0:
            for _ in range(3):
                    sys.stdout.write("\033[F")  # Move the cursor up one line
                    sys.stdout.write("\033[K")  # Clear the line
        print("Frame Interpolation: {:.2f}%".format(num / tot_finalFrames * 100))
        updateProgress1(num, tot_finalFrames)

    state = 0

    #ciclo che continua finchè caprure read restituisce un frame successivo
    while True:
        if state == 0:
            loopState(0)

        ret, frame = capture.read()
        if not ret:
            break

        # Trasformo per lavorare in scala di grigi
        if prev_frame is not None:
            prevgray = cv2.cvtColor(prev_frame, cv2.COLOR_BGR2GRAY)
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            # Calcolo l'optical flow tra i 2 frame sia avanti che indietro
            fflow = cv2.calcOpticalFlowFarneback(prevgray, gray, None, 0.5, 3, 15, 3, 3, 1.2, 0)
            bflow = cv2.calcOpticalFlowFarneback(gray, prevgray, None, 0.5, 3, 15, 3, 3, 1.2, 0)

            y, x = np.indices(frame.shape[:2])

            # Ciclo che ad ogni iterazione produce 1 frame interpolato e lo scrive nel video finale
            for t in range(num_adding_frames):

                part = 1/num_adding_frames

                # Al posto di iterare pixel per pixel uso la possibilità di numpy di svolgere operazioni su interi array
                # Ho rimosso 2 cicli e abbattuto drasticamente il carico computazionale
                # un benchmark ci ha mostrato che con i 2 cicli annidati in 45 minuti ha esportato il 70% dei frames
                # senza cicli in 44 secondi ha esportato l'intero video

                fy = np.clip(y + fflow[:, :, 1] * part * t, 0, frame.shape[0] - 1).astype(int)
                fx = np.clip(x + fflow[:, :, 0] * part * t, 0, frame.shape[1] - 1).astype(int)
                flowf[fy, fx, :] = prev_frame[y, x]

                by = np.clip(y + bflow[:, :, 1] * (1 - part * t), 0, frame.shape[0] - 1).astype(int)
                bx = np.clip(x + bflow[:, :, 0] * (1 - part * t), 0, frame.shape[1] - 1).astype(int)
                flowb[by, bx, :] = frame[y, x]

                final = cv2.addWeighted(flowf, 1 - part * t, flowb, part * t, 0)
                final = cv2.medianBlur(final, blur_k_dim_2)    #applica un filtro di denoising per rumore sale e pepe
                out.write(final)
                state += 1
                loopState(state)  # ad ogni scrittura di un nuovo frame aggiorna la % di export

        prev_frame = frame   # aggiorna il frame precedente

    # Ho finito, rilascio la capture del video
    capture.release()
    out.release()

    # Richiedo le capture del video appena creato e stampo le informazioni che voglio vedere
    capture = cv2.VideoCapture(output_video_path)
    print("EXPORT fps: ", int(capture.get(cv2.CAP_PROP_FPS)), ", frames: ", int(capture.get(cv2.CAP_PROP_FRAME_COUNT)),
          " sec: ", int(capture.get(cv2.CAP_PROP_FRAME_COUNT)) / int(capture.get(cv2.CAP_PROP_FPS)))
    
    end_time = time.time()
    elapsed_time = end_time - start_time

    print("Frame Interpolation Completed.")
    print(f"Tempo impiegato: {elapsed_time} secondi")
