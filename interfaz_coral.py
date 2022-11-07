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


script_dir = Path(__file__).parent.absolute()
assets_path = script_dir / Path("./assets")
print(assets_path)

model_file = os.path.join(script_dir, 'lite-model_imagenet_mobilenet_v3_large_075_224_classification_5_default_1 (1).tflite')
label_file = os.path.join(script_dir, "ImageNetLabels.txt")


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
    img= img.convert('RGB').resize(size, ImagePIL.ANTIALIAS)
    input_data = np.array(asarray(img), dtype=np.float32)
    input_data = np.expand_dims(input_data , axis=0)
    interpreter.set_tensor(input_details[0]['index'], input_data)
    interpreter.invoke()
    tensor_resultado= interpreter.get_tensor(output_details[0]['index'])[0]

    top_k = tensor_resultado.argsort()[-5:][::-1]
    #We get the top 5 results 
    resultado=''
    #print(top_k)
    for i in top_k:
        resultado+=('{:08.6f}: {}'.format(float(tensor_resultado[i]), labels[i]))+"\n"
    resultado=resultado+"Tiempo inferencia: "+str(time.time()-inicio)
    #print(resultado, '\n')
    resultado_max= resultado.partition('\n')[0]+'\n'+ resultado.split('\n')[-1] 
    return resultado_max, resultado


#def relative_to_assets(path: str) -> Path:
 #   return ASSETS_PATH / Path(path)

#Load labels from file
def load_labels(filename: str):
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

    #Another way to make the interface resizable or responsive
    # myframe = Frame(window)
    # myframe.pack(fill=BOTH, expand=YES)
    # mycanvas = ResizingCanvas(
    #     myframe, width=1920, height=1080, bg="#1E1E1E", highlightthickness=0)
    # mycanvas.pack(fill=BOTH, expand=YES)

    #Camera asigned
    cap = cv2.VideoCapture(0)

    #Labels for the model
    global labels

    for file in os.listdir():
        if file.endswith('tflite'):
            model=file
            print("model found: ",model)
        if file.endswith('txt'):
            labels_path=file
            print("label found: ", labels_path)

    labels=load_labels(labels_path)

    #Inference
    global interpreter, input_details, output_details
    interpreter = tflite.Interpreter(model, 
        experimental_delegates=[tflite.load_delegate('libedgetpu.so.1')])
    interpreter.allocate_tensors()
    input_details = interpreter.get_input_details()
    output_details = interpreter.get_output_details()
    _, height, width, _ = interpreter.get_input_details()[0]['shape']
    # print('tensor input', input_details)
    global size
    size = [width, height]


    # Definition of button and images for the interface

    #A way to redimension images but they lose quality without antialias method
    img_button3 = ImagePIL.open("./assets/button_3.png")
    button_3 = img_button3.resize((400, 120), ImagePIL.ANTIALIAS)
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
    button_3 = img_button3.resize((400, 120), ImagePIL.ANTIALIAS)
    button_image_stop = ImageTk.PhotoImage(button_3)
  
    # Reset button
    button_image_reset = PhotoImage(file="./assets/button_2.png")
    # button_reset = Button(image=button_image_reset,
    #                       borderwidth=0,
    #                       highlightthickness=0,
    #                       # command=lambda: os.rename(files[file_pointer],files[file_pointer]+'_'),
    #                       relief="flat"
    #                       )

    img_button2 = ImagePIL.open("./assets/button_2.png")
    button_2 = img_button2.resize((400 , 120), ImagePIL.ANTIALIAS)
    button_image_reset = ImageTk.PhotoImage(button_2)


    #Loading of the backgrounds images
    image_image_central = PhotoImage(
        file="assets/image_1.png")

    image_image_grafica_1 = PhotoImage(
        file="./assets/foo.png")

    image_image_grafica_2 = PhotoImage(
        file="./assets/foo2.png")

    image_image_crop = PhotoImage(
        file="./assets/image_6.png")

    # List for organizing the images. 

    image_list = [button_image_3, button_image_stop, button_image_reset, image_image_grafica_1,
                  image_image_grafica_2, image_image_crop]

    # Min size for rows and columns
    window.columnconfigure(1, weight=1, minsize=200)
    window.rowconfigure(1, weight=1, minsize=300)
    window.columnconfigure(2, weight=1, minsize=200)
    window.rowconfigure(2, weight=1, minsize=300)
    window.columnconfigure(3, weight=1, minsize=200)
    window.rowconfigure(3, weight=1, minsize=300)

    button_array = []
    
    #
    # You have to grid the frame and the use pack. 
    for i in range(3):
        frame = Frame(master=window, borderwidth=0, relief=FLAT)
        frame.grid(row=i, column=2)
        Button1 = Button(
            master=frame, image=image_list[i], width=400, height=120)
        button_array.append(Button1)
        Button1.pack(expand=True)

    #Here we assign commands to the button,the first one close the interface, the  trigger button starts infering from the webcam image
    button_array[1].configure(command = window.destroy)
    button_array[0].configure(command = start_inferencia)
    labels_array_fondos = []

    #Tkinter frames for labels
    for i in range(3, len(image_list)):
        frame = Frame(master=window, relief=RAISED,
                      borderwidth=1, )
        frame.grid(row=i-3, column=1, sticky="nsew")
        label = Label(master=frame,image=image_list[i], width=480, height=320, text="array label", compound='center', font=("Arial",14),fg='#21ab4b')
        labels_array_fondos.append(label)
        label.pack()

    

    # Frame for webcam video
    framewebcam = Frame(master=window, width=640, height=480)
    framewebcam.grid(row=0, column=0, rowspan=3)
    vidLabel = Label(master=framewebcam,
                     # anchor='nw'
                     )
    vidLabel.pack()

    # Loop for obtainign image from webcam and performing the inference
    while True:
        cv2image = cv2.cvtColor(cap.read()[1], cv2.COLOR_BGR2RGB)
        #In case of having no webcam, fixed image
        # framePIL = ImagePIL.open("./assets/índice.jpeg")
        framePIL = ImagePIL.fromarray(cv2image)
        #Convert image to Photoimage
        frame1 = ImageTk.PhotoImage(framePIL)
        vidLabel.configure(image=frame1)
        vidLabel.image = frame1

        #When the trigger button is pressed
        if flag_inferencia ==1:
            #Make inference from PIL image
            res_inferencia, res_total = inferencia(framePIL)
            x = res_inferencia.split("\n")
            #print(x[0])
            labels_array_fondos[0].configure(text=x[0])        
            labels_array_fondos[1].configure(text=x[1])

        window.update_idletasks()
        window.update()


# Ejecucion
if __name__ == "__main__":
    main()
