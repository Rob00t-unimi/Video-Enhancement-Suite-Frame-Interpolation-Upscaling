import tkinter as tk
from ttkthemes import ThemedStyle
from ttkbootstrap import Style
import json
from tkinter import filedialog
import cv2
from demo import start
import time
from tkinter import ttk
import webbrowser


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
    "blur_k_dim_2": 5,
    "blur_sigma_x_2": 0.5,
    "showEdges": False
}
interpolationFirst = True

# Carica i dati dal file JSON
with open('filtriPredefiniti.json', 'r') as json_file:
    data = json.load(json_file)

filters = data

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

    demo_window = tk.Toplevel(root)
    demo_window.title("Esecuzione Demo")

    frame_label1 = tk.Label(demo_window, text="Interpolazione di frame", font=("Arial", 12))
    frame_label1.grid(row=0, column=0, padx=10, pady=5)

    # Creazione di una barra di avanzamento determinata per la prima percentuale
    progress1 = ttk.Progressbar(demo_window, length=200, mode="determinate")
    progress1.grid(row=1, column=0, padx=10, pady=5)

    current_label1 = tk.Label(demo_window, text="", padx=10)
    current_label1.grid(row=2, column=0)

    frame_label2 = tk.Label(demo_window, text="Upscaling", font=("Arial", 12))
    frame_label2.grid(row=3, column=0, padx=10, pady=5)

    # Creazione di una barra di avanzamento determinata per la seconda percentuale
    progress2 = ttk.Progressbar(demo_window, length=200, mode="determinate")
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
            progress2.start()


    def on_progress2_completion():
        progress2.grid_forget()
        frame_label2.config(text="Upscaling completato", font=("Arial", 12))
        if interpolationFirst is not True: 
            progress1.start()

    def start_processing():
        try:
            start(selected_video, iterations, numFrameInterpol, zoom_factor, selectedfilter, updateProgress1, updateProgress2, interpolationFirst)
            print("Elaborazione completata. Il video è stato salvato.")
            time.sleep(3)
            demo_window.destroy()
        except Exception as e:
            print(f"Errore durante l'elaborazione del video: {str(e)}")
            time.sleep(3)
            progress1.stop()  # Ferma la barra di avanzamento in caso di errore
            progress2.stop()

    processing_thread = threading.Thread(target=start_processing)
    processing_thread.daemon = True
    processing_thread.start()

    if interpolationFirst: 
        progress1.start()
    else:
        progress2.start()
        

###########################################################################################     Funzioni Elementi Grafici

def select_video():
    global selected_video, preview_image
    file_path = filedialog.askopenfilename(filetypes=[("Video files", "*.mp4 *.avi *.mkv")])
    if file_path:
        selected_video = file_path
        selected_video_label.config(text=f"Video selezionato: {selected_video}")
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
                preview_label.image = preview_image
            cap.release()
            
def cv2_to_tkinter_photoimage(cv2_image, width, height):
    from PIL import Image, ImageTk
    cv2_image = cv2.cvtColor(cv2_image, cv2.COLOR_BGR2RGB)
    pil_image = Image.fromarray(cv2_image)
    new_width = 300
    new_height = int(height*new_width/width)
    print(new_width, new_height)
    pil_image = pil_image.resize((new_height, new_width), Image.BILINEAR)
    
    return ImageTk.PhotoImage(pil_image)

# Inizializza l'anteprima dell'immagine come None
preview_image = None

def update_zoom_factor(value):
    global zoom_factor
    zoom_factor = float(value)
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
            resolution_label.config(text=f"Risoluzione video: {initial_width}x{initial_height}\nRisoluzione dopo upscaling: {final_width}x{final_height}")
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
            fps_label.config(text=f"FPS iniziali: {fps:.2f}\nFPS finali: {finalFps:.2f}")
            cap.release()

def selectFilterType():
    if radio_value.get() == 0:  # Select a preset filter
        params_frame.pack_forget()
        preset_filter_menu.pack()
        
    else:
        preset_filter_menu.pack_forget()
        global selectedfilter
        selectedfilter = filters["Default"].copy()
        params_frame.pack()
       

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
    webbrowser.open("documentation.html")

############################################################################################    Stile
# Carica gli stili dal file JSON
with open('style.json', 'r') as styles_file:
    css_styles = json.load(styles_file)

def apply_css_style(widget, style):
    if style in css_styles:
        for prop, value in css_styles[style].items():
            widget.configure(**{prop: value})

root = tk.Tk()
root.geometry("1500x1100")  # Imposta la larghezza a 720 pixel e l'altezza a 1080 pixel
#root.state('zoomed')

style = ThemedStyle(root)
style = Style(theme="superhero")

main_frame = tk.Frame(root)
apply_css_style(main_frame, "main-div")
main_frame.pack(fill="both", expand=True)

############################################################################################    Grafica

# Calculate heights based on percentages of the total window height
total_height = root.winfo_screenheight()  # Get the screen height

title_height = (total_height * 7) // 100
container_height = (total_height * 40) // 100
sliders_height = (total_height * 7) // 100
radio_buttons_height = (total_height * 14) // 100
parameters_height = (total_height * 10) // 100
start_button_height = (total_height * 7) // 100

# Define frames with calculated heights
title_frame = tk.Frame(main_frame, height=title_height)
apply_css_style(title_frame, "title-div")
title_frame.pack(fill="x")
title_label = tk.Label(title_frame, text="Video Frame Interpolation and Upscaling", font=("Arial", 24))
title_label.pack()

container_frame = tk.Frame(main_frame, height=container_height)
apply_css_style(container_frame, "container-div")
container_frame.pack(fill="both", expand=True)

video_selector_frame = tk.Frame(container_frame)
apply_css_style(video_selector_frame, "video-selector-div")
video_selector_frame.pack(side="left", fill="both", expand=True)

Order_bool = tk.BooleanVar()
Order_bool.set(interpolationFirst)
Order_bool_btn = tk.Checkbutton(video_selector_frame, text="Interpolation First", variable=Order_bool, command=lambda: change_order(Order_bool.get()), font=("Arial", 15))
Order_bool_btn.pack(side="top", fill="both", expand=True)

select_video_button = tk.Button(video_selector_frame, text="Seleziona Video", font=("Arial", 18), command=select_video)
select_video_button.pack()

resolution_label = tk.Label(video_selector_frame, text="")
resolution_label.pack(padx=10, pady=20)

fps_label = tk.Label(video_selector_frame, text="")
fps_label.pack(padx=10, pady=5)

spacer_frame2 = tk.Frame(video_selector_frame)
spacer_frame2.pack(side="top", fill="both", expand=True)

video_preview_frame = tk.Frame(container_frame)
apply_css_style(video_preview_frame, "video-preview-div")
video_preview_frame.pack(side="right", fill="both", expand=True, padx=0, pady=0)


selected_video_label = tk.Label(video_preview_frame, text="Nessun Video Selezionato", font=("Arial", 12))
selected_video_label.pack(side="top", fill="both", expand=True)

preview_label = tk.Label(video_preview_frame, image=preview_image)
preview_label.pack(fill="both", expand=True)

spacer_frame3 = tk.Frame(video_preview_frame)
spacer_frame3.pack(side="top", fill="both", expand=True)

sliders_frame = tk.Frame(main_frame, height=sliders_height)
apply_css_style(sliders_frame, "sliders-div")
sliders_frame.pack(fill="x")

slider1 = tk.Frame(sliders_frame)
apply_css_style(slider1, "slider")
slider1.pack(side="left", fill="both", expand=True)
zoom_label = tk.Label(slider1, text=f"Seleziona upscaling zoom factor: {zoom_factor:.2f}x", font=("Arial", 15))
zoom_label.pack()
zoom_scale = tk.Scale(slider1, from_=1.0, to=10.0, length=300, orient="horizontal", command=update_zoom_factor)
zoom_scale.set(zoom_factor)
zoom_scale.pack()

slider2 = tk.Frame(sliders_frame)
apply_css_style(slider2, "slider")
slider2.pack(side="left", fill="both", expand=True)
iterations_label = tk.Label(slider2, text=f"Seleziona il numero di iterazioni di upscaling: {iterations}", font=("Arial", 15))
iterations_label.pack()
iterations_scale = tk.Scale(slider2, from_=1, to=10, length=300, orient="horizontal", command=update_iterations)
iterations_scale.set(iterations)
iterations_scale.pack()

slider3 = tk.Frame(sliders_frame)
apply_css_style(slider3, "slider")
slider3.pack(side="left", fill="both", expand=True)
numFrame_label = tk.Label(slider3, text=f"Seleziona il numero di frame da interpolare: {numFrameInterpol}", font=("Arial", 15))
numFrame_label.pack()
numFrame_scale = tk.Scale(slider3, from_=1, to=15, length=300, orient="horizontal", command=update_numFrameInterpol)
numFrame_scale.set(numFrameInterpol)
numFrame_scale.pack()  

radio_buttons_frame = tk.Frame(main_frame, height=radio_buttons_height)
apply_css_style(radio_buttons_frame, "radio-buttons-div")
radio_buttons_frame.pack(fill="x")

# Create the label and radio buttons
radio_label = tk.Label(radio_buttons_frame, text="Seleziona tipo di filtro", font=("Arial", 18))
radio_label.pack()

# Create a container frame for the radio buttons with padding
radio_buttons_container = tk.Frame(radio_buttons_frame)
apply_css_style(radio_buttons_container, "radio-buttons-container")
radio_buttons_container.pack(padx=10, pady=10)

radio_value = tk.IntVar()
radio_value.set(0)

radio_preset = tk.Radiobutton(radio_buttons_container, text="Seleziona un filtro preimpostato", variable=radio_value, value=0, command=selectFilterType)
radio_preset.pack(side="left", padx=20)

radio_customize = tk.Radiobutton(radio_buttons_container, text="Personalizza Filtro", variable=radio_value, value=1, command=selectFilterType)
radio_customize.pack(side="left")

parameters_frame = tk.Frame(main_frame, height=parameters_height)
apply_css_style(parameters_frame, "parameters-div")
parameters_frame.pack(fill="both", expand=True)

boolean_var = tk.BooleanVar()
boolean_var.set(selectedfilter["showEdges"])
boolean_checkbutton = tk.Checkbutton(parameters_frame, text="Show Edges", variable=boolean_var, command=lambda: update_input_value("showEdges", boolean_var.get()))
boolean_checkbutton.pack(padx=10, pady=15)

filter_selection = tk.StringVar()
filter_selection.set("Default")
filter_selection.trace_add("write", on_filter_selection_change)
preset_filters = list(filters.keys())
preset_filter_menu = ttk.Combobox(parameters_frame, textvariable=filter_selection, values=preset_filters)
preset_filter_menu.pack()

params_frame = tk.Frame(parameters_frame)
apply_css_style(params_frame, "inner-div")
params_frame.pack_forget()

input_values = {key: tk.StringVar(value=str(selectedfilter[key])) for key in selectedfilter}

min_value = 0
max_value = 10
step = 0.1

keys = ["blur_k_dim", "blur_sigma_x", "sharp_k_center", "Laplacian_k_size", "threshold_value", "blur_k_dim_2", "blur_sigma_x_2"]
labels = ["Dimensione kernel primo blurring", "Sigma primo blurring", "Dimensione del kernel di sharpening", "Dimensione del kernel laplaciano (edge detector)", "Soglia di binarizzazione", "Dimensione del kernel secondo blurring", "Sigma secondo blurring"]

def create_spinbox(key, row):
    label = ttk.Label(params_frame, text=labels[row-1])
    label.grid(row=row, column=0, pady=5, sticky="w")
    spinbox = ttk.Spinbox(params_frame, textvariable=input_values[key], from_=min_value, to=max_value, increment=step)
    spinbox.grid(row=row, column=1, pady=5, padx=20, sticky="w")
    spinbox.bind("<FocusOut>", lambda event, k=key: update_input_value(k, spinbox.get()))

for i, key in enumerate(keys):
    create_spinbox(key, i + 1)

start_button_frame = tk.Frame(main_frame, height=start_button_height)
apply_css_style(start_button_frame, "start-button-div")
start_button_frame.pack(fill="x")
start_button = tk.Button(start_button_frame, text="Conferma e Inizia", command=confirm, font=("Arial", 18))
start_button.grid(row=0, column=1, padx=10, pady=10)
start_button_frame.columnconfigure(2, weight=1)

show_doc_button = tk.Button(start_button_frame, text="Info", command=show_documentation, font=("Arial", 14))
show_doc_button.grid(row=0, column=3, padx=0, pady=10)

label1 = tk.Label(start_button_frame)
label1.grid(row=0, column=0, padx=10, pady=10)
start_button_frame.columnconfigure(0, weight=2)

label3 = tk.Label(start_button_frame)
label1.grid(row=0, column=0, padx=10, pady=10)
start_button_frame.columnconfigure(2, weight=2)

# Update the style in style.json
with open('style.json', 'r') as styles_file:
    css_styles = json.load(styles_file)

css_styles['show-doc-button-style'] = {
    "background": "lightgray",  # Change to the desired background color
    "font": "Arial 15",
    "foreground": "blue"  # Text color
}

# Apply the updated style to the button
show_doc_button_style = "show-doc-button-style"  # Use the updated style name
apply_css_style(show_doc_button, show_doc_button_style)


root.mainloop()