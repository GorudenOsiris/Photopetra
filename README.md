# Interfaz de Puerto Serial

Una interfaz gráfica de usuario (GUI) diseñada para interactuar con dispositivos a través del puerto serial.

## Funcionalidades Principales

1. **Conexión Serial:**
   - Visualización de puertos seriales disponibles en el sistema.
   - Botón para actualizar la lista de puertos disponibles.
   - Botón para conectar y desconectar el puerto serial seleccionado.
   - Verificación automática del estado de la conexión cada 5 segundos.

2. **Entrada de Datos:**
   - Entradas para tres valores numéricos (Radio, Longitud, Dato 3).
   - Selección del tipo de luz: Blanca o UV a través de RadioButtons.
   - Botón START para enviar datos procesados al dispositivo.
   - Botón STOP para enviar una señal de parada al dispositivo.

## Uso

1. **Conectar al Puerto Serial:**
   - Selecciona un puerto de la lista desplegable.
   - Haz clic en el botón "Conectar". Una vez conectado, el botón cambiará a "Desconectar" para permitir la desconexión.

2. **Enviar Datos:**
   - Ingresa los valores deseados en los campos de entrada.
   - Selecciona el tipo de luz.
   - Haz clic en "START" para enviar los datos. Si quieres enviar una señal de parada, haz clic en "STOP".

## Dependencias

- `tkinter`: para la creación de la GUI.
- `customtkinter`: para elementos personalizados de tkinter.
- `serial`: para la comunicación a través del puerto serial.

## Futuras Mejoras

- Añadir funcionalidades de logging para registrar eventos y acciones realizadas.
- Mejorar el proceso de envío de datos con formatos más avanzados.
- Integrar la capacidad de recibir datos y visualizarlos en la GUI.

