import tkinter as tk
import customtkinter as ctk
import serial
import serial.tools.list_ports
from settings import *

class SerialApp:
    def __init__(self, master):
        # Configuracion inicial de la ventana principal
        self.master = master
        self.master._set_appearance_mode("system") # Ajuste del tema segun el sistema
        self.master.geometry(f"{APP_SIZE[0]}x{APP_SIZE[1]}")
        self.master.resizable(width= False, height= False)
        self.master.title("Interfaz de Puerto Serial")
        
        self.serial_port = None
        
        # Seccion de conexion: Frame y controles relacionados
        self.setup_connection_controls()
        
        # Seccion de entrada de datos: Frame y controles relacionados
        self.setup_data_controls()
        
        # Actualizar lista de puertos disponibles al iniciar
        self.update_ports()
        
        #Inicia la verificacion de estado de conexion
        self.check_connection_state()
    
    def setup_connection_controls(self):
        """Configura los controles para la conexion serial."""
        self.connection_frame = ctk.CTkFrame(self.master)
        self.connection_frame.pack(pady=20, padx=20, fill="x")
        
        ctk.CTkLabel(self.connection_frame, text="Puerto Serial:").grid(row=0, column=0, padx=10, pady=5)
        
        self.dropdown = ctk.CTkComboBox(self.connection_frame, width=200)
        self.dropdown.grid(row=0, column=1, padx=10, pady=5)
        
        self.update_btn = ctk.CTkButton(self.connection_frame, text="Actualizar", command=self.update_ports)
        self.update_btn.grid(row=0, column=2, padx=10, pady=5)
        
        self.connect_btn = ctk.CTkButton(self.connection_frame, text="Conectar", command=self.toggle_connection)
        self.connect_btn.grid(row=0, column=3, padx=10, pady=5)
    
    def setup_data_controls(self):
        """Configura los controles para entrada de datos"""
        self.data_frame = ctk.CTkFrame(self.master)
        self.data_frame.pack(pady=20, padx=20, fill="x")
        
        # Variables para almacenar datos ingresados
        self.data_var1 = tk.StringVar(value="1")
        self.data_var2 = tk.StringVar(value="0")
        self.data_var3 = tk.StringVar(value="0")
        
        # Entradas de datos
        ctk.CTkLabel(self.data_frame, text="Radio:").grid(row=0, column=0, padx=10, pady=5)
        ctk.CTkEntry(self.data_frame, textvariable=self.data_var1).grid(row=0, column=1, padx=10, pady=5)
        ctk.CTkLabel(self.data_frame, text="Longitud:").grid(row=1, column=0, padx=10, pady=5)
        ctk.CTkEntry(self.data_frame, textvariable=self.data_var2).grid(row=1, column=1, padx=10, pady=5)
        ctk.CTkLabel(self.data_frame, text="Dato 3:").grid(row=2, column=0, padx=10, pady=5)
        ctk.CTkEntry(self.data_frame, textvariable=self.data_var3).grid(row=2, column=1, padx=10, pady=5)
        
        # RadioButtons para tipo de luz
        self.light_type = ctk.StringVar(value="Blanca")
        ctk.CTkRadioButton(self.data_frame, text="Luz Blanca", variable=self.light_type, value="Blanca").grid(row=3, column=0, padx=10, pady=5)
        ctk.CTkRadioButton(self.data_frame, text="Luz UV", variable=self.light_type, value="UV").grid(row=3, column=1, padx=10, pady=5)
        
        # Botón START para enviar datos
        self.start_btn = ctk.CTkButton(self.data_frame, fg_color= START_FG_COLOR, text="START", command=self.process_and_send_start_data)
        self.start_btn.grid(row=4, column=2, padx=10, pady=5, sticky='e')
        
        # Botón STOP para enviar señal de parada
        self.stop_btn = ctk.CTkButton(self.data_frame, fg_color= STOP_FG_COLOR, text="STOP", command=self.send_stop_signal)
        self.stop_btn.grid(row=4, column=3, padx=10, pady=5, sticky='e')
    
    # Métodos relacionados con la conexión serial
    def update_ports(self):
        """Actualiza la lista de puertos disponibles."""
        ports = [port.device for port in serial.tools.list_ports.comports()]
        self.dropdown.configure(values=ports)
        self.dropdown.set(ports[0] if ports else "No hay puertos disponibles")

    def connect_to_serial(self):
        """Establece conexión con el puerto serial seleccionado."""
        try:
            selected_port = self.dropdown.get()
            self.connect_btn.configure(text="Conectando...", state="disabled")
            if selected_port and selected_port != "No hay puertos disponibles":
                self.serial_port = serial.Serial(selected_port, BAUDRATE, timeout=TIMEOUT)
                self.connect_btn.configure(text="Desconectar", state="normal")
            else:
                self.show_error("Selecciona un puerto valido.")
                self.connect_btn.configure(text="Conectar", state="normal")
        except Exception as e:
            self.show_error(f"Error al conectar: {str(e)}")
            self.connect_btn.configure(text="Conectar", state="normal")
            self.serial_port = None
        finally:
            if self.serial_port and not self.serial_port.is_open:
                self.serial_port.close()
                self.serial_port = None

    def disconnect_from_serial(self):
        """Cierra la conexión serial si está abierta."""
        if self.serial_port and self.serial_port.is_open:
            self.serial_port.close()
        self.serial_port = None
        self.connect_btn.configure(text="Conectar")
        
    def toggle_connection(self):
        """Alterna entre conectar y desconectar."""
        if not self.serial_port:
            self.connect_to_serial()
        else:
            self.disconnect_from_serial()
            
    def check_connection_state(self):
        """Verifica el estado de la conexión cada 5 segundos y se auto-llama."""
        if self.serial_port:
            if not self.serial_port.is_open:
                self.disconnect_from_serial()
                self.show_error("La conexion se ha perdido.")
        self.master.after(5000, self.check_connection_state)
            
    def show_error(self, message):
        """Muestra un cuadro de diálogo de error."""
        tk.messagebox.showerror("Error", message)
        
    # Métodos relacionados con al procesamiento de datos
    def process_and_send_start_data(self):
        """Procesa y envía datos iniciales a través del puerto serial."""
        data1, data2, data3, light = self.process_data()
        if all(data is not None for data in [data1, data2, data3, light]):
            #TODO: Ajustar el formato de envio de datos con EBER
            data_string = f"{data1},{data2},{data3},{light}\n"
            self.send_data(data_string)
    
    def process_data(self):
        """Procesa las entradas de datos y las convierte a float."""
        try:
            #TODO: Realizar el proceso de conversion de datos para envio a Arduino, integrar formula de @EBER
            data1 = float(self.data_var1.get())
            data2 = float(self.data_var2.get())
            data3 = float(self.data_var3.get())
            light = self.light_type.get() # Obtener el tipo de luz seleccionado
            return data1, data2, data3, light
        except ValueError:
            # Muestra error si los datos no se pueden convertir a float
            self.show_error("Por favor, ingresa valores válidos.")
            return None, None, None, None

    def send_data(self, data):
        """Envía datos a través del puerto serial."""
        if self.serial_port and self.serial_port.is_open:
            try:
                self.serial_port.write(data.encode())
            except Exception as e:
                # Muestra un error si hay problemas al enviar
                self.show_error(f"Error al enviar datos: {str(e)}")
        else:
            # Muestra un error si el puerto serial no está conectado
            self.show_error("El puerto serial no está conectado.")

    def send_stop_signal(self):
        """Envía una señal de parada a través del puerto serial."""
        #TODO: Ajustar el formato de envio de STOP con EBER como bandera o como valor
        self.send_data("STOP\n")

            
def on_closing():
    """Acción a realizar al cerrar la ventana."""
    if app.serial_port:
        app.serial_port.close()
    master.destroy()
            
            
if __name__ == "__main__":
    master = ctk.CTk()
    app = SerialApp(master)
    master.protocol("WM_DELETE_WINDOW", on_closing)
    master.mainloop()
