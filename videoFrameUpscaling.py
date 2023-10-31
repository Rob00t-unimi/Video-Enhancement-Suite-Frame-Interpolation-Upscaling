import cv2

def process_video(input_video_path, output_video_path, zoom_factor):
    # Apri il video di input
    cap = cv2.VideoCapture(input_video_path)

    if not cap.isOpened():
        print("Impossibile aprire il video di input.")
        return

    # Leggi le dimensioni del video
    frame_width = int(cap.get(3))
    frame_height = int(cap.get(4))

    # Crea un oggetto VideoWriter per scrivere il video di output
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter(output_video_path, fourcc, 20.0, (frame_width, frame_height))

    frame_num = 0

    while True:
        ret, frame = cap.read()

        if not ret:
            break

        # Applica la tua funzione di upscaling al frame
        upscaled_frame, _, _, _ = bilinear_upscale(frame, zoom_factor, frame_num)

        # Scrivi il frame elaborato nel video di output
        out.write(upscaled_frame)

        frame_num += 1

    # Rilascia le risorse
    cap.release()
    out.release()

    print("Elaborazione del video completata.")

if __name__ == "__main__":
    input_video_path = "input_video.mp4"  # Sostituisci con il percorso del tuo video di input
    output_video_path = "output_video.mp4"  # Sostituisci con il percorso in cui desideri salvare il video di output
    zoom_factor = 2.0  # Sostituisci con il tuo fattore di upscaling desiderato

    process_video(input_video_path, output_video_path, zoom_factor)
