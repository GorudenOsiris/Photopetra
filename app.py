import os
import customtkinter as ctk
from settings import *

# Cargar el directorio en que se encuentra la aplicacion
path_actual = os.path.dirname(os.path.realpath(__file__))

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        # 1. Configurar la apariencia a oscura o clara en función del tema del sistema
        ctk.set_appearance_mode('System')
        # 2. Obtener el tamaño de la ventana de inicio de la settings.py y desactivar el cambio de tamaño de la ventana
        self.geometry(f'{APP_SIZE[0]}x{APP_SIZE[1]}')
        self.resizable(width= False, height= False)
        
        self.navigation_frame = ctk.CTkFrame(master= self, width= 140,corner_radius= STYLING['corner-radius'])
        self.navigation_frame.pack(pady= 20, padx= 60, fill='both', expand=True)
        
        
        
        self.mainloop()
        
    
class Boton(ctk.CTkButton):
    def __init__(self, parent, text, image):
        super().__init__(
            master= parent,
            text= text)

if __name__ == '__main__':
    App()