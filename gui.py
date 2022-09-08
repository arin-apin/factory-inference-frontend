from cProfile import label
import numpy as np
from numpy import asarray, transpose, tri
import tensorflow as tf
from PIL import Image
from PIL import ImageTk
# import sys, time
import cv2
from pathlib import Path
from tkinter import Tk, Canvas, Text, Button, PhotoImage
import glob
import io
import time
import os

cap= cv2.VideoCapture(0)

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path("./assets")

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

window = Tk()

window.geometry("1920x1080")
window.configure(bg = "#1E1E1E")

interpreter = tf.lite.Interpreter("./lite-model_imagenet_mobilenet_v3_large_075_224_classification_5_default_1 (1).tflite")
interpreter.allocate_tensors()
input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()
_, height, width, _ = interpreter.get_input_details()[0]['shape']
# print('tensor input', input_details)
size = [width, height]

def load_labels(filename):
  with open(filename, 'r') as f:
    return [line.strip() for line in f.readlines()]

labels=load_labels("./ImageNetLabels.txt")


def inferencia(img):
    global size
    inicio=time.time()
    img= img.convert('RGB').resize(size, Image.ANTIALIAS)
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

    

canvas = Canvas(
    window,
    bg = "#1E1E1E",
    height = 1080,
    width = 1920,
    bd = 0,
    highlightthickness = 0,
    relief = "ridge"
)

canvas.place(x = 0, y = 0)

button_image_stop = PhotoImage(
    file=relative_to_assets("button_1.png"))
button_stop = Button(
    image=button_image_stop,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: window.quit(),
    relief="flat"
)
button_stop.place(
    x=1520.0,
    y=813.0,
    width=343.0,
    height=52.0
)

button_image_reset = PhotoImage(
    file=relative_to_assets("button_2.png"))
button_reset = Button(
    image=button_image_reset,
    borderwidth=0,
    highlightthickness=0,
    # command=lambda: os.rename(files[file_pointer],files[file_pointer]+'_'),
    relief="flat"
)
button_reset.place(
    x=1520.0,
    y=989.0,
    width=343.0,
    height=52.0
)

image_image_central = PhotoImage(
    file=relative_to_assets("image_1.png"))
image_central = canvas.create_image(
    444.99999999999994,
    346.0,
    image=image_image_central
)

image_image_grafica_1 = PhotoImage(
    file=relative_to_assets("foo.png"))
image_grafica_1 = canvas.create_image(
    45+(800/2),
    701+170,
    image=image_image_grafica_1
)

image_image_grafica_2 = PhotoImage(
    file=relative_to_assets("foo2.png"))
image_grafica_2 = canvas.create_image(
    1208.0,
    701+170,
    image=image_image_grafica_2
)

image_image_crop = PhotoImage(
    file=relative_to_assets("image_6.png"))
image_6 = canvas.create_image(
    1208.0,
    346.0,
    image=image_image_crop
)

button_image_3 = PhotoImage(
    file=relative_to_assets("button_3.png"))
button_3 = Button(
    image=button_image_3,
    borderwidth=0,
    highlightthickness=0,
    # command=lambda: trigger(),
    relief="flat"
)
button_3.place(
    x=1520.0,
    y=901.0,
    width=343.0,
    height=52.0
)

window.resizable(False, False)


while True:
    cv2image= cv2.cvtColor(cap.read()[1],cv2.COLOR_BGR2RGB)
    img = Image.fromarray(cv2image)
    # Convert image to PhotoImage
    image_image_central=ImageTk.PhotoImage(image = img)
    canvas.itemconfig(image_central, image=image_image_central)
    print(inferencia(img))
    window.update_idletasks()
    window.update()
