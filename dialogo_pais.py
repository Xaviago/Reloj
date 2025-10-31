import tkinter as tk

class DialogoPais(tk.Toplevel):
    def __init__(self, parent, paises_disponibles, pais_actual):
        super().__init__(parent)
        self.title("Cambiar país")
        self.paises_disponibles = paises_disponibles
        self.resultado = None

        tk.Label(self, text="Introduce el nombre del país:").pack(padx=10, pady=5)
        self.entrada = tk.Entry(self)
        self.entrada.insert(0, pais_actual)
        self.entrada.pack(padx=10, pady=5, fill="x")
        self.entrada.bind("<KeyRelease>", self.actualizar_sugerencias)
        self.entrada.bind("<Tab>", self.autocompletar)
        self.entrada.bind("<Down>", lambda e: self.lista_sugerencias.focus_set())
        self.entrada.bind("<Up>", lambda e: self.entrada.focus_set())

        self.lista_sugerencias = tk.Listbox(self, height=5)
        self.lista_sugerencias.pack(padx=10, pady=5, fill="both", expand=True)
        self.lista_sugerencias.bind("<Double-Button-1>", self.seleccionar_sugerencia)
        self.lista_sugerencias.bind("<Return>", self.seleccionar_sugerencia)

        tk.Button(self, text="Aceptar", command=self.aceptar).pack(pady=5)
        self.actualizar_sugerencias()

        self.entrada.focus_set()
        self.grab_set()
        self.wait_window()

    def actualizar_sugerencias(self, event=None):
        texto = self.entrada.get().lower()
        self.lista_sugerencias.delete(0, tk.END)
        for pais in self.paises_disponibles:
            if texto in pais.lower():
                self.lista_sugerencias.insert(tk.END, pais)
        if self.lista_sugerencias.size() > 0:
            self.lista_sugerencias.selection_set(0)
    
    def autocompletar(self, event=None):
        if self.lista_sugerencias.size() > 0:
            sugerencia = self.lista_sugerencias.get(0)
            self.entrada.delete(0, tk.END)
            self.entrada.insert(0, sugerencia)
        return "break"
    
    def seleccionar_sugerencia(self, event=None):
        if self.lista_sugerencias.curselection():
            pais = self.lista_sugerencias.get(self.lista_sugerencias.curselection())
            self.entrada.delete(0, tk.END)
            self.entrada.insert(0, pais)
            self.aceptar()
    
    def aceptar(self):
        texto = self.entrada.get()
        for pais in self.paises_disponibles:
            if pais.lower() == texto.lower():
                texto = pais
                break
        self.resultado = texto
        self.destroy()