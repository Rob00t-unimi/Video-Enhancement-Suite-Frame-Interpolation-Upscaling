import tkinter as tk
from ttkthemes import ThemedStyle
from ttkbootstrap import Style
import json
from tkinter import filedialog
import cv2
from demo import start
import time
import webbrowser
import locale
import os
import platform
import ttkbootstrap as ttk
from ttkbootstrap.constants import *


############################################################################################    Variabili Globali

selected_video = ""
iterations = 1
numFrameInterpol = 3
zoom_factor = 1.5
selectedfilter = {
    "blur_k_dim": 5,
    "blur_sigma_x": 1,
    "sharp_k_center": 7,
    "Laplacian_k_size": 3,
    "threshold_value": 30,
    "blur_k_dim_2": 3,
    "showEdges": False
}
interpolationFirst = False

# Carica i dati dal file JSON
with open('JSON/filtriPredefiniti.json', 'r') as json_file:
    data = json.load(json_file)

filters = data

current_file_path = os.path.abspath(__file__)
directory_path = os.path.dirname(current_file_path)

with open('JSON/outputPath.json', 'r') as json_file:
    data = json.load(json_file)
    outputPath1 = directory_path + "/" + data["outputpath1"]
    outputPath2 = directory_path + "/" + data["outputPath2"]
    outputPath3 = directory_path + "/" + data["outputPath3"]
    outputPath4 = directory_path + "/" + data["outputPath4"]

############################################################################################    Controllo Multithread

# Funzione per controllare le variabili e stamparle quando cambiano
def monitor_variables():
    global selected_video, iterations, numFrameInterpol, zoom_factor, selectedfilter, interpolationFirst
    pre_selected_video, pre_iterations, pre_numFrameInterpol, pre_zoom_factor, pre_selectedfilter, pre_interpolationFirst = selected_video, iterations, numFrameInterpol, zoom_factor, selectedfilter, interpolationFirst
    while True:
        # Controlla se le variabili sono cambiate
        if selected_video != pre_selected_video:
            print(f"selected_video: {selected_video}")
        if iterations != pre_iterations:
            print(f"iterations: {iterations}")
        if numFrameInterpol != pre_numFrameInterpol:
            print(f"numFrameInterpol: {numFrameInterpol}")
        if zoom_factor != pre_zoom_factor:
            print(f"zoom_factor: {zoom_factor}")
        if interpolationFirst != pre_interpolationFirst:
            print(f"interpolationFirst: {interpolationFirst}")
        if selectedfilter != pre_selectedfilter:
            print("selectedfilter:")
            for key, value in selectedfilter.items():
                print(f"  {key}: {value}")
        pre_selected_video, pre_iterations, pre_numFrameInterpol, pre_zoom_factor, pre_selectedfilter, pre_interpolationFirst = selected_video, iterations, numFrameInterpol, zoom_factor, selectedfilter, interpolationFirst
        # Aggiorna il controllo ogni tot secondi (ad esempio, ogni 1 secondo)
        time.sleep(0.5)

# Avvia la funzione di monitoraggio in un thread separato
import threading
monitor_thread = threading.Thread(target=monitor_variables)
monitor_thread.daemon = True
monitor_thread.start()

############################################################################################    Funzioni principali

def confirm():
    global selected_video, iterations, numFrameInterpol, zoom_factor, selectedfilter, interpolationFirst
    global demo_window

    elaborated1 = 0
    total1 = None
    elaborated2 = 0
    total2 = None
    percentuale1 = 0.00
    percentuale2 = 0.00

    if not selected_video:
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
        if interpolationFirst: 
            if platform.system() == "Windows":
                global outputPath1
                os.startfile(outputPath1)
        else:
            if platform.system() == "Windows":
                global outputPath4
                os.startfile(outputPath4)


    def on_progress2_completion():
        progress2.grid_forget()
        frame_label2.config(text="Upscaling completato", font=("Arial", 12))
        if interpolationFirst: 
            if platform.system() == "Windows":
                global outputPath2
                os.startfile(outputPath2)
        else:
            if platform.system() == "Windows":
                global outputPath3
                os.startfile(outputPath3)


    def start_processing():
        try:
            start(selected_video, iterations, numFrameInterpol, zoom_factor, selectedfilter, updateProgress1, updateProgress2, interpolationFirst)
            print("Elaborazione completata. Il video è stato salvato.")
            time.sleep(3)
            demo_window.destroy()
        except Exception as e:
            print(f"Errore durante l'elaborazione del video: {str(e)}")
            time.sleep(1)


    processing_thread = threading.Thread(target=start_processing)
    processing_thread.daemon = True
    processing_thread.start()
            
    # def on_closing():
    #     if processing_thread.is_alive():
    #         processing_thread.join()  
    #         print("Thread interrotto.")
    #     demo_window.destroy()

    # demo_window.protocol("WM_DELETE_WINDOW", on_closing)

###########################################################################################     Funzioni Elementi Grafici

def select_video():
    global selected_video, preview_image
    file_path = filedialog.askopenfilename(filetypes=[("Video files", "*.mp4 *.avi *.mkv")])
    if file_path:
        selected_video = file_path
        selected_video_label.config(text=f"Video selezionato: {selected_video}", wraplength=300, anchor="nw", justify="right")

        update_resolution_info()
        update_fps_info()
        
        # Leggi il primo frame del video per l'anteprima
        cap = cv2.VideoCapture(selected_video)
        if cap.isOpened():
            ret, frame = cap.read()
            if ret:
                frame_width, frame_height, _ = frame.shape
                # Converte il frame in un formato Tkinter PhotoImage con le dimensioni desiderate
                preview_image = cv2_to_tkinter_photoimage(frame, width=frame_width, height=frame_height)
                # Visualizza l'anteprima dell'immagine
                preview_label.config(image=preview_image)
                preview_label.configure(background=None)
                preview_label.image = preview_image
            cap.release()
            
def cv2_to_tkinter_photoimage(cv2_image, width, height):
    from PIL import Image, ImageTk
    cv2_image = cv2.cvtColor(cv2_image, cv2.COLOR_BGR2RGB)
    pil_image = Image.fromarray(cv2_image)
    new_width = 365
    new_height = int(height*new_width/width)
    print(new_width, new_height)
    pil_image = pil_image.resize((new_height, new_width), Image.BILINEAR)
    
    return ImageTk.PhotoImage(pil_image)

# Inizializza l'anteprima dell'immagine come None
preview_image = None
locale.setlocale(locale.LC_ALL, 'en_US')

def update_zoom_factor(value):
    global zoom_factor
    zoom_factor = float(locale.atof(value))
    update_resolution_info()
    zoom_label.config(text=f"Seleziona upscaling zoom factor: {zoom_factor:.2f}x")

def update_iterations(value):
    global iterations
    iterations = round(float(value))
    update_resolution_info()
    iterations_label.config(text=f"Seleziona il numero di iterazioni: {iterations}")

def update_resolution_info():
    if selected_video:
        cap = cv2.VideoCapture(selected_video)
        if cap.isOpened():
            initial_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            initial_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
            final_upscaling = zoom_factor ** iterations
            final_width = int(initial_width * final_upscaling)
            final_height = int(initial_height * final_upscaling)
            resolution_label.config(text=f"Risoluzione video: {initial_width}x{initial_height}\nRisoluzione dopo upscaling: {final_width}x{final_height}", justify="left")
            cap.release()

def update_numFrameInterpol(value):
    global numFrameInterpol
    numFrameInterpol = round(float(value))
    update_fps_info()
    numFrame_label.config(text=f"Seleziona il numero di frame interpolati: {numFrameInterpol}")
def update_fps_info():
    if selected_video:
        cap = cv2.VideoCapture(selected_video)
        if cap is not None and cap.isOpened():
            frame_count = cap.get(cv2.CAP_PROP_FRAME_COUNT)
            fps = cap.get(cv2.CAP_PROP_FPS)
            originalSeconds = frame_count / fps
            tot_finalFrames = numFrameInterpol * (frame_count - 1)
            finalFps = tot_finalFrames / originalSeconds
            fps_label.config(text=f"FPS iniziali: {fps:.2f}\nFPS finali: {finalFps:.2f}", justify="left")
            cap.release()

def selectFilterType():
    if radio_value.get() == 0:  # Select a preset filter
        params_frame.grid_forget()
        preset_filter_menu.grid(column=1, row=0, sticky="E", padx=25)  
        
    else:
        preset_filter_menu.grid_forget()
        global selectedfilter
        # selectedfilter = filters["Default"].copy()
        updateView()
        params_frame.grid(columnspan=2, padx=30, sticky="we")
       

def on_filter_selection_change(*args):
    global selectedfilter
    selected_filter_name = filter_selection.get()
    print(selected_filter_name)
    selectedfilter = filters[selected_filter_name].copy()

def update_input_value(key, value):
    global selectedfilter 
    tmp = selectedfilter.copy()
    tmp[key] = value
    selectedfilter = tmp.copy()

def change_order(value):
    global interpolationFirst
    interpolationFirst = value


def show_documentation():
    webbrowser.open("documentation\documentation.html")

############################################################################################    Graphics elements

window = tk.Tk()
window.geometry("1280x720")
window.title("Frame interpolation and Upscaling")

window.grid_rowconfigure(1, weight=1)
window.grid_columnconfigure(0, weight=1)

style = ThemedStyle(window)
style = Style(theme="darkly")

# CONTAINERS

container = tk.Frame(window)
container.grid(column=0, row=1, sticky="nsew")
container.grid_columnconfigure(0, weight=1)  # Prima colonna
container.grid_columnconfigure(1, weight=2)  # Seconda colonna
container.grid_columnconfigure(2, weight=5)  # Terza colonna
container.grid_rowconfigure(0, weight=1)

title_frame = tk.Frame(window, borderwidth=1, relief="solid")
title_frame.grid(column=0, row=0, sticky="we")
title_frame.grid_columnconfigure(0, weight=1)

col1 = tk.Frame(container, borderwidth=1, relief="solid")
col1.grid(column=0, row=0, sticky="nsew")  
col1.grid_columnconfigure(0, weight=1) 

col2 = tk.Frame(container, borderwidth=1, relief="solid")
col2.grid(column=1, row=0, sticky="nsew")
col2.grid_columnconfigure(0, weight=1) 

col3 = tk.Frame(container, borderwidth=1, relief="solid")
col3.grid(column=2, row=0, sticky="nsew")
col3.grid_rowconfigure(0, weight=2)
col3.grid_rowconfigure(1, weight=2)
col3.grid_columnconfigure(0, weight=1) 

row3 = tk.Frame(container, borderwidth=1, relief="solid")
row3.grid(column=0, row=4, sticky="we", columnspan=3)
row3.grid_columnconfigure(0, weight=1)

buttonFrame = tk.Frame(row3)
buttonFrame.grid(row=0, column=0, padx=10, pady=10, sticky="E") 

# TITLE
titleLabel = tk.Label(title_frame, text="Video Frame Interpolation and Upscaling", font=("Helvetica", 16, "bold"))
titleLabel.grid(padx=10, pady=10)

# COL 1
Order_bool = tk.BooleanVar()
Order_bool.set(interpolationFirst)
orderCheckSelection = ttk.Checkbutton(col1, text="Interpolation First", variable=Order_bool, command=lambda: change_order(Order_bool.get()), bootstyle="round-toggle")
orderCheckSelection.grid( sticky="W", padx=20, pady=20)

boolean_var = tk.BooleanVar()
boolean_var.set(selectedfilter["showEdges"])
boolean_checkbutton = ttk.Checkbutton(col1, text="Show Edges", variable=boolean_var, command=lambda: update_input_value("showEdges", boolean_var.get()), bootstyle="round-toggle")
boolean_checkbutton.grid( sticky="W", padx=20)

radio_label = tk.Label(col1, text="Seleziona tipo di filtro", font=("Helvetica", 12, "bold"))
radio_label.grid( sticky="W", padx=17, pady=(30, 20))

radio_value = tk.IntVar()
radio_value.set(0)
filterRadioSelection = tk.Radiobutton(col1, text="Filtri predefiniti", variable=radio_value, value=0, command=selectFilterType, font=("Helvetica", 12))
filterRadioSelection.grid( sticky="W", padx=30 )

filterRadioSelection = tk.Radiobutton(col1, text="Filtri personalizzati", variable=radio_value, value=1, command=selectFilterType, font=("Helvetica", 12))
filterRadioSelection.grid( sticky="W", padx=30 )

# COL 2

frame1 = tk.Frame(col2, padx=20, pady=20)
frame1.grid(row=0, column=0, sticky='we')
frame1.columnconfigure(0, weight=1)

zoom_label = tk.Label(frame1, text=f"Seleziona upscaling zoom factor: {zoom_factor:.2f}x", font=("Helvetica", 12), anchor="w")
zoom_label.grid(columnspan=2, sticky='W')

zoom_scale = tk.Scale(frame1, from_=1.0, to=10.0, resolution=0.5, orient="horizontal", command=update_zoom_factor)
zoom_scale.set(zoom_factor)
zoom_scale.grid(columnspan=2, sticky='we', padx=20, pady=5)

frame2 = tk.Frame(col2, padx=20)
frame2.grid(row=1, column=0, sticky='we')
frame2.columnconfigure(0, weight=1)

iterations_label = tk.Label(frame2, text=f"Seleziona il numero di iterazioni di upscaling: {iterations}", font=("Helvetica", 12), anchor="w")
iterations_label.grid(columnspan=2, sticky='W')

iterations_scale = tk.Scale(frame2, from_=1, to=10, orient="horizontal", command=update_iterations)
iterations_scale.set(iterations)
iterations_scale.grid(columnspan=2, sticky='we', padx=20, pady=5)

frame3 = tk.Frame(col2, padx=20, pady=20)
frame3.grid(row=2, column=0, sticky='we')
frame3.columnconfigure(0, weight=1)

numFrame_label = tk.Label(frame3, text=f"Seleziona il numero di frame da interpolare: {numFrameInterpol}", font=("Helvetica", 12), anchor="w")
numFrame_label.grid(columnspan=2, sticky='W')

numFrame_scale = tk.Scale(frame3, from_=1, to=15, orient="horizontal", command=update_numFrameInterpol)
numFrame_scale.set(numFrameInterpol)
numFrame_scale.grid(columnspan=2, sticky='we', padx=20, pady=5)

frame4 = tk.Frame(col2, padx=20, pady=20)
frame4.grid(row=3, column=0, sticky='we')
  
filterLabel = tk.Label(frame4, text="Filter:", font=("Helvetica", 12, "bold"))
filterLabel.grid(column=0, row=0, pady=15, sticky="W")

filter_selection = tk.StringVar()
filter_selection.set("Default")
filter_selection.trace_add("write", on_filter_selection_change)
preset_filters = list(filters.keys())
preset_filter_menu = ttk.Combobox(frame4, textvariable=filter_selection, values=preset_filters)
preset_filter_menu.grid(column=1, row=0, sticky="E", padx=25)  

# PARAMS
params_frame = tk.Frame(col2)
params_frame.grid(columnspan=2, padx=30, sticky="we")  
params_frame.grid_forget() 


min_value = 0
max_value = 10
step = 0.1

keys = ["blur_k_dim", "blur_sigma_x", "sharp_k_center", "Laplacian_k_size", "threshold_value", "blur_k_dim_2"]
labels = ["Dimensione del kernel id blurring", "Sigma di blurring", "Dimensione del kernel di sharpening", "Dimensione del kernel laplaciano (edge detector)", "Soglia di binarizzazione", "Dimensione del kernel di Denoising"]

input_values = {key: tk.StringVar(value=str(selectedfilter[key])) for key in selectedfilter}

def updateView():
    global input_values
    input_values = {key: tk.StringVar(value=str(selectedfilter[key])) for key in selectedfilter}
    for i, key in enumerate(keys):
        create_spinbox(key, i + 1)

def create_spinbox(key, row):
    label = ttk.Label(params_frame, text=labels[row-1])
    label.grid(row=row, column=0, pady=5, sticky="w")
    spinbox = ttk.Spinbox(params_frame, textvariable=input_values[key], from_=min_value, to=max_value, increment=step)
    spinbox.grid(row=row, column=1, padx=(15, 0), pady=5, sticky="E")
    spinbox.bind("<<Increment>>", lambda event, k=key: update_input_value(k, round(float(spinbox.get())+0.1, 1)))
    spinbox.bind("<<Decrement>>", lambda event, k=key: update_input_value(k, round(float(spinbox.get())-0.1, 1)))
    spinbox.bind("<KeyRelease>", lambda event, k=key: update_input_value(k, float(spinbox.get())))

preview_frame = tk.Frame(col3)
preview_frame.grid(sticky="nsew", padx=20, pady=20)
preview_frame.columnconfigure(0, weight=1)
preview_frame.rowconfigure(0, weight=1)

preview_label = tk.Label(preview_frame, image=preview_image, anchor="center")
preview_label.grid(column=0, row=0, sticky="nsew")
preview_label.configure(background="black")

dettaglioVideo = tk.Frame(col3, borderwidth=1, relief="solid")
dettaglioVideo.grid( sticky="nsew")
dettaglioVideo.columnconfigure(0, weight=1)

select_video_button = ttk.Button(dettaglioVideo, text="Seleziona Video", command=select_video, bootstyle=( LIGHT, OUTLINE))
select_video_button.grid(column=0, row=0, sticky="nw", padx=20, pady=20)

selected_video_label = tk.Label(dettaglioVideo, text="Nessun Video Selezionato", anchor="nw")
selected_video_label.grid(column=1, row=0, padx=20, pady=20, sticky="ne")

resolution_label = tk.Label(dettaglioVideo, text=" ", anchor="w")
resolution_label.grid(column=0, row=1, padx=20, pady=20, sticky="W")

fps_label = tk.Label(dettaglioVideo, text=" ", anchor="w")
fps_label.grid(column=1, row=1, padx=20, pady=20, sticky="W")

# BUTTONS ROW

startButton = ttk.Button(buttonFrame, text="Conferma e Inizia", command=confirm, bootstyle=( PRIMARY ))
startButton.grid(row=0, column=1)   

documentationButton = ttk.Button(buttonFrame, text="Info", bootstyle=(INFO, OUTLINE), command=show_documentation)
documentationButton.grid(row=0, column=0, padx=10)

if __name__ == "__main__":
    window.mainloop()