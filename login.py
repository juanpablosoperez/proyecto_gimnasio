import tkinter as tk
from tkinter import ttk
from ttkthemes import ThemedStyle
from tkinter import messagebox
from tkinter import simpledialog, Label, LabelFrame, Entry,Frame, Button
from exportar_excel import VentanaExportar
from pagos import VentanaPagos
from informes import VentanaInformes
from rutinas import VentanaRutinas
from sqlite import *
import sqlite3
import principal
from PIL import ImageTk, Image



class Login:
    def __init__(self, ventana_login):
        self.window = ventana_login
        self.window.title("Inicio de Sesión")
        self.window.geometry("330x250")

        # Centrar la ventana en la pantalla
        screen_width = self.window.winfo_screenwidth()
        screen_height = self.window.winfo_screenheight()
        x = (screen_width - 330) // 2
        y = (screen_height - 370) // 2

        self.window.geometry(f"330x370+{x}+{y}")
        self.window.resizable(width=False, height=False)
        self.window.config(bg="#363636", bd=10)  # Cambiar el color de fondo a gris oscuro

        # TITULO
        titulo = Label(ventana_login, text="INICIO DE SESIÓN", fg="#7FFFD4", bg="#363636", font=("Arial", 13, "bold"), pady=10)
        titulo.pack()

        # LOGO LOGIN
        imagen_login = Image.open("C:\\Users\\JUAMPI\\Desktop\\Mis_Entornos\\proyecto_gimnasio\\proyecto_gimnasio\\images\\weightlifter.png")
        nueva_imagen = imagen_login.resize((40,40),resample=Image.BICUBIC)
        render = ImageTk.PhotoImage(nueva_imagen)
        label_imagen = Label(ventana_login, image=render, bg="#363636")
        label_imagen.image = render
        label_imagen.pack(pady=5)

        # MARCO
        marco = LabelFrame(ventana_login, text="Ingrese sus datos", font=("Arial", 11, "bold"), bg="#363636", fg="#7FFFD4")
        marco.config(bd=2)
        marco.pack()

        # FORMULARIO
        label_usuario = Label(marco, text="Usuario: ", font=("Arial", 11, "bold"), bg="#363636", fg="#7FFFD4")
        label_usuario.grid(row=0, column=0, sticky="s", padx=5, pady=10)
        self.usuario_login = Entry(marco,font=("Arial", 11, "bold"), width=20, bg="#9EB0AB", fg="black")  # Cambiar el color de fondo del Entry a gris claro y el color del texto a blanco
        self.usuario_login.focus()
        self.usuario_login.grid(row=0, column=1, padx=5, pady=10)

        label_contrasena = Label(marco, text="Contraseña: ", font=("Arial", 11, "bold"), bg="#363636", fg="#7FFFD4")
        label_contrasena.grid(row=1, column=0, sticky="s", padx=10, pady=10)
        self.contrasena_login = Entry(marco,font=("Arial", 11, "bold"), width=20, show="*", bg="#9EB0AB", fg="black")  # Cambiar el color de fondo del Entry a gris claro y el color del texto a blanco
        self.contrasena_login.grid(row=1, column=1, padx=10, pady=10)
        self.contrasena_login.bind("<Return>", self.Login)  # Asociar la tecla "Enter" a la función Login

        # FRAME BOTONES
        frame_botones = Frame(ventana_login, bg="#363636")
        frame_botones.pack()

        # BOTONES
        boton_ingresar = Button(frame_botones, text="INGRESAR", command=self.Login, height=2, width=12, fg="black",
                                font=("Arial", 11, "bold"))
        boton_ingresar.configure(bg="#7FFFD4")  # Cambiar el color de fondo del botón a verde agua
        boton_ingresar.grid(row=0, column=1, padx=10, pady=15)

        # Bind arrow keys for navigation between Entry widgets
        self.usuario_login.bind("<Down>", lambda e: self.contrasena_login.focus_set())
        self.contrasena_login.bind("<Up>", lambda e: self.usuario_login.focus_set())

    def limpiar_login(self):
        if self.usuario_login.winfo_exists():
            self.usuario_login.delete(0, END)
            self.contrasena_login.delete(0, END)

    def abrir_pantalla_principal(self):
        if self.window.winfo_exists():
            self.window.destroy()  # Cerrar la ventana de inicio de sesión
            ventana_principal = tk.Tk()
            aplicacion = principal.VentanaPrincipal(ventana_principal)
            ventana_principal.mainloop()

    def Login(self, event=None):
        try:
            usuario = self.usuario_login.get()
            contrasena = self.contrasena_login.get()
            if usuario == "admin" and contrasena == "admin":
                self.abrir_pantalla_principal()
            else:
                messagebox.showerror("ERROR DE INGRESO", "Usuario o contraseña incorrecto.")
        except:
            messagebox.showerror("ERROR", "Ha ocurrido un error, reinicie el programa.")
            self.limpiar_login()

if __name__ == "__main__":
    ventana_login = tk.Tk()
    aplicacion = Login(ventana_login)
    ventana_login.mainloop()