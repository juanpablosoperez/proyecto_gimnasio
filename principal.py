from tkinter import *
from tkinter.font import Font
import time
from tkinter import ttk
from tkinter import messagebox
from tkinter import simpledialog
from tkinter import Tk, Label, BOTTOM, LEFT, messagebox
import  tkinter as tk
from exportar_excel import VentanaExportar
from pagos import VentanaPagos
from informes import VentanaInformes
from rutinas import VentanaRutinas
import sqlite3
from tkinter import PhotoImage
import os


class Cliente:
    def __init__(self, nombre, apellido, domicilio, telefono, estado, dni, actividad):
        self.nombre = nombre
        self.apellido = apellido
        self.domicilio = domicilio
        self.telefono = telefono
        self.estado = estado
        self.dni = dni
        self.actividad = actividad



class VentanaPrincipal:
    def __init__(self, ventana_principal):
        self.window = ventana_principal
        self.window.title("Gimnasio")
        self.window.geometry("980x720")

        # Obtener las dimensiones de la pantalla
        screen_width = ventana_principal.winfo_screenwidth()
        screen_height = ventana_principal.winfo_screenheight()

        # Calcular las coordenadas para centrar la ventana
        x = (screen_width - 980) // 2
        y = (screen_height - 720) // 2

        # Establecer la geometría de la ventana
        ventana_principal.geometry(f"980x720+{x}+{y}")

        self.window.resizable(width=False, height=False)
        self.window.config(bg="#363636", bd=10)


        # Variable de instancia para almacenar el índice del elemento seleccionado
        self.indice_seleccionado = None

        # Crear el marco principal
        marco_principal = Frame(self.window, bg="#363636")
        marco_principal.place(relx=0.5, rely=0.5, anchor="center", relwidth=1, relheight=1)

        # Agregar el título en negrita
        titulo_font = Font(family="Arial", size=24, weight="bold")
        titulo_label = Label(marco_principal, text="GESTIÓN DE MIEMBROS", font=titulo_font, bg="#363636", fg="#7FFFD4")
        titulo_label.pack(pady=(70, 30))  # Ajusta el valor de pady según sea necesario

        # Crear el frame para la información del miembro
        frame_informacion = LabelFrame(marco_principal, text="Información del Miembro", font=("Comic Sans", 14, "bold"),
                                       bg="#363636", fg="#7FFFD4", padx=20, pady=10)
        frame_informacion.pack(side="top", fill="both", expand=True)


        # Etiqueta y campo de entrada para el cliente
        self.nombre_entry = self.crear_label_entry(frame_informacion, "Nombre:", row=1, color="#7FFFD4", rely=0.3)
        self.apellido_entry = self.crear_label_entry(frame_informacion, "Apellido:", row=2, color="#7FFFD4", rely=0.4)
        self.dni_entry = self.crear_label_entry(frame_informacion, "DNI:", row=3, color="#7FFFD4", rely=0.5)

        # Crear el marco para la tabla
        marco_tabla = Frame(frame_informacion, bg="#363636")
        marco_tabla.grid(row=4, column=0, columnspan=2, pady=10, sticky="ew")

        # Crear la tabla
        self.crear_tabla(marco_tabla)

        # Crear el marco del menú
        marco_menu = Frame(frame_informacion, bg="#363636")

        # Ruta de la carpeta de imágenes
        ruta_imagenes = os.path.join(os.getcwd(), "images")

        # Nombres de archivo de las imágenes
        nombres_imagenes = [
            "find.png",
            "refresh.png",
            "registered1.png",
            "remove.png"
        ]

        # Lista de rutas de archivo completas para las imágenes
        rutas_imagenes = [os.path.join(ruta_imagenes, nombre) for nombre in nombres_imagenes]

        # Cargar las imágenes
        self.render = [PhotoImage(file=ruta) for ruta in rutas_imagenes]

        # Crear los botones del menú con fondo blanco
        self.crear_boton(marco_menu, self.render[0], self.funcion_buscar, bg="#4CAF50")  # Verde
        self.crear_boton(marco_menu, self.render[1], self.funcion_actualizar, bg="#2196F3")  # Azul
        self.crear_boton(marco_menu, self.render[2], self.funcion_registrar, bg="#E4EE10")  # Amarillo
        self.crear_boton(marco_menu, self.render[3], self.funcion_eliminar, bg="#FF5722")  # Rojo

        # Colocar el marco del menú a la derecha de frame_informacion
        marco_menu.grid(row=0, column=3, sticky="nsew", padx=10)

        # Crear el marco para la fecha y hora
        marco_fecha_hora = Frame(self.window, bg="#212121", bd=2, relief=SOLID)
        marco_fecha_hora.place(relx=1, rely=1, anchor="se", x=-10, y=-10)

        # Etiqueta para la fecha y hora
        self.etiqueta_fecha_hora = Label(marco_fecha_hora, text="", font=("Arial", 12), bg="#212121", fg="#7FFFD4")
        self.etiqueta_fecha_hora.pack(padx=10, pady=5)

        # Actualizar la fecha y hora cada segundo
        self.actualizar_fecha_hora()

        # Crear el marco para las imágenes
        marco_imagen = Frame(self.window, bg="#363636")
        marco_imagen.place(relx=0, rely=1, anchor="sw", x=10, y=-10)

        # Cargar la primera imagen
        imagen_path1 = "C:\\Users\\JUAMPI\\Desktop\\Mis_Entornos\\proyecto_gimnasio\\proyecto_gimnasio\\images\\weightlift (4).png"
        imagen1 = PhotoImage(file=imagen_path1)

        # Crear un widget Label para mostrar la primera imagen
        label_imagen1 = Label(marco_imagen, image=imagen1, bg="#363636")
        label_imagen1.image = imagen1
        label_imagen1.pack(side="left", padx=10)

        # Cargar la segunda imagen
        imagen_path2 = "C:\\Users\\JUAMPI\\Desktop\\Mis_Entornos\\proyecto_gimnasio\\proyecto_gimnasio\\images\\weightlift (5).png"
        imagen2 = PhotoImage(file=imagen_path2)

        # Crear un widget Label para mostrar la segunda imagen
        label_imagen2 = Label(marco_imagen, image=imagen2, bg="#363636")
        label_imagen2.image = imagen2
        label_imagen2.pack(side="left", padx=10)

        # Cargar la tercera imagen
        imagen_path3 = "C:\\Users\\JUAMPI\\Desktop\\Mis_Entornos\\proyecto_gimnasio\\proyecto_gimnasio\\images\\weightlift (3).png"
        imagen3 = PhotoImage(file=imagen_path3)

        # Crear un widget Label para mostrar la tercera imagen
        label_imagen3 = Label(marco_imagen, image=imagen3, bg="#363636")
        label_imagen3.image = imagen3
        label_imagen3.pack(side="left", padx=10)

        # Crear el marco para la barra de navegación
        marco_vistas = Frame(self.window, bg="#363636")
        marco_vistas.place(relx=0, rely=0, anchor="nw", relwidth=0.8)

        # Crear la barra de navegación
        self.crear_barra_navegacion(marco_vistas, exclude=("Clientes",), relwidth=1)

        # Enlazar la tecla Intro/Enter con la función de registro
        self.window.bind('<Return>', self.funcion_registrar)

        # Vincular las teclas de flecha arriba y flecha abajo a funciones para cambiar el enfoque entre campos de entrada
        self.nombre_entry.bind("<Up>", lambda event: self.cambiar_enfoque(-1))
        self.nombre_entry.bind("<Down>", lambda event: self.cambiar_enfoque(1))
        self.apellido_entry.bind("<Up>", lambda event: self.cambiar_enfoque(-1))
        self.apellido_entry.bind("<Down>", lambda event: self.cambiar_enfoque(1))
        self.dni_entry.bind("<Up>", lambda event: self.cambiar_enfoque(-1))
        self.dni_entry.bind("<Down>", lambda event: self.cambiar_enfoque(1))

        # Asociar la función seleccionar_cliente al evento de clic en la tabla
        self.tabla.bind("<ButtonRelease-1>", self.seleccionar_cliente)

        # Variable de instancia para almacenar los datos actuales
        self.datos_actuales = None

        self.nuevo_nombre = StringVar()
        self.nuevo_apellido = StringVar()
        self.nuevo_dni = StringVar()
        self.nuevo_telefono = StringVar()
        self.nuevo_domicilio = StringVar()
        self.nueva_actividad = StringVar()
        self.nuevo_estado = StringVar()


    def cambiar_enfoque(self, direccion):
        # Obtener todos los campos de entrada
        campos_entrada = [self.nombre_entry, self.apellido_entry, self.dni_entry]

        # Obtener el índice del campo de entrada actual
        indice_actual = campos_entrada.index(self.window.focus_get())

        # Calcular el nuevo índice después de moverse en la dirección especificada
        nuevo_indice = (indice_actual + direccion) % len(campos_entrada)

        # Cambiar el enfoque al nuevo campo de entrada
        campos_entrada[nuevo_indice].focus()


    def siguiente_campo_entrada(self):
        campos_entrada = [self.nombre_entry, self.apellido_entry, self.dni_entry]
        if self.indice_seleccionado is not None:
            indice_siguiente = (self.indice_seleccionado + 1) % len(campos_entrada)
            campos_entrada[indice_siguiente].focus()

    def anterior_campo_entrada(self):
        campos_entrada = [self.nombre_entry, self.apellido_entry, self.dni_entry]
        if self.indice_seleccionado is not None:
            indice_anterior = (self.indice_seleccionado - 1) % len(campos_entrada)
            campos_entrada[indice_anterior].focus()



    def actualizar_fecha_hora(self):
        # Obtener la fecha y hora actuales
        now = time.strftime("%d-%m-%Y %H:%M:%S")

        # Actualizar la etiqueta con la fecha y hora actuales
        self.etiqueta_fecha_hora.config(text=now)

        # Llamar a la función nuevamente después de 1000 ms (1 segundo)
        self.window.after(1000, self.actualizar_fecha_hora)

    def crear_label_entry(self, frame, text, row, color, rely=None, is_integer=False):
        label = Label(frame, text=text, font=("Comic Sans", 12, "bold"), bg="#363636", fg=color)
        label.grid(row=row, column=0, padx=(10), pady=(10), sticky="e")

        if is_integer:
            entry_var = IntVar()
            entry = Entry(frame, font=("Comic Sans", 12), textvariable=entry_var, width=325, bd=3, relief="solid")
        else:
            entry = Entry(frame, font=("Comic Sans", 12), width=25, bd=3, relief="solid")

        entry.grid(row=row, column=1, padx=(10), pady=5, sticky="w")  # Ajuste en el padx de la entrada
        entry.configure(bg="#FFFFFF", fg="#000000", font=("Comic Sans", 12, "bold"))

        if rely is not None:
            frame.rowconfigure(row, minsize=30)  # Ajusta la altura de la fila según sea necesario
            label.grid_configure(pady=(0, 5), sticky="e")
            entry.grid_configure(pady=(0, 5), sticky="w")
            entry.grid(row=row, column=1, padx=10, pady=(0, 5),
                       sticky="w")  # Ajuste en el padx de la entrada
        else:
            frame.rowconfigure(row, minsize=30)

        frame.grid_columnconfigure(1, weight=1)
        return entry

    def crear_boton(self, frame, imagen, command, bg):
        boton = Button(frame, image=imagen, command=command, bd=0, bg=bg, activebackground=bg)
        boton.grid(row=0, column=frame.grid_size()[0], padx=10)

    def crear_tabla(self, marco_tabla):
        # Crear el widget Treeview
        self.tabla = ttk.Treeview(marco_tabla, columns=("ID Cliente", "Nombre", "Apellido", "DNI",  "Domicilio","Teléfono", "Estado","Actividad"), show="headings",
                             height=5)

        # Configurar las columnas
        self.tabla.heading("ID Cliente", text="ID Cliente")
        self.tabla.heading("Nombre", text="Nombre")
        self.tabla.heading("Apellido", text="Apellido")
        self.tabla.heading("DNI", text="DNI")
        self.tabla.heading("Domicilio", text="Domicilio")
        self.tabla.heading("Teléfono", text="Teléfono")
        self.tabla.heading("Estado", text="Estado")
        self.tabla.heading("Actividad", text="Actividad")

        # Ajustar el ancho de las columnas
        ancho_columnas = [60, 100, 100, 60, 100,80, 80,60]
        for i, ancho in enumerate(ancho_columnas):
            self.tabla.column(self.tabla['columns'][i], width=ancho, anchor="center")


        # Asociar el evento de clic en la tabla a la función que captura el índice
        self.tabla.bind("<ButtonRelease-1>", self.obtener_seleccion_tabla)


        # Estilo para la tabla
        estilo_tabla = ttk.Style()
        estilo_tabla.theme_use("clam")
        estilo_tabla.configure("Treeview", background="#363636", fieldbackground="#363636", foreground="#7FFFD4")
        estilo_tabla.configure("Treeview.Heading", font=("Arial", 12, "bold"), background="#363636", foreground="#7FFFD4")
        estilo_tabla.map("Treeview", background=[('selected', '#0075C2')])

        # Mostrar la tabla
        self.tabla.grid(row=0, column=0, sticky="nsew")
        marco_tabla.rowconfigure(0, weight=1)
        marco_tabla.columnconfigure(0, weight=1)
        marco_tabla.place(relx=0, rely=0.4, anchor="nw", relwidth=1, relheight=0.45)

    def cargar_tabla(self):
        # Limpiar la tabla
        self.tabla.delete(*self.tabla.get_children())

        # Obtener todos los clientes desde la base de datos real
        query = "SELECT * FROM Clientes"
        resultados = c.execute(query).fetchall()

        # Mostrar los resultados en la tabla
        for resultado in resultados:
            self.tabla.insert("", "end", values=resultado)

    def obtener_seleccion_tabla(self, event):
        # Obtener el índice del elemento seleccionado
        item = self.tabla.selection()
        if item:
            # Obtener el ID del cliente directamente del elemento
            id_cliente = self.tabla.item(item, 'values')[0]
            # Actualizar el ID del cliente seleccionado
            self.indice_seleccionado = id_cliente

    def crear_barra_navegacion(self, marco_vistas, exclude=(), relwidth=0.8):
        # Crear el marco de la barra de navegación
        marco_navegacion = Frame(marco_vistas, bg="#363636")
        marco_navegacion.pack(side=TOP, fill=X, pady=10)

        # Crear los botones de navegación
        botones_info = [
            ("Pagos", self.mostrar_vista_pagos),
            ("Exportar Excel", self.mostrar_vista_exportar_excel),
            ("Informes Estadísticos", self.mostrar_vista_informes),
            ("Rutinas", self.mostrar_vista_rutinas)
        ]

        for i, (text, command) in enumerate(botones_info):
            if text not in exclude:
                boton = Button(
                    marco_navegacion,
                    text=text,
                    command=command,
                    bg="#363636",
                    bd=0,
                    fg="white",
                    activeforeground="white",  # Color del texto cuando se presiona el botón
                    activebackground="#7FFFD4",  # Color de fondo cuando se presiona el botón
                    relief=FLAT,  # Quitar el efecto de relieve al presionar el botón
                    font=("Arial", 11),  # Fuente del texto del botón
                    padx=10,  # Espacio horizontal interno del botón
                    pady=5  # Espacio vertical interno del botón
                )
                boton.pack(side=LEFT)

        marco_vistas.place(relx=0, rely=0, anchor="nw", relwidth=relwidth)



    def mostrar_vista_informes(self):
        ventana_informes = Tk()
        # Ocultar la ventana principal
        self.window.withdraw()
        app_informes = VentanaInformes(ventana_informes)
        ventana_informes.wait_window()
        # Mostrar nuevamente la ventana principal
        self.window.deiconify()

    def mostrar_vista_exportar_excel(self):
        ventana_exportar = Tk()
        # Ocultar la ventana principal
        self.window.withdraw()
        app_exportar = VentanaExportar(ventana_exportar)
        ventana_exportar.wait_window()
        # Mostrar nuevamente la ventana principal
        self.window.deiconify()


    def mostrar_vista_rutinas(self):
        # Ocultar la ventana principal
        self.window.withdraw()
        ventana_rutinas = VentanaRutinas(self.window)


    def cerrar_ventana_rutinas(self, ventana_rutinas):
        # Acciones a realizar antes de cerrar la ventana de rutinas
        app_rutinas.destroy()
        # Por ejemplo, destruir la ventana
        ventana_rutinas.destroy()

    def mostrar_vista_pagos(self):
        # Crea una instancia de la ventana de pagos
        ventana_pagos = Tk()
        # Ocultar la ventana principal
        self.window.withdraw()
        app_pagos = VentanaPagos(ventana_pagos)

        # Espera hasta que se cierre la ventana de pagos
        ventana_pagos.wait_window()

        # Mostrar nuevamente la ventana principal
        self.window.deiconify()



    def funcion_buscar(self):
        # Crear una nueva conexión y cursor
        conn = sqlite3.connect("gimnasio.db")
        c = conn.cursor()

        # Obtener valores de los Entry
        nombre = self.nombre_entry.get().strip().lower()
        apellido = self.apellido_entry.get().strip().lower()
        dni = self.dni_entry.get().strip().lower()

        # Limpiar la tabla
        self.tabla.delete(*self.tabla.get_children())

        try:
            # Ejecutar consulta SQL para buscar coincidencias
            query = "SELECT * FROM Clientes WHERE lower(nombre) LIKE ? AND lower(apellido) LIKE ? AND lower(dni) LIKE ?"
            resultados = c.execute(query, ('%' + nombre + '%', '%' + apellido + '%', '%' + dni + '%')).fetchall()

            # Mostrar los resultados en la tabla
            for resultado in resultados:
                self.tabla.insert("", "end", values=resultado)

            # Mostrar mensaje si no se encontraron resultados
            if not resultados:
                messagebox.showinfo("Búsqueda", "No se encontraron resultados.")

        finally:
            # Cerrar la conexión
            conn.close()

    def seleccionar_cliente(self, event):
        item_seleccionado = self.tabla.selection()
        if item_seleccionado:
            self.indice_seleccionado = item_seleccionado[0]
            #print(f"Ítem seleccionado: {self.indice_seleccionado}")
            # Eliminar el primer carácter "I" del id_cliente
            id_cliente = self.indice_seleccionado[1:]
            self.datos_actuales = self.obtener_datos_cliente(id_cliente)
            print(f"Datos actuales: {self.datos_actuales}")

    def funcion_actualizar(self):
        if self.indice_seleccionado:
            item_seleccionado = self.tabla.item(self.indice_seleccionado)
            if 'values' in item_seleccionado:
                id_cliente = item_seleccionado['values'][0]
                self.datos_actuales = self.obtener_datos_cliente(id_cliente)

                nuevo_nombre = StringVar()
                nuevo_apellido = StringVar()
                nuevo_dni = StringVar()
                nuevo_domicilio = StringVar()
                nuevo_telefono = StringVar()
                nueva_actividad = StringVar()
                nuevo_estado = StringVar()

                # Crear una nueva ventana para la actualización
                self.ventana_actualizar = Toplevel(self.window)
                self.ventana_actualizar.title("Actualizar Usuario")
                self.ventana_actualizar.geometry("400x320")
                self.ventana_actualizar.resizable(width=False, height=False)

                # Obtener las dimensiones de la pantalla
                screen_width = self.window.winfo_screenwidth()
                screen_height = self.window.winfo_screenheight()

                # Calcular las coordenadas para centrar la ventana de actualización
                x = (screen_width - 400) // 2
                y = (screen_height - 320) // 2

                self.ventana_actualizar.geometry(f"400x320+{x}+{y}")  # Ajusta el tamaño y posición de la ventana
                self.ventana_actualizar.resizable(width=False, height=False)

                # Aplicar estilo similar al de la pantalla principal
                self.ventana_actualizar.config(bg="#363636", bd=8)

                # Etiquetas para los campos
                self.crear_label_entry(self.ventana_actualizar, "Nombre:", 1, "#7FFFD4", rely=0.1)
                self.crear_label_entry(self.ventana_actualizar, "Apellido:", 2, "#7FFFD4", rely=0.2)
                self.crear_label_entry(self.ventana_actualizar, "DNI:", 3, "#7FFFD4", rely=0.3)
                self.crear_label_entry(self.ventana_actualizar, "Domicilio:", 4, "#7FFFD4", rely=0.4)
                self.crear_label_entry(self.ventana_actualizar, "Teléfono:", 5, "#7FFFD4", rely=0.5)
                self.crear_label_entry(self.ventana_actualizar, "Estado:", 6, "#7FFFD4", rely=0.6)
                self.crear_label_entry(self.ventana_actualizar, "Actividad:", 7, "#7FFFD4", rely=0.7)


                # Crear el combobox de actividad vacío
                combobox_nueva_actividad = ttk.Combobox(self.ventana_actualizar, textvariable=nueva_actividad,
                                                        values=[], state='readonly', font=("Arial", 12, "bold"),
                                                        width=23,height=15)
                # Configurar el estilo visual similar al de los Entry
                combobox_nueva_actividad.config(style="Custom.TCombobox")

                # Crear un nuevo estilo para el Combobox
                style = ttk.Style()
                style.configure("Custom.TCombobox", padding=5, background="#9EB0AB", foreground="black", borderwidth=3,
                                relief="solid")

                # Utilizar Entry directamente para crear campos de entrada con variables asociadas
                entry_nuevo_nombre = Entry(self.ventana_actualizar, font=("Arial", 12, "bold"), bg="#9EB0AB",
                                           fg="black", textvariable=nuevo_nombre, width=25, bd=3, relief="solid")
                entry_nuevo_apellido = Entry(self.ventana_actualizar, font=("Arial", 12, "bold"), bg="#9EB0AB",
                                             fg="black", textvariable=nuevo_apellido, width=25, bd=3, relief="solid")
                entry_nuevo_dni = Entry(self.ventana_actualizar, font=("Arial", 12, "bold"), bg="#9EB0AB", fg="black",
                                        textvariable=nuevo_dni, width=25, bd=3, relief="solid")
                entry_nuevo_telefono = Entry(self.ventana_actualizar, font=("Arial", 12, "bold"), bg="#9EB0AB",
                                             fg="black", textvariable=nuevo_telefono, width=25, bd=3, relief="solid")
                entry_nuevo_domicilio = Entry(self.ventana_actualizar, font=("Arial", 12, "bold"), bg="#9EB0AB",
                                              fg="black", textvariable=nuevo_domicilio, width=25, bd=3, relief="solid")
                entry_nuevo_estado = Entry(self.ventana_actualizar, font=("Arial", 12, "bold"), bg="#9EB0AB",
                                           fg="black", textvariable=nuevo_estado, width=25, bd=3, relief="solid")

                # Asignar valores recuperados a las variables StringVar
                nuevo_nombre.set(self.datos_actuales[1])
                nuevo_apellido.set(self.datos_actuales[2])
                nuevo_dni.set(str(self.datos_actuales[3]))  # Convertir a cadena si es necesario
                nuevo_domicilio.set(self.datos_actuales[4])
                nuevo_telefono.set(str(self.datos_actuales[5]))
                nueva_actividad.set(self.datos_actuales[6])
                nuevo_estado.set(self.datos_actuales[7])

                # Colocar los widgets en la ventana
                entry_nuevo_nombre.grid(row=1, column=1, padx=(10), pady=5, sticky="w")
                entry_nuevo_apellido.grid(row=2, column=1, padx=(10), pady=5, sticky="w")
                entry_nuevo_dni.grid(row=3, column=1, padx=(10), pady=5, sticky="w")
                entry_nuevo_domicilio.grid(row=4, column=1, padx=(10), pady=5, sticky="w")
                entry_nuevo_telefono.grid(row=5, column=1, padx=(10), pady=5, sticky="w")
                entry_nuevo_estado.grid(row=6, column=1, padx=(10), pady=5, sticky="w")
                combobox_nueva_actividad.grid(row=7, column=1, padx=(10), pady=5, sticky="w")

                # Crear el botón de actualizar
                boton_actualizar = Button(self.ventana_actualizar, text="Actualizar",
                                          command=lambda: self.actualizar_datos(
                                              nuevo_nombre.get(), nuevo_apellido.get(), nuevo_dni.get(),
                                               nuevo_domicilio.get(),nuevo_telefono.get(), nueva_actividad.get(),
                                              nuevo_estado.get(), self.datos_actuales[0]  # idCliente
                                          ), fg="black", font=("Arial", 11, "bold"))
                boton_actualizar.configure(bg="#7FFFD4")
                boton_actualizar.grid(row=8, column=1, pady=10)

                # Obtener las actividades disponibles y configurar el combobox
                actividades = self.obtener_nombres_actividades()
                combobox_nueva_actividad['values'] = actividades

    def obtener_nombres_actividades(self):
        try:
            with sqlite3.connect("gimnasio.db") as conn:
                c = conn.cursor()
                c.execute("SELECT nombreActividad FROM actividad")
                nombres_actividades = [row[0] for row in c.fetchall()]
                return nombres_actividades
        except sqlite3.Error as error:
            print("Error al obtener nombres de actividades:", error)
            return []


    def obtener_datos_cliente(self, id_cliente):
        with sqlite3.connect("gimnasio.db") as conn:
            c = conn.cursor()
            id_cliente = int(id_cliente)
            query = "SELECT idCliente, nombre, apellido, dni,  domicilio,telefono,idActividad, estado FROM Clientes WHERE idCliente = ? LIMIT 1"
            datos_cliente = c.execute(query, (id_cliente,)).fetchone()
            print(f"Datos recuperados para el cliente {id_cliente}: {datos_cliente}")
        return datos_cliente

    def abrir_ventana_actualizar(self):
        if self.indice_seleccionado:
            self.funcion_actualizar()

    def actualizar_datos(self, nuevo_nombre, nuevo_apellido, nuevo_dni, nuevo_telefono, nuevo_domicilio,nueva_actividad, nuevo_estado,
                         id_cliente):
        try:
            with sqlite3.connect("gimnasio.db") as conn:
                c = conn.cursor()
                query = "UPDATE Clientes SET nombre=?, apellido=?, dni=?,  domicilio=?,telefono=?, idActividad=?, estado=? WHERE idCliente=?"
                c.execute(query, (
                nuevo_nombre, nuevo_apellido, nuevo_dni,  nuevo_domicilio,nuevo_telefono,nueva_actividad, nuevo_estado, id_cliente))
            # Recargar la tabla
            self.cargar_tabla()
            # Cerrar la ventana de actualización
            self.ventana_actualizar.destroy()
        except Exception as e:
            print("Error al actualizar datos:", e)




    def funcion_eliminar(self):
        # Obtener el índice seleccionado del Treeview
        seleccion = self.tabla.selection()

        # Verificar si se ha seleccionado un elemento
        if seleccion:
            # Obtener el índice del elemento seleccionado
            indice_seleccionado = self.tabla.index(seleccion[0])

            # Verificar que el índice está dentro de los límites válidos
            if 0 <= indice_seleccionado < len(self.tabla.get_children()):
                # Obtener el ítem seleccionado
                item_seleccionado = self.tabla.item(seleccion[0])

                # Verificar si el ítem tiene 'values'
                if 'values' in item_seleccionado:
                    # Obtener el ID del cliente seleccionado
                    id_cliente = item_seleccionado['values'][0]

                    # Crear ventana emergente de confirmación
                    self.ventana_confirmacion = Toplevel(self.window)
                    self.ventana_confirmacion.title("Confirmación de Eliminación")
                    self.ventana_confirmacion.geometry("450x150")
                    self.ventana_confirmacion.resizable(width=False, height=False)


                    # Obtener las dimensiones de la pantalla
                    screen_width = self.window.winfo_screenwidth()
                    screen_height = self.window.winfo_screenheight()

                    # Calcular las coordenadas para centrar la ventana de actualización
                    x = (screen_width - 450) // 2
                    y = (screen_height - 150) // 2

                    self.ventana_confirmacion.geometry(f"450x150+{x}+{y}")  # Ajusta el tamaño y posición de la ventana
                    self.ventana_confirmacion.resizable(width=False, height=False)
                    self.ventana_confirmacion.config(bg="#363636", bd=10)

                    # Obtener datos del cliente seleccionado
                    conn = sqlite3.connect("gimnasio.db")
                    c = conn.cursor()
                    query = "SELECT nombre, apellido FROM Clientes WHERE idCliente = ?"
                    cliente_seleccionado = c.execute(query, (id_cliente,)).fetchone()

                    # Etiqueta para el mensaje de confirmación
                    mensaje_confirmacion = f"¿Deseas eliminar al miembro {cliente_seleccionado[0]} {cliente_seleccionado[1]}?"
                    etiqueta_confirmacion = Label(self.ventana_confirmacion, text=mensaje_confirmacion,
                                                      font=("Arial", 12, "bold"),
                                                      bg="#363636", fg="#7FFFD4")
                    etiqueta_confirmacion.pack(pady=20, padx=5)

                    # Botones de confirmación y cancelación
                    boton_si = Button(self.ventana_confirmacion, text="Sí",
                                          command=lambda: self.confirmar_eliminacion(id_cliente),
                                          fg="black", font=("Arial", 12, "bold"), bg="#7FFFD4")
                    boton_si.pack(side=LEFT, padx=15)

                    boton_no = Button(self.ventana_confirmacion, text="No", command=self.ventana_confirmacion.destroy,
                                          fg="black",
                                          font=("Arial", 12, "bold"), bg="#7FFFD4")
                    boton_no.pack(side=LEFT, padx=15)
                else:
                    print("El ítem seleccionado no tiene 'values'.")
                    messagebox.showerror("Error", "El ítem seleccionado no tiene valores asociados.")
            else:
                print("Índice seleccionado fuera de los límites válidos.")
                messagebox.showerror("Error", "El índice seleccionado no es válido.")
        else:
            print("Ningún elemento seleccionado.")
            messagebox.showerror("Error", "Ningún elemento seleccionado.")


    def confirmar_eliminacion(self, id_cliente):
        # Eliminar cliente de la base de datos
        conn = sqlite3.connect("gimnasio.db")
        c = conn.cursor()

        try:
            # Eliminar cliente de la base de datos
            with sqlite3.connect("gimnasio.db") as conn:
                c = conn.cursor()
                query = "DELETE FROM Clientes WHERE idCliente = ?"
                c.execute(query, (id_cliente,))
                conn.commit()
                #print("Eliminación exitosa para ID Cliente:", id_cliente)

        except Exception as e:
            print("Error al intentar eliminar:", e)

        finally:
            # Cerrar la ventana emergente
            self.ventana_confirmacion.destroy()

            # Actualizar la tabla después de la eliminación
            self.cargar_tabla()

            # No necesitas cerrar la conexión aquí, ya que estás usando 'with' para la conexión

    def funcion_registrar(self, event=None):
        # Crear una nueva ventana para el registro
        ventana_registrar = Toplevel(self.window)
        ventana_registrar.title("Registrar Nuevo Usuario")
        ventana_registrar.geometry("400x320")
        ventana_registrar.resizable(width=False, height=False)

        # Obtener las dimensiones de la pantalla
        screen_width = self.window.winfo_screenwidth()
        screen_height = self.window.winfo_screenheight()

        # Calcular las coordenadas para centrar la ventana de registro
        x = (screen_width - 400) // 2
        y = (screen_height - 320) // 2

        ventana_registrar.geometry(f"400x320+{x}+{y}")  # Ajusta el tamaño y posición de la ventana
        ventana_registrar.resizable(width=False, height=False)

        # Aplicar estilo similar al de la pantalla principal
        ventana_registrar.config(bg="#363636", bd=8)

        # Etiquetas para los campos
        self.crear_label_entry(ventana_registrar, "Nombre:", 1, "#7FFFD4", rely=0.1)
        self.crear_label_entry(ventana_registrar, "Apellido:", 2, "#7FFFD4", rely=0.2)
        self.crear_label_entry(ventana_registrar, "DNI:", 3, "#7FFFD4", rely=0.3)
        self.crear_label_entry(ventana_registrar, "Domicilio:", 4, "#7FFFD4", rely=0.4)
        self.crear_label_entry(ventana_registrar, "Teléfono:", 5, "#7FFFD4", rely=0.5)
        self.crear_label_entry(ventana_registrar, "Estado:", 6, "#7FFFD4", rely=0.6)
        self.crear_label_entry(ventana_registrar, "Actividad:", 7, "#7FFFD4", rely=0.7)

        # Crear los campos de entrada
        entry_nuevo_nombre = Entry(ventana_registrar, font=("Arial", 12, "bold"), bg="#9EB0AB", fg="black",
                                   textvariable=self.nuevo_nombre, width=25, bd=3, relief="solid")
        entry_nuevo_apellido = Entry(ventana_registrar, font=("Arial", 12, "bold"), bg="#9EB0AB", fg="black",
                                     textvariable=self.nuevo_apellido, width=25, bd=3, relief="solid")
        entry_nuevo_dni = Entry(ventana_registrar, font=("Arial", 12, "bold"), bg="#9EB0AB", fg="black",
                                textvariable=self.nuevo_dni, width=25, bd=3, relief="solid")
        entry_nuevo_telefono = Entry(ventana_registrar, font=("Arial", 12, "bold"), bg="#9EB0AB", fg="black",
                                     textvariable=self.nuevo_telefono, width=25, bd=3, relief="solid")
        entry_nuevo_domicilio = Entry(ventana_registrar, font=("Arial", 12, "bold"), bg="#9EB0AB", fg="black",
                                      textvariable=self.nuevo_domicilio, width=25, bd=3, relief="solid")
        entry_nuevo_estado = Entry(ventana_registrar, font=("Arial", 12, "bold"), bg="#9EB0AB", fg="black",
                                   textvariable=self.nuevo_estado, width=25, bd=3, relief="solid")

        entry_nuevo_nombre.grid(row=1, column=1, padx=(10), pady=5, sticky="w")
        entry_nuevo_apellido.grid(row=2, column=1, padx=(10), pady=5, sticky="w")
        entry_nuevo_dni.grid(row=3, column=1, padx=(10), pady=5, sticky="w")
        entry_nuevo_domicilio.grid(row=4, column=1, padx=(10), pady=5, sticky="w")
        entry_nuevo_telefono.grid(row=5, column=1, padx=(10), pady=5, sticky="w")
        entry_nuevo_estado.grid(row=6, column=1, padx=(10), pady=5, sticky="w")

        # Obtener y cargar las opciones de actividades desde la base de datos
        opciones_actividades = self.obtener_nombres_actividades()
        # Crear el Combobox de actividad con las opciones cargadas
        combobox_nueva_actividad = ttk.Combobox(ventana_registrar, textvariable=self.nueva_actividad,
                                                values=opciones_actividades, state='readonly',
                                                font=("Arial", 12, "bold"),
                                                width=23, height=25)
        combobox_nueva_actividad.config(style="Custom.TCombobox")  # Aplicar estilo personalizado
        combobox_nueva_actividad.grid(row=7, column=1, padx=(10), pady=5, sticky="w")

        # Botón de registro
        boton_registrar = Button(ventana_registrar, text="Registrar",
                                 command=lambda: self.registrar_nuevo_usuario(
                                     self.nuevo_nombre.get(), self.nuevo_apellido.get(), self.nuevo_dni.get(),
                                      self.nuevo_domicilio.get(),self.nuevo_telefono.get(), self.nuevo_estado.get(),
                                     self.nueva_actividad.get()), fg="black", font=("Arial", 12, "bold"))
        boton_registrar.configure(bg="#7FFFD4")
        boton_registrar.grid(row=8, column=2, pady=10, padx=5)

    def registrar_nuevo_usuario(self, nuevo_nombre, nuevo_apellido, nuevo_dni,  nuevo_domicilio,nuevo_telefono,
                                nuevo_estado, nueva_actividad):
        try:
            # Validar que todos los campos estén llenos
            if not nuevo_nombre or not nuevo_apellido or not nuevo_dni or not nuevo_telefono or not nuevo_domicilio or not nuevo_estado or not nueva_actividad:
                messagebox.showerror("Error", "Todos los campos son obligatorios.")
                return

            # Agregar nuevo usuario a la base de datos
            query = "INSERT INTO Clientes (nombre, apellido, dni, domicilio, telefono,idActividad, estado) VALUES (?, ?, ?, ?, ?, ?,?)"
            with sqlite3.connect("gimnasio.db") as conn:
                c = conn.cursor()
                c.execute(query, (
                nuevo_nombre, nuevo_apellido, nuevo_dni, nuevo_domicilio, nuevo_telefono, nueva_actividad,
                nuevo_estado))
                conn.commit()

            # Limpiar los campos de entrada
            self.nuevo_nombre.set("")
            self.nuevo_apellido.set("")
            self.nuevo_dni.set("")
            self.nuevo_domicilio.set("")
            self.nuevo_telefono.set("")
            self.nuevo_estado.set("")
            self.nueva_actividad.set("")

            # Recargar la tabla
            self.cargar_tabla()

        except Exception as e:
            print("Error al registrar nuevo usuario:", e)

    def cargar_tabla(self):
        # Limpiar la tabla
        self.tabla.delete(*self.tabla.get_children())

        try:
            # Obtener todos los clientes desde la base de datos
            with sqlite3.connect("gimnasio.db") as conn:
                c = conn.cursor()
                query = "SELECT * FROM Clientes"
                resultados = c.execute(query).fetchall()

                # Mostrar los resultados en la tabla
                for resultado in resultados:
                    self.tabla.insert("", "end", values=resultado)

        except Exception as e:
            print("Error al cargar la tabla:", e)


if __name__ == "__main__":
    ventana_principal = tk.Tk()
    app = VentanaPrincipal(ventana_principal)
    ventana_principal.mainloop()

