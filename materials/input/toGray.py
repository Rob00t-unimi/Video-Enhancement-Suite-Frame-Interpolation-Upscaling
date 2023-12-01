import cv2
import imageio

# Funzione per convertire il frame in scala di grigio
def converti_in_scala_di_grigio(frame):
    return cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

# Percorso del video di input
video_input_path = r"C:\Users\rober\Desktop\progetto-principi\materials\input\stockVideos\la haine - zoom in\cut_24fps_10sec_720p.mp4"

# Percorso del video di output in scala di grigio
video_output_path = r"C:\Users\rober\Desktop\progetto-principi\materials\input\stockVideos\la haine - zoom in\2cut_24fps_10sec_720p.mp4"

# Apri il video di input
video_capture = cv2.VideoCapture(video_input_path)

# Ottieni le informazioni del video (larghezza, altezza, frame per secondo, ecc.)
fps = int(video_capture.get(cv2.CAP_PROP_FPS))
frame_size = (int(video_capture.get(cv2.CAP_PROP_FRAME_WIDTH)), int(video_capture.get(cv2.CAP_PROP_FRAME_HEIGHT)))

# Crea un oggetto VideoWriter per il video di output
video_writer = imageio.get_writer(video_output_path, fps=fps, quality=8, codec='libx264')

# Loop attraverso ogni frame del video
while True:
    # Leggi il frame successivo
    ret, frame = video_capture.read()

    # Se il frame è vuoto, esci dal loop
    if not ret:
        break

    # Converti il frame in scala di grigio
    gray_frame = converti_in_scala_di_grigio(frame)

    # Scrivi il frame in scala di grigio nel video di output
    video_writer.append_data(gray_frame)

# Rilascia le risorse
video_capture.release()
video_writer.close()

print("Conversione completata. Video in scala di grigio salvato in:", video_output_path)
