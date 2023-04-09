import tkinter as tk
from tkinter import ttk

# Ventana
window = tk.Tk()
window.title('Demo')
window.geometry('300x150')

# Titulo
title_label = ttk.Label(master=window, text='Comienzo interfaz Photopetra', font='Calibri 12 bold')
title_label.pack()

#Input
input_frame = ttk.Frame(master=window)
entry = ttk.Entry(master=input_frame)
button = ttk.Button(master=input_frame, text='Enviar')
entry.pack()
button.pack()
input_frame.pack()

# Run
window.mainloop()