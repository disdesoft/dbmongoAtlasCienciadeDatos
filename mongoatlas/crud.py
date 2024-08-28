import tkinter as tk
from tkinter import messagebox, Scrollbar, ttk
from pymongo import MongoClient
from pymongo.server_api import ServerApi
import re

# Conexión a la base de datos MongoDB
uri = "mongodb+srv://MongodbFabian:Ciencia777@cluster0.utsby.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
client = MongoClient(uri, server_api=ServerApi('1'))
db = client['nombre_base_datos']  # Reemplaza con el nombre de tu base de datos
collection = db['nombre_coleccion']  # Reemplaza con el nombre de tu colección

# Funciones CRUD
def validar_datos():
    if not entry_cedula.get().isdigit():
        messagebox.showwarning("Advertencia", "El campo 'Cédula' debe ser un número entero.")
        return False
    if not entry_nombre.get().isalpha():
        messagebox.showwarning("Advertencia", "El campo 'Nombre' debe contener solo letras.")
        return False
    if not entry_edad.get().isdigit():
        messagebox.showwarning("Advertencia", "El campo 'Edad' debe ser un número entero.")
        return False
    if combobox_ciudad.get() not in ciudades:
        messagebox.showwarning("Advertencia", "Selecciona una ciudad válida del desplegable.")
        return False
    if not entry_telefono.get().isdigit():
        messagebox.showwarning("Advertencia", "El campo 'Teléfono' debe ser un número entero.")
        return False
    if not re.match(r"[^@]+@[^@]+\.[^@]+", entry_email.get()):
        messagebox.showwarning("Advertencia", "Ingresa un email válido.")
        return False
    return True

def create_document():
    if validar_datos():
        documento = {
            "cedula": entry_cedula.get(),
            "nombre": entry_nombre.get(),
            "edad": int(entry_edad.get()),
            "ciudad": combobox_ciudad.get(),
            "telefono": entry_telefono.get(),
            "email": entry_email.get(),
            "carrera": entry_carrera.get()
        }
        collection.insert_one(documento)
        messagebox.showinfo("Éxito", "Documento creado exitosamente.")
        clear_entries()
        read_documents()

def read_documents():
    listbox.delete(*listbox.get_children())
    documentos = collection.find()
    for doc in documentos:
        listbox.insert("", "end", values=(doc.get('cedula'), doc.get('nombre'), doc.get('edad'), 
                                          doc.get('ciudad'), doc.get('telefono'), doc.get('email'),
                                          doc.get('carrera')))

def update_document():
    if validar_datos():
        cedula = entry_cedula.get()
        if cedula:
            query = {"cedula": cedula}
            update = {
                "nombre": entry_nombre.get(),
                "edad": int(entry_edad.get()),
                "ciudad": combobox_ciudad.get(),
                "telefono": entry_telefono.get(),
                "email": entry_email.get(),
                "carrera": entry_carrera.get()
            }
            result = collection.update_one(query, {"$set": update})
            if result.modified_count > 0:
                messagebox.showinfo("Éxito", "Documento actualizado exitosamente.")
            else:
                messagebox.showwarning("Advertencia", "No se encontró el documento para actualizar.")
            clear_entries()
            read_documents()
        else:
            messagebox.showwarning("Advertencia", "El campo 'Cédula' es obligatorio para actualizar.")

def delete_document():
    cedula = entry_cedula.get()
    if cedula:
        query = {"cedula": cedula}
        result = collection.delete_one(query)
        if result.deleted_count > 0:
            messagebox.showinfo("Éxito", "Documento borrado exitosamente.")
        else:
            messagebox.showwarning("Advertencia", "No se encontró el documento para borrar.")
        clear_entries()
        read_documents()
    else:
        messagebox.showwarning("Advertencia", "El campo 'Cédula' es obligatorio para borrar.")

def clear_entries():
    entry_cedula.delete(0, tk.END)
    entry_nombre.delete(0, tk.END)
    entry_edad.delete(0, tk.END)
    combobox_ciudad.set('')
    entry_telefono.delete(0, tk.END)
    entry_email.delete(0, tk.END)
    entry_carrera.delete(0, tk.END)

# Crear la interfaz gráfica con Tkinter
app = tk.Tk()
app.title("CRUD MongoDB")
app.geometry("800x600")  # Tamaño ajustado
app.configure(bg="#f0f0f0")  # Fondo claro

style = ttk.Style()
style.configure("TLabel", font=("Arial", 12), background="#f0f0f0")
style.configure("TEntry", font=("Arial", 12))
style.configure("TButton", font=("Arial", 12), padding=5)

# Frame para los campos de entrada
frame_form = ttk.Frame(app, padding="10")
frame_form.grid(row=0, column=0, padx=20, pady=10)

# Etiquetas y campos de entrada
ttk.Label(frame_form, text="Cédula:").grid(row=0, column=0, sticky=tk.W, pady=5)
entry_cedula = ttk.Entry(frame_form, width=30)
entry_cedula.grid(row=0, column=1, pady=5)

ttk.Label(frame_form, text="Nombre:").grid(row=1, column=0, sticky=tk.W, pady=5)
entry_nombre = ttk.Entry(frame_form, width=30)
entry_nombre.grid(row=1, column=1, pady=5)

ttk.Label(frame_form, text="Edad:").grid(row=2, column=0, sticky=tk.W, pady=5)
entry_edad = ttk.Entry(frame_form, width=30)
entry_edad.grid(row=2, column=1, pady=5)

ttk.Label(frame_form, text="Ciudad:").grid(row=3, column=0, sticky=tk.W, pady=5)
ciudades = ["Fusagasugá", "Girardot", "Ubaté", "Chía", "Zipaquirá", "Chocontá", "Facatativá", "Soacha"]
combobox_ciudad = ttk.Combobox(frame_form, values=ciudades, width=28, state="readonly")
combobox_ciudad.grid(row=3, column=1, pady=5)

ttk.Label(frame_form, text="Teléfono:").grid(row=4, column=0, sticky=tk.W, pady=5)
entry_telefono = ttk.Entry(frame_form, width=30)
entry_telefono.grid(row=4, column=1, pady=5)

ttk.Label(frame_form, text="Email:").grid(row=5, column=0, sticky=tk.W, pady=5)
entry_email = ttk.Entry(frame_form, width=30)
entry_email.grid(row=5, column=1, pady=5)

ttk.Label(frame_form, text="Carrera:").grid(row=6, column=0, sticky=tk.W, pady=5)
entry_carrera = ttk.Entry(frame_form, width=30)
entry_carrera.grid(row=6, column=1, pady=5)

# Botones para las operaciones CRUD
frame_buttons = ttk.Frame(app, padding="10")
frame_buttons.grid(row=1, column=0, padx=20, pady=10)

ttk.Button(frame_buttons, text="Crear", command=create_document).grid(row=0, column=0, padx=10)
ttk.Button(frame_buttons, text="Leer", command=read_documents).grid(row=0, column=1, padx=10)
ttk.Button(frame_buttons, text="Actualizar", command=update_document).grid(row=0, column=2, padx=10)
ttk.Button(frame_buttons, text="Borrar", command=delete_document).grid(row=0, column=3, padx=10)

# Tabla para mostrar los documentos
frame_table = ttk.Frame(app)
frame_table.grid(row=2, column=0, padx=20, pady=10)

columns = ("cedula", "nombre", "edad", "ciudad", "telefono", "email", "carrera")
listbox = ttk.Treeview(frame_table, columns=columns, show="headings", height=10)

for col in columns:
    listbox.heading(col, text=col.capitalize())
    listbox.column(col, width=120)

listbox.pack(side=tk.LEFT, fill=tk.BOTH)

# Scrollbar para la tabla
scrollbar = ttk.Scrollbar(frame_table, orient="vertical", command=listbox.yview)
listbox.configure(yscrollcommand=scrollbar.set)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

# Iniciar la aplicación
app.mainloop()
