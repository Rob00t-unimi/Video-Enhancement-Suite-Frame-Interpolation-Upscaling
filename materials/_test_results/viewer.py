from moviepy.editor import VideoFileClip, clips_array, vfx
import tkinter as tk

def get_screen_dimensions():
    root = tk.Tk()
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    root.destroy()
    return screen_width, screen_height


def videoViewer(video_path1, video_path2, same_dimensions):

    # Utilizza la funzione per ottenere le dimensioni dello schermo
    screen_width, _ = get_screen_dimensions()

        # Carica i video
    clip1 = VideoFileClip(video_path1)
    clip2 = VideoFileClip(video_path2)
    
    if same_dimensions:
        clip1_resized = clip1.resize(width=screen_width/2)
        clip2_resized = clip2.resize(width=screen_width/2)
    else:
        clip1_resized = clip1.resize(width=screen_width/3)
        clip2_resized = clip2.resize(width=screen_width/3*2)
    
    final_clip = clips_array([[clip1_resized, clip2_resized]])
    final_clip.preview()
    final_clip.close()

    clip1_slow = clip1.fx(vfx.speedx, 0.4)
    clip2_slow = clip2.fx(vfx.speedx, 0.4)

    if same_dimensions:
        clip1_slow_resized = clip1_slow.resize(width=screen_width/2)
        clip2_slow_resized = clip2_slow.resize(width=screen_width/2)
    else:
        clip1_slow_resized = clip1_slow.resize(width=screen_width/3)
        clip2_slow_resized = clip2_slow.resize(width=screen_width/3*2)

    final_clip = clips_array([[clip1_slow_resized, clip2_slow_resized]])
    final_clip.preview()
    final_clip.close()




path1 = r"C:\Users\rober\Desktop\MainFolder\UniMi\Percezione\ProjectCode\Originale\progetto-principi\materials\_test_results\lights - 10fps to 60fps\short-720p-10fps.mp4"
path2 = r"C:\Users\rober\Desktop\MainFolder\UniMi\Percezione\ProjectCode\Originale\progetto-principi\materials\_test_results\lights - 10fps to 60fps\UpscaledVideo-Interpolated.avi"

# same_dimensions = False
same_dimensions = True

videoViewer(path1, path2, same_dimensions)