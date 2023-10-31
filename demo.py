from videoFrameInterpolation import frameInterpolation
from videoFrameUpscaling import video_upscaling
import msvcrt

#Video Upscaling
input_video_path = "materials/input/stockVideos/waves/short720-25.mp4"  
output_video_path = "materials/output/VideoProcessing/VideoUpscaling/upscaledVideo.avi"  
zoom_factor = 1.5  # fattore di upscaling desiderato
iterazioniUpscaling = 2 # numero di volte in cui viene eseguito l'upscaling sullo stesso frame

#upscaling finale = zoom_factor elevato** iterazioniUpscaling

# # Filtri applicati durante l'upscaling (se filtro = None non viene applicato)

# # standard values:
# bilateralFilter = {
#     "d": 9,
#     "sigmaColor": 75,
#     "sigmaSpace": 75
# }
# sharpening = {
#     "weight_upscaled_image": 1.5,
#     "weight_current_image": -0.5
# }
# increaseContrast = None

# # rallye:
# bilateralFilter = {
#     "d": 9,
#     "sigmaColor": 150,
#     "sigmaSpace": 150
# }
# sharpening = {
#     "weight_upscaled_image": 0.7,
#     "weight_current_image": 0.3
# }
# increaseContrast = {
#     "alpha": 1.01,
#     "beta": 0
# }

# All filters disalbed:
bilateralFilter = None
sharpening = None
increaseContrast = None

print("Starting Upscaling...")
video_upscaling(input_video_path, output_video_path, zoom_factor, iterazioniUpscaling, bilateralFilter, sharpening, increaseContrast)
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
numInterpolateFrames = 3 #numero di frame da interpolare per ogni coppia di frame

#fps finali = numInterpolateFrames * (numFramesIniziale - 1)

print("Starting Frame Interpolation...")
frameInterpolation(inputVideoPath, outputVideoPath, numInterpolateFrames)
print("Final Video There: materials/output/VideoProcessing/VideoUpscaling/upscaledVideo.avi")

print("End of System")
