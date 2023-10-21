#Interfaz de Puerto Serial
Esta GUI (Interfaz Gráfica de Usuario) se diseñó para establecer comunicación serial con dispositivos externos, proporcionando una forma intuitiva y amigable de interactuar con ellos.

Características
1. Conexión Serial

Lista dinámica de puertos disponibles, con la capacidad de actualizar automáticamente.
Botón de conexión que permite conectar y desconectar del puerto seleccionado.
Comprobación automática del estado de la conexión cada 5 segundos, desconectando y notificando al usuario si se pierde la conexión.
Entrada de Datos

Tres entradas para datos numéricos, con validaciones para garantizar que se ingresen valores válidos.
Seleccionador de tipo de luz con opciones para "Luz Blanca" y "Luz UV".
Botón START para enviar los datos procesados al dispositivo.
Botón STOP para enviar una señal de parada al dispositivo.
Gestión de Errores

Mensajes de error claros y descriptivos que informan al usuario sobre problemas específicos, ya sea con la entrada de datos o con la conexión serial.
Diseño de Interfaz

Utiliza customtkinter para mejorar la estética de la interfaz y proporcionar un aspecto más moderno y pulido.
Pendientes
Ajustar el formato de envío de datos según especificaciones adicionales.
Integrar fórmulas o cálculos específicos para procesar los datos antes de enviarlos.