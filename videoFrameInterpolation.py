import cv2
import numpy as np
import os

def frameInterpolation(video_name):

    capture = cv2.VideoCapture(video_name)

    if not capture.isOpened():
        print("ERROR: Failed to open the video")
        return
    
    # Estraggo le captures del video originale
    originalFps = int(capture.get(cv2.CAP_PROP_FPS))
    frame_count = int(capture.get(cv2.CAP_PROP_FRAME_COUNT))
    originalSeconds = frame_count / originalFps

    # Calcolo le captures del video dopo l'elaborazione
    num_adding_frames = 3   # elaborazione di 3 frames tra ogni coppia di frame originali, gli originali vengono scartati
    tot_finalFrames = num_adding_frames*(frame_count-1)
    finalFps = tot_finalFrames/originalSeconds

    # Stampo le info
    def printInfo():
        print("ORIGINAL fps: ", originalFps, ", frames: " , frame_count, " sec: " , originalSeconds)
        print("FINAL fps: ", finalFps, ", frames: " , tot_finalFrames, " sec: " , originalSeconds)

    # Estraggo dimensioni dei frame
    dWidth = int(capture.get(cv2.CAP_PROP_FRAME_WIDTH))
    dHeight = int(capture.get(cv2.CAP_PROP_FRAME_HEIGHT))
    frame_size = (dWidth, dHeight)

    # Set del writer del nuovo video con codec XVID, captures e frame size calcolate
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter("materials/output/FrameInterpolation/Videos/InterpolatedVideo.avi", fourcc, finalFps, frame_size, isColor=True)

    prev_frame = None   # parto dal primo frame quindi setto il precedente a None

    # Set di 3 matrici (frame) all zeros
    flowf = np.zeros((dHeight, dWidth, 3), dtype=np.uint8)
    flowb = np.zeros((dHeight, dWidth, 3), dtype=np.uint8)
    final = np.zeros((dHeight, dWidth, 3), dtype=np.uint8)

    fx, fy, bx, by = 0, 0, 0, 0

    # Funzione per stampare la % di export
    def loopState(num):
        os.system('cls' if os.name == 'nt' else 'clear')
        printInfo()
        print("Progress: {:.2f}%".format(num / tot_finalFrames * 100))

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

        # Ciclo che ad ogni iterazione produce 1 frame interpolato e lo scrive nel video finale
            for t in range(num_adding_frames):   

                # Doppio ciclo che elabpra l'interpolazione dei frame sia avanti che indietro usando come peso t
                for y in range(frame.shape[0]):
                    for x in range(frame.shape[1]):
                        fxy = fflow[y, x]
                        fy = max(min(y + fxy[1] * 0.25 * t, frame.shape[0] - 1), 0)
                        fx = max(min(x + fxy[0] * 0.25 * t, frame.shape[1] - 1), 0)
                        flowf[int(fy), int(fx)] = prev_frame[y, x]

                        bxy = bflow[y, x]
                        by = max(min(y + bxy[1] * (1 - 0.25 * t), frame.shape[0] - 1), 0)
                        bx = max(min(x + bxy[0] * (1 - 0.25 * t), frame.shape[1] - 1), 0)
                        flowb[int(by), int(bx)] = frame[y, x]

                final = cv2.addWeighted(flowf, 1 - 0.25 * t, flowb, 0.25 * t, 0)
                final = cv2.medianBlur(final, 3)
                out.write(final)
                state += 1
                loopState(state)    # ad ogni scrittura di un nuovo frame aggiorna la % di export

        prev_frame = frame # aggiorna il frame precedente

    # Ho finito, rilascio la capture del video
    capture.release()
    out.release()

    # Richiedo le capture del video appena creato e stampo le informazioni che voglio vedere
    capture = cv2.VideoCapture("progetto-principi/materials/output/FrameInterpolation/Videos/InterpolatedVideo.avi")
    print("EXPORT fps: ", int(capture.get(cv2.CAP_PROP_FPS)), ", frames: " , int(capture.get(cv2.CAP_PROP_FRAME_COUNT)), " sec: " , int(capture.get(cv2.CAP_PROP_FRAME_COUNT)) / int(capture.get(cv2.CAP_PROP_FPS)))

    print("Completed")