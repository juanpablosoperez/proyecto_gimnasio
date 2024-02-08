from tkinter import Tk, Label, Frame, Button, StringVar, filedialog
from tkinter import messagebox
import tkinter as tk
import time
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter import Tk, Label, BOTTOM, LEFT, messagebox


# Lista de nombres de meses en español
meses_espanol = [
    'Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun',
    'Jul', 'Ago', 'Sep', 'Oct', 'Nov', 'Dic'
]

class VentanaInformes:
    def __init__(self, ventana_informes):
        self.window = ventana_informes
        self.window.title("Informes")
        self.window.geometry("980x720")

        # Obtener las dimensiones de la pantalla
        screen_width = ventana_informes.winfo_screenwidth()
        screen_height = ventana_informes.winfo_screenheight()

        # Calcular las coordenadas para centrar la ventana
        x = (screen_width - 980) // 2
        y = (screen_height - 720) // 2

        # Establecer la geometría de la ventana
        ventana_informes.geometry(f"980x720+{x}+{y}")

        self.window.resizable(width=False, height=False)
        self.window.config(bg="#363636", bd=10)

        # Crear el marco principal
        marco_principal = Frame(self.window, bg="#363636")
        marco_principal.pack(side="top", fill="x", pady=10, padx=10, anchor="nw")

        # Botón para regresar a la pantalla principal
        estilo_boton_ppal = {
            "bd": 0,
            "fg": "white",
            "relief": "flat",
            "font": ("Arial", 11),
            "padx": 10,
            "pady": 5,
            "bg": "#363636"
        }

        boton_principal = Button(
            marco_principal,
            text="Pantalla Principal",
            command=self.volver_pantalla_principal,
            **estilo_boton_ppal
        )
        boton_principal.pack(side="left")

        marco_fecha_hora = Frame(self.window, bg="#212121", bd=2, relief="solid")
        marco_fecha_hora.place(relx=1, rely=1, anchor="se", x=-10, y=-10)

        # Etiqueta para la fecha y hora
        self.etiqueta_fecha_hora = Label(marco_fecha_hora, text="", font=("Arial", 12), bg="#212121", fg="#7FFFD4")
        self.etiqueta_fecha_hora.pack(padx=10, pady=5)

        # Actualizar la fecha y hora cada segundo
        self.actualizar_fecha_hora()

        # Agregar el título en negrita centrado sobre el marco de pagos
        titulo_label = Label(self.window, text="INFORMES ESTADÍSTICOS", font=("Arial", 24, "bold"), bg="#363636",
                             fg="#7FFFD4")
        titulo_label.pack(pady=(0, 10))

        # Crear el marco para los botones de Excel y Gráficos
        marco_botones = Frame(self.window, bg="#363636")
        marco_botones.pack(pady=(10, 20))

        # Botones para cargar archivo y generar gráficos
        estilo_boton_ingresar = {
            "bd": 0,
            "fg": "white",
            "relief": "flat",
            "font": ("Arial", 11),
            "padx": 10,
            "pady": 5,
            "bg": "#4CAF50"  # Color verde
        }

        estilo_boton_graficos = {
            "bd": 0,
            "fg": "white",
            "relief": "flat",
            "font": ("Arial", 11),
            "padx": 10,
            "pady": 5,
            "bg": "#2196F3"  # Color azul
        }

        boton_ingresar_excel = Button(
            marco_botones,
            text="Ingresar Excel",
            command=self.cargar_excel,
            **estilo_boton_ingresar
        )
        boton_ingresar_excel.pack(side="left", padx=(0, 10))

        boton_graficos = Button(
            marco_botones,
            text="Generar Gráficos",
            command=self.generar_graficos,
            **estilo_boton_graficos
        )
        boton_graficos.pack(side="left")



        # Variables para almacenar los datos cargados
        self.df = None
        # Variable para almacenar el widget del gráfico
        self.canvas = None

    def actualizar_fecha_hora(self):
        # Obtener la fecha y hora actuales
        now = time.strftime("%d-%m-%Y %H:%M:%S")

        # Actualizar la etiqueta con la fecha y hora actuales
        self.etiqueta_fecha_hora.config(text=now)

        # Llamar a la función nuevamente después de 1000 ms (1 segundo)
        self.window.after(1000,  self.actualizar_fecha_hora)

    def volver_pantalla_principal(self):
        # Cerrar la ventana de informes
        self.window.destroy()

    def cargar_excel(self):


        file_path = filedialog.askopenfilename(
            title="Seleccionar archivo Excel",
            filetypes=[("Archivos Excel", "*.xlsx;*.xls")],
        )

        # Mostrar nuevamente la ventana principal
        self.window.deiconify()

        if file_path:
            # Cargar datos desde el archivo Excel
            self.df = pd.read_excel(file_path)
            print(f"Datos cargados desde: {file_path}")

    def generar_graficos(self):
        if self.df is None:
            messagebox.showerror("Error", "Error: Debes cargar un archivo Excel antes de generar gráficos.")
            return

        # Convertir la columna 'Fecha de Pago' a tipo datetime
        self.df['Fecha de Pago'] = pd.to_datetime(self.df['Fecha de Pago'])

        # Agrupar por mes y contar clientes por mes
        clientes_por_mes = self.df.groupby(self.df['Fecha de Pago'].dt.month).size()

        # Obtener nombres de los meses abreviados en español
        meses_abreviados_espanol = [meses_espanol[int(mes) - 1] for mes in clientes_por_mes.index]

        # Crear y mostrar el gráfico de clientes mensuales
        self.mostrar_grafico(meses_abreviados_espanol, clientes_por_mes.values, 'Clientes por Mes', '',
                             'Cantidad de Clientes')

        # Agrupar por mes y sumar el dinero recaudado por mes
        dinero_por_mes = self.df.groupby(self.df['Fecha de Pago'].dt.month)['Dinero recaudado por mes'].sum()

        # Crear y mostrar el gráfico de dinero recaudado por mes
        self.mostrar_grafico(meses_abreviados_espanol, dinero_por_mes.values, 'Dinero Recaudado por Mes', '', 'Dinero')

        # Mostrar nuevamente la ventana principal
        self.window.deiconify()

    def mostrar_grafico(self, x, y, titulo, etiqueta_x, etiqueta_y):
        plt.figure(figsize=(6, 3))

        plt.plot(x, y, marker='o', color='skyblue', linestyle='-')
        plt.title(titulo)
        plt.xlabel(etiqueta_x)
        plt.ylabel(etiqueta_y)

        plt.gca().yaxis.set_major_locator(MaxNLocator(integer=True))  # Mostrar valores enteros en el eje y

        # Establecer los ticks del eje y como valores enteros
        plt.yticks(range(int(min(y)), int(max(y)) + 1))

        # Incorporar el gráfico en la interfaz de Tkinter
        self.canvas = FigureCanvasTkAgg(plt.gcf(), master=self.window)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack()


if __name__ == "__main__":
    ventana_informes = tk.Tk()
    app_informes = VentanaInformes(ventana_informes)
    ventana_informes.mainloop()