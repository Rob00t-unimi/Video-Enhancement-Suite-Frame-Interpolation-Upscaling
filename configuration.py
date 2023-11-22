import locale
import os
import platform
import threading
import json
import time
import tkinter as tk
from tkinter import filedialog
import webbrowser
import cv2
from ttkthemes import ThemedStyle
from ttkbootstrap import Style
import ttkbootstrap as ttk

from classes.factors import Factors
import classes.filtersClasses
from classes.paths import Paths
from demo import start
from printObjects import printObjects
from classes.videoInfo import VideoInfo



factors = Factors()
paths = Paths()
selectedFilter = classes.filtersClasses.ActiveFilters()
videoInfo = None
preview_image = None
locale.setlocale(locale.LC_ALL, 'en_US')

printObjects(factors, paths, selectedFilter)

# Carica i dati dal file JSON
with open('JSON/filtriPredefiniti.json', 'r') as json_file:
    data = json.load(json_file)
filters = data

############################################################################################    Funzioni principali

def confirm():
    global demo_window

    elaborated1 = 0
    total1 = None
    elaborated2 = 0
    total2 = None
    percentuale1 = 0.00
    percentuale2 = 0.00

    if not paths._input_video_path:
        print("Errore: Nessun video selezionato")
        return

    demo_window = tk.Toplevel(window)
    demo_window.title("Esecuzione Demo")

    frame_label1 = tk.Label(demo_window, text="Interpolazione di frame", font=("Arial", 12))
    frame_label1.grid(row=0, column=0, padx=10, pady=5)

    # Creazione di una barra di avanzamento determinata per la prima percentuale
    progress1 = ttk.Progressbar(demo_window, length=300, mode="determinate", maximum=100, value=0)
    progress1.grid(row=1, column=0, padx=10, pady=5)

    current_label1 = tk.Label(demo_window, text="", padx=10)
    current_label1.grid(row=2, column=0)

    frame_label2 = tk.Label(demo_window, text="Upscaling", font=("Arial", 12))
    frame_label2.grid(row=3, column=0, padx=10, pady=5)

    # Creazione di una barra di avanzamento determinata per la seconda percentuale
    progress2 = ttk.Progressbar(demo_window, length=300, mode="determinate", maximum=100, value=0)
    progress2.grid(row=4, column=0, padx=10, pady=5)

    current_label2 = tk.Label(demo_window, text="", padx=10)
    current_label2.grid(row=5, column=0)

    # Update Progress Bars
    def updateProgress1(progress, total):
        nonlocal elaborated1, total1, percentuale1
        elaborated1 = progress
        total1 = total
        percentuale1 = elaborated1 / total1 * 100
        progress1["value"] = percentuale1
        current_label1.config(text=f"Frame elaborati: {elaborated1}/{total1} ({percentuale1:.2f}%)")
        if elaborated1 == total1:
            threading.Thread(target=on_progress1_completion).start()

    def updateProgress2(progress, total):
        nonlocal elaborated2, total2, percentuale2
        elaborated2 = progress
        total2 = total
        percentuale2 = elaborated2 / total2 * 100
        progress2["value"] = percentuale2
        current_label2.config(text=f"Frame elaborati: {elaborated2}/{total2} ({percentuale2:.2f}%)")
        if elaborated2 == total2:
            threading.Thread(target=on_progress2_completion).start()

    # Completamento progress bar
    def on_progress1_completion():
        progress1.grid_forget()
        frame_label1.config(text="Interpolazione di frame completata", font=("Arial", 12))
        if factors._interpolationFirst: 
            if platform.system() == "Windows":
                os.startfile(paths._output_path_1)
        else:
            if platform.system() == "Windows":
                os.startfile(paths._output_path_4)


    def on_progress2_completion():
        progress2.grid_forget()
        frame_label2.config(text="Upscaling completato", font=("Arial", 12))
        if factors._interpolationFirst: 
            if platform.system() == "Windows":
                os.startfile(paths._output_path_2)
        else:
            if platform.system() == "Windows":
                os.startfile(paths._output_path_3)


    def start_processing():
        try:
            start(paths._input_video_path, factors._numIterations, factors._numFrameInterpol, factors._zoom_factor, selectedFilter, updateProgress1, updateProgress2, factors._interpolationFirst)
            print("Elaborazione completata. Il video è stato salvato.")
            time.sleep(3)
            demo_window.destroy()
        except Exception as e:
            print(f"Errore durante l'elaborazione del video: {str(e)}")
            time.sleep(1)


    processing_thread = threading.Thread(target=start_processing)
    processing_thread.daemon = True
    processing_thread.start()

    ###########################################################################################     Funzioni Elementi Grafici

def select_video():
    global videoInfo
    file_path = filedialog.askopenfilename(filetypes=[("Video files", "*.mp4 *.avi *.mkv")])
    if file_path:
        paths.set_input_video_path(file_path)
        selected_video_label.config(text=f"Video selezionato: {paths._input_video_path}", wraplength=300, anchor="nw", justify="right")
        videoInfo = VideoInfo(paths._input_video_path)

        update_resolution_info()
        update_fps_info()
        
        if videoInfo.cover is not None:
            preview_image = cv2_to_tkinter_photoimage(videoInfo)
            # Visualizza l'anteprima dell'immagine
            preview_label.config(image=preview_image)
            preview_label.configure(background=None)
            preview_label.image = preview_image
            
def cv2_to_tkinter_photoimage(videoInfo):
    from PIL import Image, ImageTk
    cv2_image = videoInfo.cover
    pil_image = Image.fromarray(cv2_image)
    new_width = 365
    new_height = int(videoInfo.height*new_width/videoInfo.width)
    print(new_width, new_height)
    pil_image = pil_image.resize((new_height, new_width), Image.BILINEAR)
    return ImageTk.PhotoImage(pil_image)

def update_zoom_factor(value):
    factors.set_zoom_factor(float(locale.atof(value)))
    update_resolution_info()
    zoom_label.config(text=f"Seleziona upscaling zoom factor: {factors._zoom_factor:.2f}x")

def update_iterations(value):
    factors.set_numIterations(round(float(value)))
    update_resolution_info()
    iterations_label.config(text=f"Seleziona il numero di iterazioni: {factors._numIterations}")

def update_resolution_info():
    if videoInfo.width is not None and videoInfo.height is not None:
        final_width, final_height = videoInfo.calc_new_shape(factors._zoom_factor, factors._numIterations)
        resolution_label.config(text=f"Risoluzione video: {videoInfo.width}x{videoInfo.height}\nRisoluzione dopo upscaling: {final_width}x{final_height}", justify="left")

def update_numFrameInterpol(value):
    factors.set_numFrameInterpol(round(float(value)))
    update_fps_info()
    numFrame_label.config(text=f"Seleziona il numero di frame interpolati: {factors._numFrameInterpol}")

def update_fps_info():
    if paths._input_video_path:
        if videoInfo.fps is not None:
            finalFps = videoInfo.calc_new_fps(factors._numFrameInterpol)
            fps_label.config(text=f"FPS iniziali: {videoInfo.fps:.2f}\nFPS finali: {finalFps:.2f}", justify="left")

##### ................
# 
#  i am copying main there ...
       

