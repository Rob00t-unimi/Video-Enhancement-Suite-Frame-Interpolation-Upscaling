import cv2
import numpy as np
import matplotlib.pyplot as plt

# Carica i due frame consecutivi
frame1 = cv2.imread("progetto-principi/materials/output/upscaling/bilinear/img_upscaledBilinear_bilateral_sharpened1.png")
frame2 = cv2.imread("progetto-principi/materials/output/upscaling/bilinear/img_upscaledBilinear_bilateral_sharpened2.png")

frame1 = cv2.imread("progetto-principi/materials/input/cube/frame1-1080p.png")
frame2 = cv2.imread("progetto-principi/materials/input/cube/frame2-1080p.png")


########################

# Visualizza i frame in una finestra separata
plt.figure(figsize=(12, 4))

plt.subplot(131)
plt.imshow(cv2.cvtColor(frame1, cv2.COLOR_BGR2RGB))
plt.title("Frame1")
plt.axis('off')

plt.subplot(132)
plt.imshow(cv2.cvtColor(interpolated_frame, cv2.COLOR_BGR2RGB))
plt.title("Interpolazione")
plt.axis('off')

plt.subplot(133)
plt.imshow(cv2.cvtColor(frame2, cv2.COLOR_BGR2RGB))
plt.title("Frame2")
plt.axis('off')

plt.show()
