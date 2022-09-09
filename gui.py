from cProfile import label
import numpy as np
from numpy import asarray, transpose, tri
import tensorflow as tf
from PIL import Image as ImagePIL 
from PIL import ImageTk
# import sys, time
import cv2
from pathlib import Path
from tkinter import *
import glob
import io
import time
import os
# segunda versión se ha cambiado la forma en la que se hacen los 
# dibujos, hay que volver a ajustar
#NOTA: al importar tkinter * se reemplaza la Image de PIL con la de Tkinter, 
# por eso no funcionaba si no le pone el as

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path("./assets")


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

def load_labels(filename):
  with open(filename, 'r') as f:
    return [line.strip() for line in f.readlines()]

def inferencia(img):

    global size
    inicio=time.time()
    img= img.convert('RGB').resize(size, ImagePIL.ANTIALIAS)
    input_data = np.array(asarray(img), dtype=np.float32)
    input_data = np.expand_dims(input_data , axis=0)
    interpreter.set_tensor(input_details[0]['index'], input_data)
    interpreter.invoke()
    tensor_resultado= interpreter.get_tensor(output_details[0]['index'])[0]
    
    # resultado=""
    # for i in range(len(labels)):
    #     resultado=resultado + '{:08.6f}: {}'.format(float(tensor_resultado[i]), labels[i])+"\n"

    top_k = tensor_resultado.argsort()[-5:][::-1]
    for i in top_k:
        resultado=('{:08.6f}: {}'.format(float(tensor_resultado[i]), labels[i]))+"\n"
    resultado=resultado+"Tiempo inferencia: "+str(time.time()-inicio)
    return resultado

#Subclass of Canvas para resizing
class ResizingCanvas(Canvas):
    def __init__(self,parent,**kwargs):
        Canvas.__init__(self,parent,**kwargs)
        self.bind("<Configure>", self.on_resize)
        self.height = self.winfo_reqheight()
        self.width = self.winfo_reqwidth()

    def on_resize(self,event):
        # determine the ratio of old width/height to new width/height
        wscale = float(event.width)/self.width
        hscale = float(event.height)/self.height
        self.width = event.width
        self.height = event.height
        # resize the canvas 
        self.config(width=self.width, height=self.height)
        # rescale all the objects tagged with the "all" tag
        self.scale("all",0,0,wscale,hscale)

def main():

    window = Tk()
    myframe = Frame(window)
    myframe.pack(fill=BOTH, expand=YES)
    mycanvas = ResizingCanvas(myframe,width=1920, height=1080, bg="#1E1E1E", highlightthickness=0)
    mycanvas.pack(fill=BOTH, expand=YES)

    #llamada a las labels
    global labels
    labels=load_labels("./ImageNetLabels.txt")

    #Inferencia
    global interpreter, input_details, output_details
    interpreter = tf.lite.Interpreter("./lite-model_imagenet_mobilenet_v3_large_075_224_classification_5_default_1 (1).tflite")
    interpreter.allocate_tensors()
    input_details = interpreter.get_input_details()
    output_details = interpreter.get_output_details()
    _, height, width, _ = interpreter.get_input_details()[0]['shape']
    # print('tensor input', input_details)
    global size
    size = [width, height]

    # mycanvas.create_rectangle(50, 25, 150, 75, fill="blue")
    #La webcam
    cap= cv2.VideoCapture(0)

    #Definicion de los botones y cuadros de la interfaz
    button_image_3 = PhotoImage( file="./assets/button_3.png")
    button_3 = Button(
        image=button_image_3,
        borderwidth=0,
        highlightthickness=0,
        # command=lambda: trigger(),
        relief="flat"
    )
    # button_3.place(
    #     x=1520.0,
    #     y=901.0,
    #     width=343.0,
    #     height=52.0
    # )

    button_image_stop = PhotoImage(file="./assets/button_1.png")
    button_stop = Button(image=button_image_stop,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: window.quit(),
        relief="flat"
    )
    button_stop.configure(width = 343, activebackground = "#33B5E5", relief = FLAT)


    #El botón de reseteo 
    button_image_reset = PhotoImage(file="./assets/button_2.png")
    button_reset = Button(image=button_image_reset,
        borderwidth=0,
        highlightthickness=0,
        # command=lambda: os.rename(files[file_pointer],files[file_pointer]+'_'),
        relief="flat"
        )
    # button_reset.place(
    #     x=700.0,
    #     y=500.0,
    #     width=300.0,
    #     height=52.0
    # )
    button_reset.configure(width = 343, activebackground = "#33B5E5", relief = FLAT)

    image_image_central = PhotoImage(
        file="assets/image_1.png")
  
    image_image_grafica_1 = PhotoImage(
        file="./assets/foo.png")

    image_image_grafica_2 = PhotoImage(
        file="./assets/foo2.png")

    image_image_crop = PhotoImage(
        file="./assets/image_6.png")


    #Añadir las imagenes
    
    mycanvas.create_image(445,701+170,image=image_image_grafica_1)    
    mycanvas.create_image(1150.0,701+170,image=image_image_grafica_2)
    mycanvas.create_image(1125.0,346.0,image=image_image_crop)
    mycanvas.create_image(1700,250, image = button_image_3)
    mycanvas.create_window(1700,325, window=button_stop)
    mycanvas.create_window(1700,400, window=button_reset)
    image_central= mycanvas.create_image(400,346.0,image=PhotoImage(
        file="/home/mario/arinapin/git/factory-inference-frontend/assets/image_1.png"))
    

    # tag all of the drawn widgets
    mycanvas.addtag_all("all")
    while True:
        cv2image= cv2.cvtColor(cap.read()[1],cv2.COLOR_BGR2RGB)
        img = ImagePIL.fromarray(cv2image)
        # Convert image to PhotoImage
        image_image_central=ImageTk.PhotoImage(image = img)
        mycanvas.itemconfig(image_central, image=image_image_central, tag=all)
        print(inferencia(img))
        window.update_idletasks()
        window.update()



#Ejecucion
if __name__ == "__main__":
    main()