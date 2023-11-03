from videoFrameInterpolation import frameInterpolation
from videoFrameUpscaling import video_upscaling
import msvcrt
from SelectionPage import SelectFilters, SelectVideo


#Video Path
input_video_path = SelectVideo("Lights10") # Valori accettati: Tunnel, Waves, Rallye, Smoke, Monochrome, Lights, Bees, Lights10
output_video_path = "materials/output/VideoProcessing/VideoUpscaling/upscaledVideo.avi"  

#Parametri
zoom_factor = 1.5  # fattore di upscaling desiderato
iterazioniUpscaling = 1 # numero di volte in cui viene eseguito l'upscaling sullo stesso frame
numInterpolateFrames = 10 #numero di frame da interpolare per ogni coppia di frame

#upscaling finale = zoom_factor elevato** iterazioniUpscaling

# Filtri applicati durante l'upscaling (se filtro = None non viene applicato)
filtersValues, increaseContrast = SelectFilters("Lights10")     #Valori accettati:  Bees, Bees360p, Lights10, None



# # Se si vuole impostare un path manualmente: 
#input_video_path = "materials/input/stockVideos/lights/short-720p-10fps.mp4"

# # Configurazione filtri manuale: 
# filtersValues = {
#                 "blur_k_dim": 5,
#                 "blur_sigma_x": 1,
#                 "sharp_k_center": 7,
#                 "Laplacian_k_size": 3,
#                 "threshold_value": 9,
#                 "blur_k_dim_2": 5,
#                 "blur_sigma_x_2": 1
#             }
# increaseContrast = {
#     "alpha": ,
#     "beta": 
# }

# # Disabilitare manualmente alcuni filtri:
# filtersValues = None
# increaseContrast = None


print("Starting Upscaling...")
video_upscaling(input_video_path, output_video_path, zoom_factor, iterazioniUpscaling, filtersValues, increaseContrast)
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

#fps finali = numInterpolateFrames * (numFramesIniziale - 1)

print("Starting Frame Interpolation...")
frameInterpolation(inputVideoPath, outputVideoPath, numInterpolateFrames)
print("Final Video There: materials/output/VideoProcessing/VideoUpscaling/upscaledVideo.avi")

print("End of System")
