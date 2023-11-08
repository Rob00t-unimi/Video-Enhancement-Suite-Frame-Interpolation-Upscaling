import cv2
import numpy as np
import os
from threading import Thread
import queue

def extractInfo(input_video_path, num_adding_frames):
    #NumAdiingFrames --> elaborazione di n frames tra ogni coppia di frame originali, gli originali vengono scartati
    capture = cv2.VideoCapture(input_video_path)

    if not capture.isOpened():
        print("ERROR: Failed to open the video")
        return
    
    # Estraggo le captures del video originale
    originalFps = float(capture.get(cv2.CAP_PROP_FPS))
    frame_count = float(capture.get(cv2.CAP_PROP_FRAME_COUNT))
    originalSeconds = frame_count / originalFps
 
    tot_finalFrames = num_adding_frames*(frame_count-1)
    finalFps = tot_finalFrames/originalSeconds

    # Stampo le info
    def printInfo():
        print("ORIGINAL fps: ", originalFps, ", frames: " , frame_count, " sec: " , originalSeconds)
        print("FINAL fps: ", finalFps, ", frames: " , tot_finalFrames, " sec: " , originalSeconds)

    return finalFps, tot_finalFrames, capture, printInfo

def inizializeOut(capture, output_video_path, finalFps):
    dWidth = int(capture.get(cv2.CAP_PROP_FRAME_WIDTH))
    dHeight = int(capture.get(cv2.CAP_PROP_FRAME_HEIGHT))
    frame_size = (dWidth, dHeight)

    # Set del writer del nuovo video con codec XVID, captures e frame size calcolate
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter(output_video_path, fourcc, finalFps, frame_size, isColor=True)
    
    return dHeight, dWidth, out

# Funzione per stampare la % di export
def loopState(num, tot_finalFrames, updateProgress1, printInfo):
    os.system('cls' if os.name == 'nt' else 'clear')
    printInfo()
    print("Frame Interpolation: {:.2f}%".format(num / tot_finalFrames * 100))
    updateProgress1(num, tot_finalFrames) 

def frame_interpolation_worker(input_frames, output_frames, num_frames, t, num_adding_frames, input_video_path, loopState, state, tot_finalFrames, updateProgress1, printInfo):

    capture = cv2.VideoCapture(input_video_path)
    dWidth = int(capture.get(cv2.CAP_PROP_FRAME_WIDTH))
    dHeight = int(capture.get(cv2.CAP_PROP_FRAME_HEIGHT))

    for i in range(t, num_frames, num_adding_frames):

        ret, frame = capture.read()
        if not ret:
            break

        frame = input_frames[i]
        prev_frame = input_frames[i - 1]

        # Set di 3 matrici (frame) all zeros
        flowf = np.zeros((dHeight, dWidth, 3), dtype=np.uint8)
        flowb = np.zeros((dHeight, dWidth, 3), dtype=np.uint8)
        final = np.zeros((dHeight, dWidth, 3), dtype=np.uint8)
        fx, fy, bx, by = 0, 0, 0, 0
        
        prevgray = cv2.cvtColor(prev_frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        fflow = cv2.calcOpticalFlowFarneback(prevgray, gray, None, 0.5, 3, 15, 3, 3, 1.2, 0)
        bflow = cv2.calcOpticalFlowFarneback(gray, prevgray, None, 0.5, 3, 15, 3, 3, 1.2, 0)
        
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
        output_frames.put(final)
    loopState(state, tot_finalFrames, updateProgress1, printInfo)
    state += 1

def frameInterpolation(input_video_path, output_video_path, num_adding_frames, updateProgress1):
    
    finalFps, tot_finalFrames, capture, printInfo = extractInfo(input_video_path, num_adding_frames)
    out = inizializeOut(capture, output_video_path, finalFps)

    frames = []
    while True:
        ret, frame = capture.read()
        if not ret:
            break
        frames.append(frame)

    threads = []
    output_frames = queue.Queue()

    state = 0

    for t in range(num_adding_frames):
        thread = Thread(target=frame_interpolation_worker, args=(frames, output_frames, len(frames), t, num_adding_frames, input_video_path, loopState, state, tot_finalFrames, updateProgress1, printInfo))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    while not output_frames.empty():
        frame = output_frames.get()
        out.write(frame)
    # Release resources
    capture.release()
    out.release()

    print("Frame Interpolation Completed.")

    # Richiedo le capture del video appena creato e stampo le informazioni che voglio vedere
    capture = cv2.VideoCapture(output_video_path)
    print("EXPORT fps: ", int(capture.get(cv2.CAP_PROP_FPS)), ", frames: " , int(capture.get(cv2.CAP_PROP_FRAME_COUNT)), " sec: " , int(capture.get(cv2.CAP_PROP_FRAME_COUNT)) / int(capture.get(cv2.CAP_PROP_FPS)))

    print("Frame Interpolation Completed.")