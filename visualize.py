import cv2
import matplotlib.pyplot as plt

def visualizeUpscaledImages(original1, up_bi1, up_bi_sharp1, original2, up_bi2, up_bi_sharp2):
    
    if original1 is not None and up_bi1 is not None and up_bi_sharp1 is not None:
                
                plt.figure(figsize=(12, 8))
                
                plt.subplot(231)  
                plt.imshow(cv2.cvtColor(original1, cv2.COLOR_BGR2RGB))
                plt.title("Immagine Originale")
                plt.axis('off')

                plt.subplot(232)  
                plt.imshow(cv2.cvtColor(up_bi1, cv2.COLOR_BGR2RGB))
                plt.title("Upscaled-BilateralFilter")
                plt.axis('off')

                plt.subplot(233)  
                plt.imshow(cv2.cvtColor(up_bi_sharp1, cv2.COLOR_BGR2RGB))
                plt.title("Upscaled-BilateralFilter-sharpening")
                plt.axis('off')

                if original2 is not None and up_bi2 is not None and up_bi_sharp2 is not None:

                    plt.subplot(234)  
                    plt.imshow(cv2.cvtColor(original2, cv2.COLOR_BGR2RGB))
                    plt.title("Immagine Originale")
                    plt.axis('off')

                    plt.subplot(235)  
                    plt.imshow(cv2.cvtColor(up_bi2, cv2.COLOR_BGR2RGB))
                    plt.title("Upscaled-BilateralFilter")
                    plt.axis('off')

                    plt.subplot(236)  
                    plt.imshow(cv2.cvtColor(up_bi_sharp2, cv2.COLOR_BGR2RGB))
                    plt.title("Upscaled-BilateralFilter-sharpening")
                    plt.axis('off')

                try:
                    plt.tight_layout()
                    plt.show()
                except (KeyboardInterrupt, SystemExit):
                    pass

    return None