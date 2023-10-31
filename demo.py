from videoFrameInterpolation import frameInterpolation
from videoFrameUpscaling import video_upscaling
import msvcrt

#Video Upscaling
input_video_path = "materials/stockVideos/short_480p_10fps.mp4"  
output_video_path = "materials/output/VideoProcessing/VideoUpscaling/upscaledVideo.avi"  
zoom_factor = 1.5  # fattore di upscaling desiderato
iterazioniUpscaling = 1 # numero di volte in cui viene eseguito l'upscaling sullo stesso frame

#upscaling finale = zoom_factor elevato** iterazioniUpscaling

print("Starting Upscaling...")
video_upscaling(input_video_path, output_video_path, zoom_factor, iterazioniUpscaling)
print("New Video There: materials/output/VideoProcessing/VideoUpscaling/upscaledVideo.avi")
print("Press Enter to continue...")

# Attendi fino a quando viene premuto "Enter"
while True:
    if msvcrt.kbhit():
        key = msvcrt.getch()
        if key == b'\r':
            break

#frame interpolation
inputVideoPath = "materials/output/VideoProcessing/VideoUpscaling/upscaledVideo.avi"
outputVideoPath = "materials/output/VideoProcessing/FrameInterpolation/Upscaled-InterpolatedVideo.avi"

print("Starting Frame Interpolation...")
frameInterpolation(inputVideoPath, outputVideoPath)
print("Final Video There: materials/output/VideoProcessing/VideoUpscaling/upscaledVideo.avi")

print("End of System")
