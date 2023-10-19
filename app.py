import tkinter as tk
import customtkinter as ctk
import serial
import serial.tools.list_ports
from settings import *

class SerialApp:
    def __init__(self, master):
        self.master = master
        
        # 1. Configurar la apariencia a oscura o clara en función del tema del sistema
        self.master._set_appearance_mode('System')
        # 2. Obtener el tamaño de la ventana de inicio de la settings.py y desactivar el cambio de tamaño de la ventana
        self.master.geometry(f'{APP_SIZE[0]}x{APP_SIZE[1]}')
        self.master.resizable(width= False, height= False)
        self.master.title("Interfaz de Puerto Serial")
        
        self.serial_port = None
        
        # Layout para conexión
        self.connection_frame = tk.Frame(self.master, bd=2, bg=DARK_BG_COLOR, relief="groove")
        self.connection_frame.pack(pady=20, padx=20, fill="x")
        
        ctk.CTkLabel(self.connection_frame, text="Puerto Serial:").grid(row=0, column=0, padx=10, pady=5)
        
        self.dropdown = ctk.CTkComboBox(self.connection_frame, width=200)
        self.dropdown.grid(row=0, column=1, padx=10, pady=5)
        
        self.update_btn = ctk.CTkButton(self.connection_frame, text="Actualizar", command=self.update_ports)
        self.update_btn.grid(row=0, column=2, padx=10, pady=5)
        
        self.connect_btn = ctk.CTkButton(self.connection_frame, text="Conectar", command=self.toggle_connection)
        self.connect_btn.grid(row=0, column=3, padx=10, pady=5)
        
        # Layout para entradas de datos
        self.data_frame = tk.Frame(self.master, bd=2, bg=DARK_BG_COLOR, relief="groove")
        self.data_frame.pack(pady=20, padx=20, fill="x")
        
        self.data_var1 = tk.StringVar()
        self.data_var2 = tk.StringVar()
        self.data_var3 = tk.StringVar()
        
        ctk.CTkLabel(self.data_frame, text= "Radio:").grid(row=0, column=0, padx=10, pady=5)
        ctk.CTkEntry(self.data_frame, textvariable=self.data_var1).grid(row=0, column=1, padx=10, pady=5)
        
        ctk.CTkLabel(self.data_frame, text= "Longitud:").grid(row=1, column=0, padx=10, pady=5)
        ctk.CTkEntry(self.data_frame, textvariable=self.data_var2).grid(row=1, column=1, padx=10, pady=5)
        
        ctk.CTkLabel(self.data_frame, text= "Dato 3:").grid(row=2, column=0, padx=10, pady=5)
        ctk.CTkEntry(self.data_frame, textvariable=self.data_var3).grid(row=2, column=1, padx=10, pady=5)
        
        # Botones para tipo de luz
        self.light_type = ctk.StringVar()
        ctk.CTkRadioButton(self.data_frame, text= "Luz Blanca", variable= self.light_type, value="Blanca").grid(row=3, column= 0, padx=10, pady=5)
        ctk.CTkRadioButton(self.data_frame, text= "Luz UV", variable= self.light_type, value="UV").grid(row=3, column= 1, padx=10, pady=5)

        # Actualizar lista de puertos al inicio
        self.update_ports()
    
    def update_ports(self):
        ports = [port.device for port in serial.tools.list_ports.comports()]
        self.dropdown._values = ports
        if ports:
            self.dropdown.set(ports[0])
        else:
            self.dropdown.set("No hay puertos disponibles")

    def connect_to_serial(self):
        try:
            selected_port = self.dropdown.get()
            self.connect_btn.configure(text="Conectando...", state="disabled")
            if selected_port and selected_port != "No hay puertos disponibles":
                self.serial_port = serial.Serial(selected_port, 9600, timeout=1)
                self.connect_btn.configure(text="Desconectar", state="normal")
            else:
                self.show_error("Selecciona un puerto valido.")
        except Exception as e:
            self.show_error(f"Error al conectar: {str(e)}")
            self.connect_btn.configure(text="Conectar", state="normal")
            self.serial_port = None

    def disconnect_from_serial(self):
        if self.serial_port and self.serial_port.is_open:
            self.serial_port.close()
        self.serial_port = None
        self.connect_btn.configure(text="Conectar")
        
    def toggle_connection(self):
        if not self.serial_port:
            self.connect_to_serial()
        else:
            self.disconnect_from_serial()
            
    def check_connection_state(self):
        if self.serial_port:
            if not self.serial_port.is_open():
                self.show_error("La conexión se ha perdido.")
                self.disconnect_from_serial()
        self.master.after(5000, self.check_connection_state)
            
    def show_error(self, message):
            tk.messagebox.showerror("Error", message)
            
def on_closing():
    if app.serial_port:
        app.serial_port.close()
    master.destroy()
            
            
if __name__ == "__main__":
    master = ctk.CTk()
    app = SerialApp(master)
    master.protocol("WM_DELETE_WINDOW", on_closing)
    master.mainloop()
