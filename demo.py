from videoFrameInterpolation import frameInterpolation
from videoFrameUpscaling import video_upscaling
import json
import os
from moviepy.editor import VideoFileClip, clips_array, vfx


def videoViewer(video_path1, video_path2):

    # Carica i video
    clip1 = VideoFileClip(video_path1)
    clip2 = VideoFileClip(video_path2)

    clip1_resized = clip1.resize(width=clip1.size[0]/2.5, height=clip1.size[1]/2.5)
    clip2_resized = clip2.resize(width=clip2.size[0]/2.5, height=clip2.size[1]/2.5)
    
    final_clip = clips_array([[clip1_resized, clip2_resized]])
    final_clip.preview()
    final_clip.close()

    clip1_slow = clip1.fx(vfx.speedx, 0.5)
    clip2_slow = clip2.fx(vfx.speedx, 0.5)
    clip1_slow_resized = clip1_slow.resize(width=clip1_slow.size[0]/2.5, height=clip1_slow.size[1]/2.5)
    clip2_slow_resized = clip2_slow.resize(width=clip2_slow.size[0]/2.5, height=clip2_slow.size[1]/2.5)

    final_clip = clips_array([[clip1_slow_resized, clip2_slow_resized]])
    final_clip.preview()
    final_clip.close()


# Per una questione computazionale inverto le operazioni, prima interpolo il frame rate e poi faccio upscaling

def start(selected_video, iterazioniUpscaling, numInterpolateFrames, zoom_factor, filtersValues, updateProgress1, updateProgress2, interpolationFirst): 

    n = 0
    # dir = os.path.dirname(selected_video) 

    with open('JSON/outputPath.json', 'r') as json_file:
        data = json.load(json_file)
        dir = os.path.dirname(data["dir"])  

    while True:
        # Generate file paths
        outputPath1 = os.path.join(dir, f"InterpolatedVideo{n}.mp4")
        outputPath2 = os.path.join(dir, f"InterpolatedVideo-Upscaled{n}.mp4")
        outputPath3 = os.path.join(dir, f"UpscaledVideo{n}.mp4")
        outputPath4 = os.path.join(dir, f"UpscaledVideo-Interpolated{n}.mp4")

        # Check if any of the files already exist
        if not (
            os.path.exists(outputPath1)
            or os.path.exists(outputPath2)
            or os.path.exists(outputPath3)
            or os.path.exists(outputPath4)
        ):
            break

        # If any file exists, increment n and try again
        n += 1
    
    outputPath1 = os.path.join(dir, f"InterpolatedVideo{n}.mp4")
    outputPath2 = os.path.join(dir, f"InterpolatedVideo-Upscaled{n}.mp4")
    outputPath3 = os.path.join(dir, f"UpscaledVideo{n}.mp4")
    outputPath4 = os.path.join(dir, f"UpscaledVideo-Interpolated{n}.mp4")
    

# # path selection by JSON
#     with open('JSON/outputPath.json', 'r') as json_file:
#         data = json.load(json_file)
#         global outputPath1, outputPath3, outputPath4, outputPath5
#         outputPath1 = data["outputpath1"]
#         outputPath2 = data["outputPath2"]
#         outputPath3 = data["outputPath3"]
#         outputPath4 = data["outputPath4"]

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

    def start_frame_interpolation(input_path, output_path, numInterpolateFrames, updateProgress1, filtersValues):
        print("Starting Frame Interpolation...")
        frameInterpolation(input_path, output_path, numInterpolateFrames, updateProgress1, filtersValues)
        print("Final Video There:" + output_path)

    def start_upscaling(input_path, output_path, iterazioniUpscaling, zoom_factor, filtersValues, updateProgress2):
        print("Starting Upscaling...")
        video_upscaling(input_path, output_path, zoom_factor, iterazioniUpscaling, filtersValues, increaseContrast, updateProgress2)
        print("New Video There:" + output_path)

    if interpolationFirst:
        start_frame_interpolation(selected_video, outputPath1, numInterpolateFrames, updateProgress1, filtersValues)
        # os.startfile(outputPath1)
        start_upscaling(outputPath1, outputPath2, iterazioniUpscaling, zoom_factor, filtersValues, updateProgress2)
        # os.startfile(outputPath2)
        videoViewer(selected_video,outputPath2)
    else:
        start_upscaling(selected_video, outputPath3,iterazioniUpscaling, zoom_factor, filtersValues, updateProgress2)
        # os.startfile(outputPath3)
        start_frame_interpolation(outputPath3, outputPath4, numInterpolateFrames, updateProgress1, filtersValues)
        # os.startfile(outputPath4)
        videoViewer(selected_video,outputPath4)
    print("End of System")


