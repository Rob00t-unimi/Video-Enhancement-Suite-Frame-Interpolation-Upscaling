import cv2

class VideoInfo:
    def __init__(self, inputVideoPath=None):
        set.videoPath(self, inputVideoPath)

    def calc_new_fps(self, numFramesInterpol):
        tot_finalFrames = numFramesInterpol * (self.numFrames - 1)
        finalFps = tot_finalFrames / self.duration
        return finalFps

    def calc_new_shape(self, zoomFactor, numIterations):
        final_upscaling = zoomFactor ** numIterations
        newWidth = int(self.width * final_upscaling)
        newHeight = int(self.height * final_upscaling)
        return newWidth, newHeight

    def set_videoPath(self, inputVideoPath):
        if inputVideoPath and inputVideoPath != "":
            self.capture = cv2.VideoCapture(inputVideoPath)
            if self.capture.isOpened():
                self.numFrames = int(self.capture.get(cv2.CAP_PROP_FRAME_COUNT))
                self.fps = self.capture.get(cv2.CAP_PROP_FPS)
                self.duration = float(self.numFrames) / float(self.fps)

                ret, frame = self.capture.read()
                if ret:
                    self.width, self.height, _ = frame.shape
                    self.cover = frame
                self.capture.release()
            else:
                raise ValueError("Error: Unable to open the video file.")
        else:
            self.capture = None
            self.numFrames = None
            self.fps = None
            self.width = None
            self.height = None
            self.duration = None
            self.cover = None