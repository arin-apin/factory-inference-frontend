import tkinter as tk 
from tkinter import font

class GameScreen():
    def __init__(self, master, image, roi, inventory_item=None, help_text=None):
        self.master = master
        self.roi = roi
        self.image = tk.PhotoImage(file=image)
        self.inventory_item = inventory_item
        self.help_text = help_text

    def on_click(self,event):
        if (self.roi[0] <= event.x <= self.roi[2]
            and self.roi[1] <= event.y <= self.roi[3]):

            if self.inventory_item: 
                self.master.add_inventory_item(self.inventory_item)
            self.master.show_next_screen()

class Game(tk.Tk):
    def __init__(self):
        super().__init__()

        self.inventory_slots = []
        self.inv