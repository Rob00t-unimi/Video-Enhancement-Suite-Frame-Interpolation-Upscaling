import cv2

def resize_video(input_path, output_path, target_fps=10):
    # Apre il video
    cap = cv2.VideoCapture(input_path)

    # Ottiene il frame rate del video originale
    original_fps = cap.get(cv2.CAP_PROP_FPS)

    # Verifica che il frame rate target sia maggiore di zero
    if target_fps <= 0:
        print("Il frame rate target deve essere maggiore di zero.")
        return

    # Calcola il rapporto di ridimensionamento
    resize_factor = original_fps / target_fps

    # Ottiene le dimensioni del video originale
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    # Crea l'oggetto VideoWriter per scrivere il video ridimensionato
    out = cv2.VideoWriter(output_path, cv2.VideoWriter_fourcc(*'XVID'), target_fps, (width, height))

    while True:
        ret, frame = cap.read()

        if not ret:
            break

        # Scrive il frame solo ogni resize_factor frame
        if cap.get(cv2.CAP_PROP_POS_FRAMES) % resize_factor < 1:
            out.write(frame)

    # Rilascia le risorse
    cap.release()
    out.release()

    print(f"Video ridimensionato con successo a {target_fps} fps. Salvato in {output_path}")

if __name__ == "__main__":
    input_video_path = r"C:\Users\rober\Desktop\progetto-principi\materials\input\stockVideos\la haine - zoom in\cut_24fps_10sec_720p.mp4"
    output_video_path = r"C:\Users\rober\Desktop\progetto-principi\materials\input\stockVideos\la haine - zoom in\cut_10fps_10sec_720p.mp4"
    target_fps = 10

    resize_video(input_video_path, output_video_path, target_fps)
