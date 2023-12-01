import cv2
import numpy as np
import os

def taglia_e_salva_video(input_path, output_path, inizio, durata):
    # Apri il video originale
    cap = cv2.VideoCapture(input_path)

    # Ottieni le informazioni sul video
    fps = cap.get(cv2.CAP_PROP_FPS)
    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    # Calcola il numero totale di frame da leggere
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    # Calcola i frame di inizio e fine per il taglio
    start_frame = int(inizio * fps)
    end_frame = int((inizio + durata) * fps)

    # Assicurati che end_frame non superi il numero totale di frame
    end_frame = min(end_frame, total_frames - 1)

    # Imposta il video writer
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_path, fourcc, fps, (frame_width, frame_height))

    # Vai al frame di inizio
    cap.set(cv2.CAP_PROP_POS_FRAMES, start_frame)

    # Leggi e scrivi i frame nel nuovo video
    for frame_num in range(start_frame, end_frame + 1):
        ret, frame = cap.read()
        if not ret:
            break
        out.write(frame)

    # Rilascia le risorse
    cap.release()
    out.release()

# Specifica il percorso del video originale
video_originale_path = r"C:\Users\rober\Desktop\progetto-principi\materials\input\stockVideos\the dark knight - dark on dark\cutted.mp4"

cartella_path = os.path.dirname(video_originale_path)

# Specifica il percorso e il nome del video tagliato
video_tagliato_path = cartella_path + "\cut.mp4"

# Specifica il punto di inizio e la durata del taglio
inizio_taglio = 0  # secondi
durata_taglio = 10.0  # secondi

# Esegui la funzione per tagliare e salvare il video
taglia_e_salva_video(video_originale_path, video_tagliato_path, inizio_taglio, durata_taglio)
