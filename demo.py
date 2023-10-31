from imageProcessing.BicubicUpscaling import bicubic_upscale
from BilinearUpscaling import bilinear_upscale
from imageProcessing.visualize import visualizeUpscaledImages
from videoFrameInterpolation import frameInterpolation
from videoFrameUpscaling import video_upscaling
import msvcrt

#Video Upscaling
input_video_path = "materials/stockVideos/short_480p_10fps.mp4"  # Sostituisci con il percorso del tuo video di input
output_video_path = "materials/output/VideoProcessing/VideoUpscaling/upscaledVideo.avi"  # Sostituisci con il percorso in cui desideri salvare il video di output
zoom_factor = 1.5  # fattore di upscaling desiderato
iterazioniUpscaling = 1 # numero di volte in cui viene eseguito l'upscaling sullo stesso frame

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
