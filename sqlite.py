import sqlite3
from principal import Cliente
import tkinter as tk
from tkinter import ttk, messagebox
from pagos import VentanaPagos

def crear_tabla_clientes(conn):
    try:
        c = conn.cursor()
        c.execute('''CREATE TABLE "Clientes" (
	"idCliente"	INTEGER NOT NULL,
	"idActividad"	INTEGER,
	"nombre"	TEXT NOT NULL,
	"apellido"	TEXT NOT NULL,
	"dni"	INTEGER NOT NULL,
	"domicilio"	TEXT NOT NULL,
	"telefono"	NUMERIC NOT NULL,
	FOREIGN KEY("idActividad") REFERENCES "Actividad"("idActividad"),
	"estado"	TEXT NOT NULL,
	PRIMARY KEY("idCliente")''')
        conn.commit()
        print("Tabla Clientes creada exitosamente.")
    except sqlite3.Error as error:
        print("Error al crear la tabla Clientes:", error)

def crear_tabla_pagos(conn):
    try:
        c = conn.cursor()
        c.execute('''CREATE TABLE "Pagos" (
	"idPago"	INTEGER NOT NULL,
	"idCliente"	INTEGER NOT NULL,
	"idActividad"	INTEGER NOT NULL,
	"montoTotal"	NUMERIC NOT NULL,
	"montoRecibido"	NUMERIC NOT NULL,
	"cambio"	NUMERIC NOT NULL,
	"fechaPago"	TEXT NOT NULL,
	PRIMARY KEY("idPago"),
	FOREIGN KEY("idCliente") REFERENCES "Clientes"("idCliente"),
	FOREIGN KEY("idActividad") REFERENCES "Actividad"("idActividad")''')
        conn.commit()
        print("Tabla Pagos creada exitosamente.")
    except sqlite3.Error as error:
        print("Error al crear la tabla Pagos:", error)


def crear_tabla_actividad():
    try:
        # Conexión a la base de datos
        conn = sqlite3.connect("gimnasio.db")
        c = conn.cursor()

        # Crear la tabla "Actividad"
        c.execute('''CREATE TABLE Actividad (
                        idActividad INTEGER PRIMARY KEY,
                        nombreActividad TEXT NOT NULL,
                        montoActividad NUMERIC
                     )''')

        # Guardar cambios y cerrar la conexión
        conn.commit()
        conn.close()
        print("Tabla 'Actividad' creada exitosamente.")

    except sqlite3.Error as error:
        print("Error al crear la tabla 'Actividad':", error)


def inicializar_base_datos():
    try:
        conn = sqlite3.connect("gimnasio.db")
        crear_tabla_clientes(conn)
        crear_tabla_pagos(conn)
        crear_tabla_actividad()
        conn.close()
    except sqlite3.Error as error:
        print("Error al inicializar la base de datos:", error)

if __name__ == "__main__":
    inicializar_base_datos()
