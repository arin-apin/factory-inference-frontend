from cProfile import label
from cgitb import text
from ctypes import resize
from mimetypes import common_types
from tkinter import scrolledtext
import numpy as np
from numpy import asarray, transpose, tri
from PIL import Image as ImagePIL
from PIL import ImageTk
import time
import cv2
import os
from pathlib import Path
from tkinter import *


 #https://coral.ai/docs/edgetpu/tflite-python/#update-existing-tf-lite-code-for-the-edge-tpu
import tflite_runtime.interpreter as tflite

# from pycoral.adapters import common
# from pycoral.adapters import common
# from pycoral.utils import edgetpu
# from pycoral.utils import dataset 

#pantalla portatil = 1920 *1080
original_dpi = 72

script_dir = Path(__file__).parent.absolute()
assets_path = script_dir / Path("./assets")
print(assets_path)

# model_file = os.path.join(script_dir, 'lite-model_imagenet_mobilenet_v3_large_075_224_classification_5_default_1 (1).tflite')
# label_file = os.path.join(script_dir, "ImageNetLabels.txt")

def get_dpi():
    screen = Tk()
    current_dpi = screen.winfo_fpixels('1i')
    screen.destroy()
    return current_dpi


# Subclass of Canvas para resizing
class ResizingCanvas(Canvas):
    def __init__(self, parent, **kwargs):
        Canvas.__init__(self, parent, **kwargs)
        self.bind("<Configure>", self.on_resize)
        self.height = self.winfo_reqheight()
        self.width = self.winfo_reqwidth()

    def on_resize(self, event):
        # determine the ratio of old width/height to new width/height
        wscale = float(event.width)/self.width
        hscale = float(event.height)/self.height
        self.width = event.width
        self.height = event.height
        # resize the canvas
        self.config(width=self.width, height=self.height)
        # rescale all the objects tagged with the "all" tag
        self.scale("all", 0, 0, wscale, hscale)

def inferencia(img):

    global size
    inicio=time.time()
    img= img.convert('RGB').resize(size, ImagePIL.Resampling.LANCZOS)
    input_data = np.array(asarray(img), dtype=np.float32)
    input_data = np.expand_dims(input_data , axis=0)
    interpreter.set_tensor(input_details[0]['index'], input_data)
    interpreter.invoke()
    tensor_resultado= interpreter.get_tensor(output_details[0]['index'])[0]

    top_k = tensor_resultado.argsort()[-5:][::-1]
    for i in top_k:
        resultado=('{:08.6f}: {}'.format(float(tensor_resultado[i]), labels[i]))+"\n"
    resultado=resultado+"Tiempo inferencia: "+str(time.time()-inicio)
    return resultado


#def relative_to_assets(path: str) -> Path:
 #   return ASSETS_PATH / Path(path)

#Cargar etiquetass
def load_labels(filename):
  with open(filename, 'r') as f:
    return [line.strip() for line in f.readlines()]

def start_inferencia():
    global flag_inferencia
    print("inferencia started")
    flag_inferencia=1

def main():

    global window, cap, flag_inferencia
    flag_inferencia=0
    window = Tk()
    dpi = window.winfo_fpixels('1i')
    print(dpi)
    SCALE = get_dpi()/original_dpi
    print("Factor de escalado: ", SCALE)
    window.tk.call('tk', 'scaling', 1.25)

    # myframe = Frame(window)
    # myframe.pack(fill=BOTH, expand=YES)
    # mycanvas = ResizingCanvas(
    #     myframe, width=1920, height=1080, bg="#1E1E1E", highlightthickness=0)
    # mycanvas.pack(fill=BOTH, expand=YES)

     #activar la camara cuando tenga el dispositivo
    cap = cv2.VideoCapture(0)
    

    global labels

    #get the files, this only work with one filetype 
    for file in os.listdir():
        if file.endswith('tflite'):
            model=file
            print("model found: ",model)
        if file.endswith('txt'):
            labels_path=file
            print("label found: ", labels_path)

   #llamada a las labels
    
    labels=load_labels(labels_path)

    #Inferencia
    global interpreter, input_details, output_details
    interpreter = tflite.Interpreter(model)
        #experimental_delegates=[tflite.load_delegate('libedgetpu.so.1')])
    interpreter.allocate_tensors()
    input_details = interpreter.get_input_details()
    output_details = interpreter.get_output_details()
    _, height, width, _ = interpreter.get_input_details()[0]['shape']
    # print('tensor input', input_details)
    global size
    size = [width, height]


    # Definicion de los botones y cuadros de la interfaz
    size_w = 1920/3
    size_l = 1080/3


    # Forma de redimensionar las imagenes pero pierden calidad sin antialias
    img_button3 = ImagePIL.open("./assets/button_3.png")
    button_3 = img_button3.resize((400, 120), ImagePIL.Resampling.LANCZOS)
    button_image_3 = ImageTk.PhotoImage(button_3)

    button_image_stop = PhotoImage(file="./assets/button_1.png")
    # button_stop = Button(image=button_image_stop,
    #                      borderwidth=0,
    #                      highlightthickness=0,
    #                      command=lambda: window.quit(),
    #                      relief="flat"
    #                      )
    # button_stop.configure(width=343, activebackground="#33B5E5", relief=FLAT)


    img_button3 = ImagePIL.open((os.path.join(assets_path,"button_1.png")))
    button_3 = img_button3.resize((400, 120), ImagePIL.Resampling.LANCZOS)
    button_image_stop = ImageTk.PhotoImage(button_3)
  
    # El bot??n de reseteo
    button_image_reset = PhotoImage(file="./assets/button_2.png")
    # button_reset = Button(image=button_image_reset,
    #                       borderwidth=0,
    #                       highlightthickness=0,
    #                       # command=lambda: os.rename(files[file_pointer],files[file_pointer]+'_'),
    #                       relief="flat"
    #                       )

    img_button2 = ImagePIL.open("./assets/button_2.png")
    button_2 = img_button2.resize((400 , 120), ImagePIL.Resampling.LANCZOS)
    button_image_reset = ImageTk.PhotoImage(button_2)


    #Carga de las imagenes de backgroud
    image_image_central = PhotoImage(
        file="assets/image_1.png")
    

    image_image_grafica_1 = ImagePIL.open("./assets/foo.png")
    image_image_grafica_1  = image_image_grafica_1.resize((640 , 480), ImagePIL.Resampling.LANCZOS)
    image_image_grafica_1  = ImageTk.PhotoImage(image_image_grafica_1 )

    image_image_grafica_2 = ImagePIL.open("./assets/foo2.png")
    image_image_grafica_2  = image_image_grafica_2.resize((640 , 480), ImagePIL.Resampling.LANCZOS)
    image_image_grafica_2  = ImageTk.PhotoImage(image_image_grafica_2 )

    image_image_crop = ImagePIL.open("./assets/image_6.png")
    image_image_crop  = image_image_crop.resize((640 , 480), ImagePIL.Resampling.LANCZOS)
    image_image_crop  = ImageTk.PhotoImage(image_image_crop )

    # frame para organizar

    image_list = [button_image_3, button_image_stop, button_image_reset, image_image_grafica_1,
                  image_image_grafica_2, image_image_crop]

    # Tamano minimo de las columnas y filas.
    window.columnconfigure(1, weight=1, minsize=200)
    window.rowconfigure(1, weight=1, minsize=300)
    window.columnconfigure(2, weight=1, minsize=200)
    window.rowconfigure(2, weight=1, minsize=300)
    window.columnconfigure(3, weight=1, minsize=200)
    window.rowconfigure(3, weight=1, minsize=300)

    button_array = []
    # No son botones de esta forma, me da error si lo meto con Button, parece porque
    # se mezcla .grid y .pack en algun momento.
    for i in range(3):
        frame = Frame(master=window, borderwidth=0, relief=FLAT)
        frame.grid(row=i, column=2)
        Button1 = Button(
            master=frame, image=image_list[i], width=400, height=120, bg='red')
        button_array.append(Button1)
        Button1.pack(expand=True, fill=BOTH)

    button_array[1].configure(command = window.destroy)
    button_array[0].configure(command = start_inferencia)
    labels_array_fondos = []

    for i in range(3, len(image_list)):
        frame = Frame(master=window, relief=RAISED,
                      borderwidth=1, )
        frame.grid(row=i-3, column=1, sticky="nsew")
        label = Label(master=frame,image=image_list[i], 
                    #width=480, height=320,
                    width=640, height=320, 
                    text="array label", compound='center', font=("Arial",14),
                    fg='#21ab4b',bg='green')
        labels_array_fondos.append(label)
        label.pack(expand=1)

    
    #obtain resolution from webcam 

    # Definir el frame de la webcam
    
    cam_wide = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
    cam_height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
    framewebcam = Frame(master=window, width=cam_wide, height=cam_height)
    framewebcam.grid(row=0, column=0, rowspan=3)
    vidLabel = Label(master=framewebcam,
                     # anchor='nw'
                    #  width=w,
                    #  height=h
                     )
    vidLabel.pack(side=LEFT,fill=BOTH,expand=TRUE)

    # bucle de lectura de la webcam
    while True:
        cv2image = cv2.cvtColor(cap.read()[1], cv2.COLOR_BGR2RGB)
        #imagen de testeo, si no tengo webcam
        #framePIL = ImagePIL.open("./assets/??ndice.jpeg")
        framePIL = ImagePIL.fromarray(cv2image)
        #Convert image to Photoimage
        frame1 = ImageTk.PhotoImage(framePIL)
        vidLabel.configure(image=frame1)
        vidLabel.image = frame1

        if flag_inferencia == 1:
            #Hacer la inferencia de la imagen PIL
            res_inferencia = inferencia(framePIL)
            x = res_inferencia.split("\n")
            #print(x[0])
            labels_array_fondos[0].configure(text=x[0])        
            labels_array_fondos[1].configure(text=x[1])

        window.update_idletasks()
        window.update()


# Ejecucion
if __name__ == "__main__":
    main()
