# grid1 sin comentarios solo el codigo mas claro

from cProfile import label
from ctypes import resize
import numpy as np
from numpy import asarray, transpose, tri
from PIL import Image as ImagePIL
from PIL import ImageTk
import sys
import time
from pathlib import Path
from tkinter import *

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


def main():
    global window, cap
    window = Tk()
    # myframe = Frame(window)
    # myframe.pack(fill=BOTH, expand=YES)
    # mycanvas = ResizingCanvas(
    #     myframe, width=1920, height=1080, bg="#1E1E1E", highlightthickness=0)
    # mycanvas.pack(fill=BOTH, expand=YES)

    # Usar ttk para importar un estilo
    #s = ttk.Style()

    # Definicion de los botones y cuadros de la interfaz
    button_image_3 = PhotoImage(file="./assets/button_3.png")
    button_3 = Button(
        image=button_image_3,
        borderwidth=0,
        highlightthickness=0,
        # command=lambda: trigger(),
        relief="flat"
    )



    # Forma de redimensionar las imagenes pero pierden calidad sin antialias
    #Con el resize consigo cambiar el tamaño de los botones en la interfaz
    #la propia imagen, pero esto no cambia el tamaño del grid, esto se cambia abajo donde se crea el layer de la imagen
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


    img_button3 = ImagePIL.open("./assets/button_1.png")
    button_3 = img_button3.resize((400, 120), ImagePIL.ANTIALIAS)
    button_image_stop = ImageTk.PhotoImage(button_3)

    # El botón de reseteo
    button_image_reset = PhotoImage(file="./assets/button_2.png")
    button_reset = Button(image=button_image_reset,
                          borderwidth=0,
                          highlightthickness=0,
                          # command=lambda: os.rename(files[file_pointer],files[file_pointer]+'_'),
                          relief="flat"
                          )

    img_button2 = ImagePIL.open("./assets/button_2.png")
    button_2 = img_button2.resize((400 , 120), ImagePIL.ANTIALIAS)
    button_image_reset = ImageTk.PhotoImage(button_2)


    #Carga de las imagenes de backgroud, ¿se podrían cargar como bg?
    image_image_central = PhotoImage(
        file="assets/image_1.png")

    image_image_grafica_1 = PhotoImage(
        file="./assets/foo.png")

    image_image_grafica_2 = PhotoImage(
        file="./assets/foo2.png")

    image_image_crop = PhotoImage(
        file="./assets/image_6.png")

    # frame para organizar

    image_list = [button_image_3, button_image_stop, button_image_reset, image_image_grafica_1,
                  image_image_grafica_2, image_image_crop]

    # Tamaño mínimo de las columnas y filas.
    window.columnconfigure(1, weight=1, minsize=200)
    window.rowconfigure(1, weight=1, minsize=300)
    window.columnconfigure(2, weight=1, minsize=200)
    window.rowconfigure(2, weight=1, minsize=300)
    window.columnconfigure(3, weight=1, minsize=200)
    window.rowconfigure(3, weight=1, minsize=300)

    # No son botones de esta forma, me da error si lo meto con Button, parece porque
    # se mezcla .grid y .pack en algún momento.
    for i in range(3):
        frame = Frame(master=window, borderwidth=0, relief=FLAT)
        frame.grid(row=i, column=2)
        label = Button(
            master=frame, image=image_list[i], width=400, height=120)
        if i == 1:
            label.command = lambda: window.quit(),
        label.pack()

    button_array[1].configure(command = window.destroy)
    button_array[0].configure(command = start_inferencia)
    labels_array_fondos = []

    for i in range(3, len(image_list)):
        frame = Frame(master=window, relief=RAISED,
                      borderwidth=1, )
        frame.grid(row=i-3, column=1, sticky="nsew")

        label = Label(master=frame, image=image_list[i], width=480, height=320)
        label.pack()

    # Definir el frame de la webcam
    framewebcam = Frame(master=window, width=640, height=480)
    framewebcam.grid(row=0, column=0, rowspan=3)
    vidLabel = Label(master=framewebcam,
                     # anchor='nw'
                     )
    vidLabel.pack()

    # bucle de ledctura de la webcam
    while True:

        # segundo metodo
        # cv2image = cv2.cvtColor(cap.read()[1], cv2.COLOR_BGR2RGB)

        # frame1 = ImagePIL.fromarray(cv2image)

        # frame1 = ImageTk.PhotoImage(frame1)
        # vidLabel.configure(image=frame1)
        # vidLabel.image = frame1

        # print(inferencia(img))
        window.update_idletasks()
        window.update()


# Ejecucion
if __name__ == "__main__":
    main()
