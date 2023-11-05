from videoFrameInterpolation import frameInterpolation
from videoFrameUpscaling import video_upscaling
import msvcrt

# Per una questione computazionale inverto le operazioni, prima interpolo il frame rate e poi faccio upscaling

def start(selected_video, iterazioniUpscaling, numInterpolateFrames, zoom_factor, filtersValues, updateProgress1, updateProgress2, interpolationFirst): 

    # #Video Path
    # input_video_path = SelectVideo("Lights10") # Valori accettati: Tunnel, Waves, Rallye, Smoke, Monochrome, Lights, Bees, Lights10
    outputPath1 = "materials/output/VideoProcessing/FrameInterpolation/InterpolatedVideo.avi"  
    outputPath2 = "materials/output/VideoProcessing/VideoUpscaling/InterpolatedVideo-Upscaled.avi"

    outputPath3 = "materials/output/VideoProcessing/FrameInterpolation/UpscaledVideo.avi"  
    outputPath4 = "materials/output/VideoProcessing/VideoUpscaling/UpscaledVideo-Interpolated.avi"

    # #Parametri
    # zoom_factor = 1.5  # fattore di upscaling desiderato
    # iterazioniUpscaling = 1 # numero di volte in cui viene eseguito l'upscaling sullo stesso frame
    # numInterpolateFrames = 10 #numero di frame da interpolare per ogni coppia di frame
    # #upscaling finale = zoom_factor elevato** iterazioniUpscaling

    # # Filtri applicati durante l'upscaling (se filtro = None non viene applicato)

    # # increaseContrast = {
    # #     "alpha": ,
    # #     "beta": 
    # # }
    # # # se si vuole disabilitare manualmente i filtri:
    # # filtersValues = None
    increaseContrast = None

    def start_frame_interpolation(input_path, output_path, numInterpolateFrames, updateProgress1):
        print("Starting Frame Interpolation...")
        frameInterpolation(input_path, output_path, numInterpolateFrames, updateProgress1)
        print("Final Video There:" + output_path)

    def start_upscaling(input_path, output_path, iterazioniUpscaling, zoom_factor, filtersValues, updateProgress2):
        print("Starting Upscaling...")
        video_upscaling(input_path, output_path, zoom_factor, iterazioniUpscaling, filtersValues, increaseContrast, updateProgress2)
        print("New Video There:" + output_path)

    if interpolationFirst:
        start_frame_interpolation(selected_video, outputPath1, numInterpolateFrames, updateProgress1)
        start_upscaling(outputPath1, outputPath2,iterazioniUpscaling, zoom_factor, filtersValues, updateProgress2)
    else:
        start_upscaling(selected_video, outputPath3,iterazioniUpscaling, zoom_factor, filtersValues, updateProgress2)
        start_frame_interpolation(outputPath3, outputPath4, numInterpolateFrames, updateProgress1)
    print("End of System")


