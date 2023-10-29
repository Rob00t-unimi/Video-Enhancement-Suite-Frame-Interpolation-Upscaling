import numpy as np
import scipy
import cv2
import matplotlib.pyplot as plt
from BicubicUpscaling import bicubic_upscale
from BilinearUpscaling import bilinear_upscale
from visualize import visualizeUpscaledImages

#path dei 2 frame
framePath1 = "progetto-principi/materials/input/frame1.png"
framePath2 = "progetto-principi/materials/input/frame2.png"

#upscaling dei frame
frame1, up_bi_filtered_img1, up_img1 = bilinear_upscale(framePath1, 1.5, 1)
frame2, up_bi_filtered_img2, up_img2 = bilinear_upscale(framePath2, 1.5, 2)
#frame1, up_bi_filtered_img1, up_img1 = bicubic_upscale(framePath1, 1.5, 1)
#frame2, up_bi_filtered_img2, up_img2 = bicubic_upscale(framePath2, 1.5, 2)

#visualizzazione frame upscalati
visualizeUpscaledImages(frame1, up_bi_filtered_img1, up_img1, frame2, up_bi_filtered_img2, up_img2)

#frame interpolation
#...

