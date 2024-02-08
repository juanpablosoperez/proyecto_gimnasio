import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
import datetime
import threading
import time
from tkinter import Tk, Label, Frame, Button, OptionMenu, StringVar, Entry, Listbox, Scrollbar

class VentanaPagos:
    def __init__(self, ventana_pagos):
        self.window = ventana_pagos
        self.window.title("Pagos")
        self.window.geometry("980x680")
        self.conn = sqlite3.connect("gimnasio.db")  # Conexión a la base de datos
        self.conn = sqlite3.connect("gimnasio.db", detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES)
        self.c = self.conn.cursor()  # Crear cursor para la base de datos

        # Obtener las dimensiones de la pantalla
        screen_width = self.window.winfo_screenwidth()
        screen_height = self.window.winfo_screenheight()

        # Calcular las coordenadas para centrar la ventana
        x = (screen_width - 980) // 2
        y = (screen_height - 680) // 2

        # Establecer la geometría de la ventana
        self.window.geometry(f"980x680+{x}+{y}")
        self.window.resizable(width=False, height=False)
        self.window.config(bg="#363636", bd=10)

        # Crear el marco principal
        marco_principal = tk.Frame(self.window, bg="#363636")
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

        # Agregar el título en negrita centrado sobre el marco de pagos
        titulo_label = tk.Label(self.window, text="PAGOS", font=("Arial", 24, "bold"), bg="#363636", fg="#7FFFD4")
        titulo_label.place(relx=0.5, rely=0.1, anchor="center")

        # Agregar un nuevo marco para ingreso de cliente y cálculo de monto
        marco_pago = tk.Frame(self.window, bg="#363636", bd=4, relief="solid", highlightbackground="#7FFFD4", highlightthickness=1,takefocus=False)
        marco_pago.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.55, relheight=0.6)

        # Etiqueta y combobox para seleccionar actividad
        opciones_actividades = self.obtener_actividades_desde_bd()
        self.actividad_seleccionada = tk.StringVar(marco_pago)

        etiqueta_actividad = tk.Label(marco_pago, text="Seleccionar Actividad:", font=("Arial", 12, "bold"), bg="#363636",
                                   fg="#7FFFD4")
        etiqueta_actividad.grid(row=1, column=0, padx=10, pady=5)

        self.combobox_actividades = ttk.Combobox(marco_pago, textvariable=self.actividad_seleccionada,
                                             values=opciones_actividades, state='readonly')
        self.combobox_actividades.grid(row=1, column=1, pady=10, padx=5, sticky="ew")
        self.combobox_actividades.set("")

        # Etiqueta y combobox para ingresar el nombre del cliente que va a pagar
        etiqueta_cliente = tk.Label(marco_pago, text="Ingrese Nombre Cliente:", font=("Arial", 12, "bold"), bg="#363636", fg="#7FFFD4")
        etiqueta_cliente.grid(row=2, column=0, padx=10, pady=5)

        self.entry_nombre_cliente = ttk.Combobox(marco_pago)
        self.entry_nombre_cliente.grid(row=2, column=1, pady=10, padx=5, sticky="ew")
        self.entry_nombre_cliente.bind('<KeyRelease>', self.mostrar_coincidencias_clientes)

        # Botón para agregar cliente
        #boton_agregar_cliente = ttk.Button(marco_pago, text="Agregar Cliente", command=self.agregar_cliente)
        # Botón para agregar usuario a la lista
        estilo_boton_agregar = {
            "bd": 0,
            "fg": "white",
            "relief": "flat",
            "font": ("Arial", 11),
            "padx": 10,
            "pady": 5,
            "bg": "#363636"
        }

        boton_agregar_cliente = Button(
            marco_pago,
            text="Agregar Cliente",
            command=self.agregar_cliente,
            **estilo_boton_agregar
        )
        boton_agregar_cliente.grid(row=2, column=2, padx=5, pady=5)

        # Lista para mostrar clientes con actividad
        self.lista_clientes_actividades = tk.Listbox(marco_pago, selectbackground="#7FFFD4", selectforeground="#363636", font=("Arial", 11), bg="#363636", fg="#7FFFD4", height=6)
        self.lista_clientes_actividades.grid(row=3, column=0, columnspan=3, pady=10, padx=20, sticky="nsew")

        # Scrollbar para la lista de usuarios
        scrollbar_usuarios = Scrollbar(marco_pago, orient="vertical", command=self.lista_clientes_actividades.yview)
        scrollbar_usuarios.grid(row=3, column=2, pady=10, sticky="nse")

        self.lista_clientes_actividades.config(yscrollcommand=scrollbar_usuarios.set)

        # Botón para calcular monto a pagar
        estilo_boton_calcular = {
            "bd": 0,
            "fg": "black",
            "relief": "flat",
            "font": ("Arial", 11, "bold"),
            "padx": 10,
            "pady": 8,
            "bg": "#7FFFD4"
        }

        boton_calcular_monto = Button(
            marco_pago,
            text="Calcular Monto",
            command=self.calcular_monto,
            **estilo_boton_calcular
        )
        boton_calcular_monto.grid(row=4, column=2, columnspan=2, pady=10)

        # Etiqueta y entry para ingresar el monto recibido
        etiqueta_monto_recibido = tk.Label(marco_pago, text="Monto Recibido:", font=("Arial", 12, "bold"), bg="#363636",
                                           fg="#7FFFD4")
        etiqueta_monto_recibido.grid(row=5, column=0, padx=10, pady=5, sticky="e")

        self.monto_recibido_entry = ttk.Entry(marco_pago)
        self.monto_recibido_entry.grid(row=5, column=1, padx=5, pady=5, sticky="w")

        # Botón para realizar el pago
        estilo_boton_pagar = {
            "bd": 0,
            "fg": "black",
            "relief": "flat",
            "font": ("Arial", 11, "bold"),
            "padx": 25,
            "pady": 8,
            "bg": "#7FFFD4"
        }

        boton_pagar = Button(
            marco_pago,
            text="Pagar",
            command=self.realizar_pago,
            **estilo_boton_pagar
        )
        boton_pagar.grid(row=6, column=2, columnspan=1, pady=10)

        # Inicia el temporizador para verificar los pagos vencidos
        self.iniciar_temporizador_verificacion_pagos()

        marco_fecha_hora = Frame(self.window, bg="#212121", bd=2, relief="solid")
        marco_fecha_hora.place(relx=1, rely=1, anchor="se", x=-10, y=-10)

        # Etiqueta para la fecha y hora
        self.etiqueta_fecha_hora = Label(marco_fecha_hora, text="", font=("Arial", 12), bg="#212121", fg="#7FFFD4")
        self.etiqueta_fecha_hora.pack(padx=10, pady=5)

        # Actualizar la fecha y hora cada segundo
        self.actualizar_fecha_hora()

    def actualizar_fecha_hora(self):
        # Obtener la fecha y hora actuales
        now = time.strftime("%d-%m-%Y %H:%M:%S")

        # Actualizar la etiqueta con la fecha y hora actuales
        self.etiqueta_fecha_hora.config(text=now)

        # Llamar a la función nuevamente después de 1000 ms (1 segundo)
        self.window.after(1000, self.actualizar_fecha_hora)

    def calcular_monto_total(self):
        monto_total = 0
        for item in self.lista_clientes_actividades.get(0, tk.END):
            actividad = item.split(" - ")[1]
            monto_actividad = self.obtener_monto_actividad(actividad)
            if monto_actividad is not None:
                monto_total += monto_actividad
        return monto_total

    def calcular_monto(self):
        monto_total = self.calcular_monto_total()
        messagebox.showinfo("Monto a Pagar", f"El monto total a pagar es: ${monto_total}")


    def mostrar_coincidencias_clientes(self, event):
        nombre_cliente = self.entry_nombre_cliente.get().strip().lower()

        if nombre_cliente:  # Verificar si el nombre del cliente no está vacío
            clientes = self.obtener_coincidencias_clientes(nombre_cliente)
            self.entry_nombre_cliente['values'] = clientes

    def agregar_cliente(self):
        nombre_cliente = self.entry_nombre_cliente.get().strip()
        actividad = self.actividad_seleccionada.get()
        if nombre_cliente and actividad:
            self.lista_clientes_actividades.insert(tk.END, f"{nombre_cliente} - {actividad}")
            self.entry_nombre_cliente.set("")
            self.combobox_actividades.set("")


    def realizar_pago(self):
        monto_total = self.calcular_monto_total()
        monto_recibido = float(self.monto_recibido_entry.get().strip())
        cambio = monto_recibido - monto_total

        if cambio < 0:
            messagebox.showerror("Pago Insuficiente", "El monto recibido es insuficiente.")
        else:
            mensaje_pago_exitoso = f"Pago exitoso! El cambio es: ${cambio:.2f}."
            messagebox.showinfo("Pago Realizado", mensaje_pago_exitoso)

            # Obtener el nombre del cliente y la actividad seleccionada
            cliente_actividad = self.lista_clientes_actividades.get(tk.ACTIVE)
            nombre_cliente, actividad = cliente_actividad.split(" - ")

            # Obtener el idCliente correspondiente al nombre del cliente
            id_cliente = self.obtener_id_cliente(nombre_cliente)

            # Obtener el idActividad correspondiente a la actividad seleccionada
            id_actividad = self.obtener_id_actividad(actividad)

            if id_cliente is not None and id_actividad is not None:

                # Formatear la fecha y hora actual como una cadena
                fecha_pago = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                # Insertar un nuevo registro en la tabla Pagos
                try:
                    self.c.execute(
                        "INSERT INTO Pagos (idCliente, idActividad, montoTotal, montoRecibido, cambio, fechaPago) VALUES (?, ?, ?, ?, ?, ?)",
                        (id_cliente, id_actividad, monto_total, monto_recibido, cambio, fecha_pago)
                    )
                    self.conn.commit()
                    print("Registro de pago insertado correctamente en la base de datos.")

                    # Insertar un nuevo registro en la tabla Ingresos
                    self.insertar_ingreso(id_cliente, monto_total, fecha_pago)

                    # Actualizar el estado del cliente a "Pago" en la base de datos
                    self.actualizar_estado_cliente(id_cliente)
                except sqlite3.Error as error:
                    print("Error al insertar registro de pago en la base de datos:", error)
            else:
                messagebox.showerror("Error", "Cliente no encontrado o actividad no seleccionada.")

        # Mostrar nuevamente la ventana principal
        self.window.deiconify()

    def insertar_ingreso(self, id_cliente, monto_total, fecha_pago):
        try:
            # Obtener mes y año de la fecha de pago
            fecha_pago_dt = datetime.datetime.strptime(fecha_pago, "%Y-%m-%d %H:%M:%S")
            mes = fecha_pago_dt.strftime("%m")
            año = fecha_pago_dt.strftime("%Y")

            # Insertar un nuevo registro en la tabla Ingresos
            self.c.execute(
                "INSERT INTO Ingresos (idPago, fechaIngreso, montoIngreso, mes, año) VALUES (?, ?, ?, ?, ?)",
                (id_cliente, fecha_pago, monto_total, mes, año)
            )
            self.conn.commit()
            print("Registro de ingreso insertado correctamente en la base de datos.")
        except sqlite3.Error as error:
            print("Error al insertar registro de ingreso en la base de datos:", error)


    def actualizar_estado_cliente(self, id_cliente):
        try:
            # Actualizar el estado del cliente a "Pago"
            self.c.execute("UPDATE Clientes SET estado = ? WHERE idCliente = ?", ("Pago", id_cliente))
            self.conn.commit()
            print(f"Estado actualizado a 'Pago' para el cliente con ID {id_cliente}")
        except sqlite3.Error as error:
            print("Error al actualizar estado del cliente:", error)

    def obtener_coincidencias_clientes(self, nombre_cliente):
        try:
            self.c.execute("SELECT nombre || ' ' || apellido FROM Clientes WHERE LOWER(nombre) LIKE ? OR LOWER(apellido) LIKE ?",
                           ('%' + nombre_cliente + '%', '%' + nombre_cliente + '%'))
            clientes = self.c.fetchall()
            clientes = [cliente[0] for cliente in clientes]
            return clientes
        except sqlite3.Error as error:
            print("Error al cargar clientes:", error)
            return []

    def obtener_monto_actividad(self, actividad):
        try:
            self.c.execute("SELECT montoActividad FROM Actividad WHERE nombreActividad = ?", (actividad,))
            row = self.c.fetchone()
            if row:
                return row[0]
            else:
                return None
        except sqlite3.Error as error:
            print("Error al obtener monto de actividad:", error)
            return None

    def obtener_actividades_desde_bd(self):
        try:
            self.c.execute("SELECT nombreActividad FROM Actividad")
            actividades = self.c.fetchall()
            actividades = [actividad[0] for actividad in actividades]
            return actividades
        except sqlite3.Error as error:
            print("Error al cargar actividades desde la base de datos:", error)
            return []

    def obtener_id_cliente(self, nombre_cliente):
        try:
            self.c.execute("SELECT idCliente FROM Clientes WHERE nombre || ' ' || apellido = ?", (nombre_cliente,))
            query_result = self.c.fetchone()
            if query_result:
                return query_result[0]
            else:
                messagebox.showerror("Error", "Cliente no encontrado")
                return None
        except sqlite3.Error as error:
            print("Error al obtener ID del cliente:", error)
            return None

    def obtener_id_actividad(self, nombre_actividad):
        try:
            self.c.execute("SELECT idActividad FROM Actividad WHERE nombreActividad = ?", (nombre_actividad,))
            row = self.c.fetchone()
            if row:
                return row[0]
            else:
                return None
        except sqlite3.Error as error:
            print("Error al obtener id de actividad:", error)
            return None

    def iniciar_temporizador_verificacion_pagos(self):
        # Crea un hilo para ejecutar la función de verificación periódica
        t = threading.Thread(target=self.verificar_pagos_vencidos)
        t.daemon = True  # El hilo se detendrá cuando se cierre la aplicación
        t.start()

    def verificar_pagos_vencidos(self):
        while True:
            try:
                # Crea una nueva conexión y cursor dentro del hilo secundario
                conn = sqlite3.connect("gimnasio.db")
                c = conn.cursor()

                # Obtener la fecha actual menos 30 días
                fecha_limite = datetime.datetime.now() - datetime.timedelta(days=30)
                fecha_limite_str = fecha_limite.strftime("%Y-%m-%d %H:%M:%S")  # Formatear la fecha como string

                # Consultar los registros de pago con fecha anterior a fecha_limite
                c.execute("SELECT idCliente FROM Pagos WHERE fechaPago <= ?", (fecha_limite_str,))
                pagos_vencidos = c.fetchall()

                for pago in pagos_vencidos:
                    id_cliente = pago[0]
                    self.actualizar_estado_cliente_por_id(id_cliente, "No pago")

                # Cerrar la conexión y esperar un día antes de verificar nuevamente
                conn.close()
                time.sleep(24 * 60 * 60)

            except Exception as e:
                print("Error al verificar pagos vencidos:", e)

    def actualizar_estado_cliente_por_id(self, id_cliente, estado):
        try:
            self.c.execute("UPDATE Clientes SET estado = ? WHERE idCliente = ?", (estado, id_cliente))
            self.conn.commit()
            print(f"Estado actualizado a '{estado}' para el cliente con ID {id_cliente}")
        except sqlite3.Error as error:
            print("Error al actualizar estado del cliente:", error)

    def volver_pantalla_principal(self):
        self.window.destroy()

if __name__ == "__main__":
    ventana_pagos = tk.Tk()
    app_pagos = VentanaPagos(ventana_pagos)
    ventana_pagos.mainloop()
