import numpy as np
import scipy
import cv2
import matplotlib.pyplot as plt
from BicubicUpscaling import bicubic_upscale
from BilinearUpscaling import bilinear_upscale
from visualize import visualizeUpscaledImages

#path dei 2 frame
framePath1 = "progetto-principi/materials/input/race/frame1-720p.png"
framePath2 = "progetto-principi/materials/input/race/frame2-720p.png"
zoom_factor = 1.5

#upscaling dei frame:
#Bilineare
frame1, up_img1, up_bi_filtered_img1, up_bi_sharp1  = bilinear_upscale(framePath1, zoom_factor, 1)
frame2, up_img2, up_bi_filtered_img2, up_bi_sharp2  = bilinear_upscale(framePath2, zoom_factor, 2)

#Bicubico
#frame1, up_img1, up_bi_filtered_img1, up_bi_sharp1 = bicubic_upscale(framePath1, zoom_factor, 1)
#frame2, up_img2, up_bi_filtered_img2, up_bi_sharp2 = bicubic_upscale(framePath2, zoom_factor, 2)


######################
#frame2, up_img2, up_bi_filtered_img2, up_bi_sharp2  = None, None, None, None
#provo ad applicarlo di nuovo per vedere se migliora un po' sull'immagine già upcalata e filtrata con il filtro bilaterale
#cv2.imwrite("progetto-principi/materials/output/upscaling/bilinear/img_upscaledBilinear-filtered1.png", up_bi_sharp1)  # Salva l'immagine elaborata su disco
#frame1, up_img1, up_bi_filtered_img1, up_bi_sharp1 = bilinear_upscale("progetto-principi/materials/output/upscaling/bilinear/img_upscaledBilinear-filtered1.png", zoom_factor, 1)
######################


print("Completato!")
#visualizzazione frame upscalati
#originale - upscalato - upscalato con bilateral filter - upscalato con bilateral filter e sharpening filter
visualizeUpscaledImages(frame1, up_img1, up_bi_filtered_img1, up_bi_sharp1, frame2, up_img2, up_bi_filtered_img2, up_bi_sharp2)

print("Continuo..")

#frame interpolation
#...

print("End..")
