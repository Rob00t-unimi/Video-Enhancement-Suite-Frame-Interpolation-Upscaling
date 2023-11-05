from videoFrameInterpolation import frameInterpolation
from videoFrameUpscaling import video_upscaling
import msvcrt
from SelectionPage import SelectFilters, SelectVideo

# Per una questione computazionale inverto le operazioni, prima interpolo il frame rate e poi faccio upscaling

def start(selected_video, iterazioniUpscaling, numInterpolateFrames, zoom_factor, filtersValues, updateProgress1, updateProgress2): 
    # #Video Path
    # input_video_path = SelectVideo("Lights10") # Valori accettati: Tunnel, Waves, Rallye, Smoke, Monochrome, Lights, Bees, Lights10
    outputPath1 = "materials/output/VideoProcessing/FrameInterpolation/InterpolatedVideo.avi"  
    outputPath2 = "materials/output/VideoProcessing/VideoUpscaling/InterpolatedVideo-Upscaled.avi"

    # # # Se si vuole impostare un path manualmente: 
    # #input_video_path = "materials/input/stockVideos/"

    # #Parametri
    # zoom_factor = 1.5  # fattore di upscaling desiderato
    # iterazioniUpscaling = 1 # numero di volte in cui viene eseguito l'upscaling sullo stesso frame
    # numInterpolateFrames = 10 #numero di frame da interpolare per ogni coppia di frame
    # #upscaling finale = zoom_factor elevato** iterazioniUpscaling

    # # Filtri applicati durante l'upscaling (se filtro = None non viene applicato)
    # filtersValues, increaseContrast = SelectFilters("Lights10")     #Valori accettati:  Bees, Bees360p, Lights10, None

    # # # Configurazione filtri manuale: 
    # # filtersValues = {
    # #                 "blur_k_dim": 5,
    # #                 "blur_sigma_x": 1,
    # #                 "sharp_k_center": 7,
    # #                 "Laplacian_k_size": 3,
    # #                 "threshold_value": 9,
    # #                 "blur_k_dim_2": 5,
    # #                 "blur_sigma_x_2": 1
    # #             }
    # # increaseContrast = {
    # #     "alpha": ,
    # #     "beta": 
    # # }

    # # # se si vuole disabilitare manualmente i filtri:
    # # filtersValues = None
    increaseContrast = None


    #frame interpolation
    print("Starting Frame Interpolation...")
    frameInterpolation(selected_video, outputPath1, numInterpolateFrames, updateProgress1)     #fps finali = numInterpolateFrames * (numFramesIniziale - 1)
    print("Final Video There:" + outputPath1)
    print("Press Enter to continue...")

    # # Attendi fino a quando viene premuto "Enter"
    # while True:
    #     if msvcrt.kbhit():
    #         key = msvcrt.getch()
    #         if key == b'\r':
    #             break

    #Upscaling
    print("Starting Upscaling...")
    video_upscaling(outputPath1, outputPath2, zoom_factor, iterazioniUpscaling, filtersValues, increaseContrast, updateProgress2)
    print("New Video There:" + outputPath2)
    print("End of System")
