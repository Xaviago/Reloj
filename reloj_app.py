import tkinter as tk
import datetime
import zoneinfo as zi
from menu_reloj import crear_menu_configuracion

class RelojApp:
    def __init__(self, config = None):
        #   Variables globales para la primera configuración del reloj
        self.config = config or {
            "letra": ("Helvetica", 40),
            "color_texto": "white",
            "color_fondo": "black",
            "formato_24_horas": True,
            "zona_horaria": "Europe/Madrid"
        }

        #   App con título, tamaño y color de texto y de fondo
        self.app = tk.Tk()
        self.app.title("Reloj")
        self.altura_ventana = 200
        self.anchura_ventana = 323
        self.app.geometry(f"{self.anchura_ventana}x{self.altura_ventana}")
        self.app.configure(bg = self.config["color_fondo"])

        #   Marco para contener el reloj (y centrarlo)
        self.marco_reloj = tk.Frame(self.app, bg = self.config["color_fondo"])
        self.marco_reloj.pack(expand = True)

        #   Etiqueta para mostrar la hora. Letra, color de texto y color de fondo según la configuración
        self.etiqueta_hora = tk.Label(self.app, font = self.config["letra"], fg = self.config["color_texto"], bg = self.config["color_fondo"])
        self.etiqueta_hora.pack(pady = (self.altura_ventana - self.config["letra"][1]) // 2)
        
        #   Creamos el menú de configuración
        crear_menu_configuracion(self.app, self.etiqueta_hora, self.marco_reloj, self.config, self.actualizar_formato)

    #   Como los relojes muestran la hora en tiempo real, necesitamos una función que actualice la hora cada segundo
    def actualizar_reloj(self):
        self.actualizar_formato()
        self.etiqueta_hora.after(10, self.actualizar_reloj)

    #   Debe ser posible cambiar el formato sin esperar a que se actualice la hora
    def actualizar_formato(self):
        hora_actual = datetime.datetime.now().astimezone(zi.ZoneInfo(self.config["zona_horaria"])).strftime("%H:%M:%S") if self.config["formato_24_horas"] else datetime.datetime.now().astimezone(zi.ZoneInfo(self.config["zona_horaria"])).strftime("%I:%M:%S %p")
        self.etiqueta_hora.config(text=hora_actual)

    #   Ejecución principal de la app
    def ejecutar(self):
        self.actualizar_reloj()
        self.app.mainloop()