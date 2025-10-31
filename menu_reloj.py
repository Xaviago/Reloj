import tkinter as tk
import zoneinfo as zi
from tkinter import font, simpledialog, colorchooser, messagebox
from dialogo_fuente import DialogoFuente
from dialogo_pais import DialogoPais

def crear_menu_configuracion(app, etiqueta_hora, marco_reloj, config, actualizar_formato):
    fuentes_disponibles = sorted(list(font.families()))
    paises_disponibles = sorted(list(zi.available_timezones()))

    #   Creamos el menú de configuración
    app.menu = tk.Menu(app)
    app.config(menu=app.menu)
    menu_configuracion = tk.Menu(app.menu, tearoff=0)
    app.menu.add_cascade(label="Configuración", menu=menu_configuracion)

    # =======  Funciones internas  =======
    def cambiar_letra():
        dialogo = DialogoFuente(app, fuentes_disponibles, config["letra"][0])
        fuente_elegida = dialogo.resultado
        config["letra"] = (fuente_elegida if fuente_elegida in fuentes_disponibles else min(fuentes_disponibles, key=lambda f: abs(len(f) - len(fuente_elegida)) + sum(c1 != c2 for c1, c2 in zip(f, fuente_elegida))), config["letra"][1])
        if fuente_elegida != config["letra"][0]:
            fuente_parecida = config["letra"][0]
            messagebox.showinfo("Fuente no encontrada", f"La fuente '{fuente_elegida}' no se encontró. Se ha seleccionado la fuente más parecida: '{fuente_parecida}'.")
        etiqueta_hora.config(font=config["letra"])
    
    def cambiar_tamano():
        nuevo_tamano = simpledialog.askinteger("Cambiar tamaño", "Introduce el tamaño de la fuente (ej. 24, 48):")
        if nuevo_tamano:
            etiqueta_hora.pack_configure(pady=(app.winfo_height()-nuevo_tamano)//2)
            alto = 200
            ancho = 323
            if len(etiqueta_hora.cget("text")) == 8:
                if ((etiqueta_hora.winfo_width()*(nuevo_tamano/config["letra"][1])*(11.6/8)) > (ancho - 20)):
                    ancho = int(etiqueta_hora.winfo_width()*(nuevo_tamano/config["letra"][1])*(11.6/8)) + 20
                if (etiqueta_hora.winfo_height()*(nuevo_tamano/config["letra"][1]) > (alto - 50)):
                    alto = int(etiqueta_hora.winfo_height()*(nuevo_tamano/config["letra"][1])) + 50
            else:
                if (etiqueta_hora.winfo_width()*(nuevo_tamano/config["letra"][1]) > (ancho - 20)):
                    ancho = int(etiqueta_hora.winfo_width()*(nuevo_tamano/config["letra"][1])) + 20
                if (etiqueta_hora.winfo_height()*(nuevo_tamano/config["letra"][1]) > (alto - 50)):
                    alto = int(etiqueta_hora.winfo_height()*(nuevo_tamano/config["letra"][1])) + 50
            app.geometry(f"{ancho}x{alto}")
            config["letra"] = (config["letra"][0], nuevo_tamano)
            etiqueta_hora.config(font=config["letra"])
            

    def cambiar_color_texto():
        nuevo_color = colorchooser.askcolor(title="Elige el color del texto")
        if nuevo_color[1]:
            config["color_texto"] = nuevo_color[1]
            etiqueta_hora.config(fg=config["color_texto"])
    
    def cambiar_color_fondo():
        nuevo_color = colorchooser.askcolor(title="Elige el color de fondo")
        if nuevo_color[1]:
            config["color_fondo"] = nuevo_color[1]
            app.configure(bg=config["color_fondo"])
            etiqueta_hora.config(bg=config["color_fondo"])
            marco_reloj.config(bg=config["color_fondo"])

    def cambiar_zona_horaria():
        dialogo = DialogoPais(app, paises_disponibles, config["zona_horaria"])
        zona_elegida = dialogo.resultado
        if zona_elegida:
            if zona_elegida not in paises_disponibles:
                zona_elegida = config["zona_horaria"]
                messagebox.showinfo("Zona horaria no encontrada", f"La zona horaria '{dialogo.resultado}' no se encontró. Se mantiene la zona horaria actual: '{zona_elegida}'.")
            config["zona_horaria"] = zona_elegida
            actualizar_formato()

    def cambiar_formato_hora():
        config["formato_24_horas"] = not config["formato_24_horas"]
        actualizar_formato()
    
    # =======  Añadir opciones al menú  =======

    menu_configuracion.add_command(label="Cambiar fuente", command=cambiar_letra)
    menu_configuracion.add_command(label="Cambiar tamaño", command=cambiar_tamano)
    menu_configuracion.add_command(label="Cambiar color de texto", command=cambiar_color_texto)
    menu_configuracion.add_command(label="Cambiar color de fondo", command=cambiar_color_fondo)

    menu_configuracion.add_separator()

    menu_configuracion.add_command(label="Cambiar zona horaria", command=cambiar_zona_horaria)
    menu_configuracion.add_command(label="Cambiar formato de hora (12/24)", command=cambiar_formato_hora)

    menu_configuracion.add_separator()

    menu_configuracion.add_command(label="Salir", command=app.quit)