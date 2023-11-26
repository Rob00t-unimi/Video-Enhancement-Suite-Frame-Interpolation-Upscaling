# Project Frame Interpolation and Upscaling for Video

For computational complexity reasons, it is better to perform frame interpolation first and then upscaling. However, for the best results, it is preferable to apply upscaling first and then frame interpolation.

### Requires:
#### Used Libraries:
- OpenCV
- NumPy
- matplotlib
- msvcrt
- os
- tkinter
- time
- json
- ttkbootstrap
- ttkthemes
- webbrowser

### Instructions:

- Run `main.py`
- Select the video
- Select parameters
- Run

### Processing Steps:

`main.py` is a GUI that allows you to select the video and the desired enhancement parameters. A button allows you to launch `demo.py` in a new thread.

#### Frame Interpolation:
1. `demo.py` passes the video's path to the frame interpolation function.
2. The video interpolation function increases the number of frames by first calculating the optical flow between frame pairs both forward and backward, then interpolating n new frames between each frame pair.
3. The original frames are discarded.
4. on every new frame is applied a median blur denoizing.
5. The video is saved.

#### Video Upscaling:
6. `demo.py` calls the video upscaling function, passing it the path of the video. For each frame, the function invokes the bilinear upscaling function.
7. Once a frame has been upscaled, enhancement is applied, and the frame is saved to the new video, until completion.

### End of System

### Legend:

- `zoom_factor`:                        Desired upscaling factor
- `iterazioniUpscaling`:                Number of times upscaling is performed on the same frame
- `numInterpolateFrames`:               Number of frames to interpolate for each frame pair

- final_upscaling = initial_resolution * (zoom_factor ** iterations)

- Final FPS after interpolation:  FPS = numInterpolateFrames * (numFramesIniziale - 1)

- Codec used: XVID

- `filterValues` Legend:

    * `blur_k_dim`:                       Initial blurring kernel size
    * `blur_sigma_x`:                     Initial blurring sigma
    * `sharp_k_center`:                   Center value of the sharpening kernel
    * `Laplacian_k_size`:                 Laplacian kernel size (lower values detect finer edges)
    * `threshold_value`:                  Threshold value (precision of edges included in binarization, 0-255, lower values include more edges)
    * `blur_k_dim_2`:                     Dimension of the median blur denoising kernel
    * `showEdges`:                        Keep as false, allows enabling or disabling the visualization of edge detection overlaid on the image


Coded by Roberto Tallarini

