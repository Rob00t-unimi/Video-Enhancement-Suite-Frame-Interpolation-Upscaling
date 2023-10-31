import cv2
import numpy as np
import os

def main(video_name):

    capture = cv2.VideoCapture(video_name)

    if not capture.isOpened():
        print("ERROR: Failed to open the video")
        return
    
    originalFps = int(capture.get(cv2.CAP_PROP_FPS))
    frame_count = int(capture.get(cv2.CAP_PROP_FRAME_COUNT))
    originalSeconds = frame_count / originalFps

    num_adding_frames = 3
    tot_finalFrames = num_adding_frames*(frame_count-1)
    finalFps = tot_finalFrames/originalSeconds

    def printInfo():
        print("ORIGINAL fps: ", originalFps, ", frames: " , frame_count, " sec: " , originalSeconds)
        print("FINAL fps: ", finalFps, ", frames: " , tot_finalFrames, " sec: " , originalSeconds)

    dWidth = int(capture.get(cv2.CAP_PROP_FRAME_WIDTH))
    dHeight = int(capture.get(cv2.CAP_PROP_FRAME_HEIGHT))


    frame_size = (dWidth, dHeight)
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter("SlowVideo1.mp4", fourcc, finalFps, frame_size, isColor=True)

    prev_frame = None
    flowf = np.zeros((dHeight, dWidth, 3), dtype=np.uint8)
    flowb = np.zeros((dHeight, dWidth, 3), dtype=np.uint8)
    final = np.zeros((dHeight, dWidth, 3), dtype=np.uint8)

    fx, fy, bx, by = 0, 0, 0, 0

    def loopState(num):
        os.system('cls' if os.name == 'nt' else 'clear')
        printInfo()
        print("Progress: {:.2f}%".format(num / tot_finalFrames * 100))

    state = 0
    while True:
        if state == 0:
            print("Progress: 0%")
        
        loopState(state)
        ret, frame = capture.read()
        if not ret:
            break

        if prev_frame is not None:
            prevgray = cv2.cvtColor(prev_frame, cv2.COLOR_BGR2GRAY)
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            fflow = cv2.calcOpticalFlowFarneback(prevgray, gray, None, 0.5, 3, 15, 3, 3, 1.2, 0)
            bflow = cv2.calcOpticalFlowFarneback(gray, prevgray, None, 0.5, 3, 15, 3, 3, 1.2, 0)

            for t in range(num_adding_frames):   
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
                loopState(state)

        prev_frame = frame

    capture.release()
    out.release()

if __name__ == "__main__":
    video_name = "materials/stockVideos/rallye_-_1295(Original).mp4"
    main(video_name)

    capture = cv2.VideoCapture("SlowVideo1.mp4")
    print("EXPORT fps: ", int(capture.get(cv2.CAP_PROP_FPS)), ", frames: " , int(capture.get(cv2.CAP_PROP_FRAME_COUNT)), " sec: " , int(capture.get(cv2.CAP_PROP_FRAME_COUNT)) / int(capture.get(cv2.CAP_PROP_FPS)))

    print("Completed")