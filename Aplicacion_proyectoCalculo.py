import cv2
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Button
from tkinter import filedialog
import tkinter as tk


img = None
ubi = 1

def seleccionar_imagen(event):
    global img
    global img_ori
    global gaussian_blur
    global median_blur
    global bilateral_blur
     
    img_path = filedialog.askopenfilename(title="Seleccionar Imagen", filetypes=[("Image files", "*.jpg *.jpeg *.png")])

    if img_path:
        
        img_ori = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)    

        img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)

        plt.subplot(1,2,1).remove()
        plt.subplot(1,2,2).remove()
        
        
        plt.subplot(1,1,1)
        if ubi==1:
            aplicar_sobel(event)
        elif ubi==2:
            aplicar_canny(event)
        else:
            mostrar_comparacion(event)

        #aplicar filtros internamente
        gaussian_blur = cv2.GaussianBlur(img, (7, 7), 2) 
        median_blur = cv2.medianBlur(img, 7)
        bilateral_blur = cv2.bilateralFilter(img, 7, 75, 75)


def aplicar_canny(event):
    if img is not None:
        
        global ubi

        ubi = 2

        edges = cv2.Canny(img, 100, 200)

        plt.subplot(1,1,1).remove()
        plt.subplot(1,2,1).remove()
        plt.subplot(1,2,2).remove()
       


        plt.subplot(1, 2, 1)
        plt.title('Imagen Original')
        plt.imshow(img, cmap='gray')
        plt.draw()
        plt.axis('off')

        plt.subplot(1, 2, 2)
        plt.title('Canny')
        plt.imshow(edges, cmap='gray')
        plt.axis('off')

        plt.draw()
        


def aplicar_sobel(event):
    if img is not None:
        
        
        global ubi

        ubi = 1

        sobelx = cv2.Sobel(img, cv2.CV_64F, 1, 0, ksize=5)  
        sobely = cv2.Sobel(img, cv2.CV_64F, 0, 1, ksize=5)  

        magnitud = np.sqrt(sobelx**2 + sobely**2)

        sobelx = cv2.normalize(sobelx, None, 0, 255, cv2.NORM_MINMAX)
        sobely = cv2.normalize(sobely, None, 0, 255, cv2.NORM_MINMAX)
        magnitud = cv2.normalize(magnitud, None, 0, 255, cv2.NORM_MINMAX)

        magnitud = magnitud.astype(np.uint8)
        sobelx = sobelx.astype(np.uint8)
        sobely = sobely.astype(np.uint8)

        plt.subplot(1,1,1).remove()
        plt.subplot(1,2,1).remove()
        plt.subplot(1,2,2).remove()
        

        plt.subplot(1, 2, 1)
        plt.title('Imagen Original')
        plt.imshow(img, cmap='gray')
        plt.axis('off')
                                            
        plt.subplot(1, 2, 2)
        plt.imshow(magnitud, cmap='gray')  
        plt.title('Sobel')
        plt.axis('off')
                        

        plt.draw()


def mostrar_comparacion(event):

    if img is not None:
        global ubi

        ubi = 3

        plt.subplot(1,1,1).remove()
        plt.subplot(1,2,1).remove()
        plt.subplot(1,2,2).remove()

        sobelx = cv2.Sobel(img, cv2.CV_64F, 1, 0, ksize=5)  
        sobely = cv2.Sobel(img, cv2.CV_64F, 0, 1, ksize=5)  

        magnitud = np.sqrt(sobelx**2 + sobely**2)

        sobelx = cv2.normalize(sobelx, None, 0, 255, cv2.NORM_MINMAX)
        sobely = cv2.normalize(sobely, None, 0, 255, cv2.NORM_MINMAX)
        magnitud = cv2.normalize(magnitud, None, 0, 255, cv2.NORM_MINMAX)

        magnitud = magnitud.astype(np.uint8)
        sobelx = sobelx.astype(np.uint8)
        sobely = sobely.astype(np.uint8)

        edges = cv2.Canny(img, 100, 200)
        

        plt.subplot(1, 2, 1)
        plt.title('Sobel')
        plt.imshow(magnitud, cmap='gray')
        plt.axis('off')
                                            
        plt.subplot(1, 2, 2)
        plt.imshow(edges, cmap='gray')  
        plt.title('Canny')
        plt.axis('off')
                        

        plt.draw()    


def imagen_normal(event):
    global img

    img = img_ori

    if ubi==1:
        aplicar_sobel(event)
    elif ubi==2:
        aplicar_canny(event)
    else:
        mostrar_comparacion(event)


def aplicar_filtro_gaussiano(event):
    global img
    
    img=gaussian_blur 

    if ubi==1:
        aplicar_sobel(event)
    elif ubi==2:
        aplicar_canny(event)
    else:
        mostrar_comparacion(event)  
    
    
def aplicar_filtro_mediana(event):
    global img
    
    img=median_blur  

    if ubi==1:
        aplicar_sobel(event)
    elif ubi==2:
        aplicar_canny(event)
    else:
        mostrar_comparacion(event)

def aplicar_filtro_bilateral(event):
    global img
    
    img= bilateral_blur

    if ubi==1:
        aplicar_sobel(event)
    elif ubi==2:
        aplicar_canny(event)
    else:
        mostrar_comparacion(event)






mng = plt.get_current_fig_manager()

mng.window.state('zoomed') 


plt.subplots_adjust(top=0.82)  
plt.subplots_adjust(left=0.22)  


ax_btn_sel_img = plt.axes([0.2, 0.9, 0.15, 0.05])  
btn_sel_img = Button(ax_btn_sel_img, 'Seleccionar Imagen')
btn_sel_img.on_clicked(seleccionar_imagen)

ax_btn_sobel = plt.axes([0.36, 0.9, 0.15, 0.05])  
btn_sobel = Button(ax_btn_sobel, 'Contornos con sobel')
btn_sobel.on_clicked(aplicar_sobel)

ax_btn_canny = plt.axes([0.52, 0.9, 0.15, 0.05])  
btn_canny = Button(ax_btn_canny, 'Contornos con canny')
btn_canny.on_clicked(aplicar_canny)

ax_btn_comparacion = plt.axes([0.68, 0.9, 0.1, 0.05]) 
btn_comparacion = Button(ax_btn_comparacion, 'Comparación')
btn_comparacion.on_clicked(mostrar_comparacion)


ax_btn_original = plt.axes([0.03, 0.75, 0.1, 0.05])  
btn_original = Button(ax_btn_original, 'Sin filtro')
btn_original.on_clicked(imagen_normal)

ax_btn_gauss = plt.axes([0.03, 0.65, 0.1, 0.05])  
btn_gauss = Button(ax_btn_gauss, 'Filtro gaussiano')
btn_gauss.on_clicked(aplicar_filtro_gaussiano)

ax_btn_mediana = plt.axes([0.03, 0.55, 0.1, 0.05])  
btn_mediana = Button(ax_btn_mediana, 'Filtro mediana')
btn_mediana.on_clicked(aplicar_filtro_mediana)

ax_btn_bilateral = plt.axes([0.03, 0.45, 0.1, 0.05])  
btn_bilateral = Button(ax_btn_bilateral, 'Filtro bilateral')
btn_bilateral.on_clicked(aplicar_filtro_bilateral)

ax_text = plt.axes([0.03, 0.85, 0.1, 0.05]) 


ax_text.text(0.1,0,'Aplicar filtros\na la imagen',fontsize=12,fontweight='bold')
ax_text.axis('off')



plt.show()

