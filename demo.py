from videoFrameInterpolation import frameInterpolation
from videoFrameUpscaling import video_upscaling
import msvcrt
from SelectionPage import SelectFilters, SelectVideo


#Video Path
input_video_path = SelectVideo("Tunnel") # Valori accettati: Tunnel, Waves, Rallye, Smoke, Monochrome, Lights, Bees
output_video_path = "materials/output/VideoProcessing/VideoUpscaling/upscaledVideo.avi"  
zoom_factor = 1.5  # fattore di upscaling desiderato
iterazioniUpscaling = 2 # numero di volte in cui viene eseguito l'upscaling sullo stesso frame

#upscaling finale = zoom_factor elevato** iterazioniUpscaling

# Filtri applicati durante l'upscaling (se filtro = None non viene applicato)
bilateralFilter, sharpening, increaseContrast = SelectFilters("Tunnel")     #Valori accettati: Tunnel, Waves, Rallye, None, Default



# # Se si vuole impostare un path manualmente: 
# input_video_path = SelectVideo("materials/input/stockVideos/" + "")

# # Configurazione filtri manuale: 
# bilateralFilter = {
#     "d": ,
#     "sigmaColor": ,
#     "sigmaSpace": 
# }
# sharpening = {
#     "weight_upscaled_image": ,
#     "weight_current_image": 
# }
# increaseContrast = {
#     "alpha": ,
#     "beta": 
# }

# # Disabilitare manualmente alcuni filtri:
# bilateralFilter = None
# sharpening = None
# increaseContrast = None


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
