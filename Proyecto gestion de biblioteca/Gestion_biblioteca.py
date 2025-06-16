from customtkinter import *
from tkinter import messagebox
from conector_biblioteca import obtener_conexion

set_appearance_mode("dark")
set_default_color_theme("dark-blue")

def login():
    login_window.withdraw()
    abrir_gestion_biblioteca()

def cerrar_sesion(ventana):
    ventana.destroy()
    login_window.deiconify()

def abrir_gestion_biblioteca():
    ventana = CTk()
    ventana.title("Gestion de inventario")
    ventana.geometry("700x650")

    listbox = CTkTextbox(ventana, font=("Arial", 12), height=150)
    listbox.pack(fill=BOTH, expand=False, padx=10, pady=10)

    def cargar_libros():
        try:
            conexion_biblioteca = obtener_conexion()
            cursor = conexion_biblioteca.cursor()
            cursor.execute("SELECT titulo, autor, cantidad, categoria, ISBN FROM libros")
            historial_libros = cursor.fetchall()
            listbox.delete("1.0", END)
            for titulo, autor, cantidad, categoria, ISBN in historial_libros:
                listbox.insert(END, f"{titulo} de {autor} - categoria: {categoria} - cantidad: {cantidad} - {ISBN}\n")
            messagebox.showinfo("Exito", "Datos cargados correctamente")
            cursor.close()
            conexion_biblioteca.close()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def registrar_libro():
        try:
            conexion_biblioteca = obtener_conexion()
            cursor = conexion_biblioteca.cursor()
            val1 = titulo_campo.get()
            val2 = autor_campo.get()
            val3 = categoria_campo.get()
            val4 = cantidad_campo.get()
            val5 = ISBN_campo.get()
            comando_sql = "INSERT INTO libros (titulo, autor, categoria, cantidad, ISBN) VALUES (%s, %s, %s, %s, %s)"
            cursor.execute(comando_sql, (val1, val2, val3, val4, val5))
            conexion_biblioteca.commit()
            messagebox.showinfo("Exito", "Libro insertado correctamente")
            titulo_campo.delete(0, END)
            autor_campo.delete(0, END)
            categoria_campo.delete(0, END)
            cantidad_campo.delete(0, END)
            ISBN_campo.delete(0, END)
            cursor.close()
            conexion_biblioteca.close()
        except Exception as e:
            messagebox.showerror("ERROR", f"Error al insertar datos: {e}")

    def eliminar_libro():
        seleccion = listbox.get("insert linestart", "insert lineend")
        if not seleccion:
            messagebox.showwarning("Advertencia", "Selecciona un libro para eliminar.")
            return
        try:
            ISBN = seleccion.split(" - ")[-1].strip()
        except IndexError:
            messagebox.showerror("Error", "No se pudo extraer el ISBN correctamente.")
            return
        confirmacion = messagebox.askyesno("Confirmar", f"¿Eliminar el libro con ISBN {ISBN}?")
        if not confirmacion:
            return
        try:
            conexion_biblioteca = obtener_conexion()
            cursor = conexion_biblioteca.cursor()
            query = "DELETE FROM libros WHERE ISBN = %s"
            cursor.execute(query, (ISBN,))
            conexion_biblioteca.commit()
            cursor.close()
            conexion_biblioteca.close()
            messagebox.showinfo("Éxito", "Libro eliminado correctamente.")
            cargar_libros()
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo eliminar el libro:\n{e}")

    CTkButton(ventana, text="Cargar libros", command=cargar_libros).pack(pady=5)

    CTkLabel(ventana, text="Nombre del titulo:").pack()
    titulo_campo = CTkEntry(ventana)
    titulo_campo.pack()

    CTkLabel(ventana, text="Autor del titulo:").pack()
    autor_campo = CTkEntry(ventana)
    autor_campo.pack()

    CTkLabel(ventana, text="Categoria del titulo:").pack()
    categoria_campo = CTkEntry(ventana)
    categoria_campo.pack()

    CTkLabel(ventana, text="Cantidad de libros por titulo:").pack()
    cantidad_campo = CTkEntry(ventana)
    cantidad_campo.pack()

    CTkLabel(ventana, text="ISBN del titulo:").pack()
    ISBN_campo = CTkEntry(ventana)
    ISBN_campo.pack()

    CTkButton(ventana, text="Insertar libro", command=registrar_libro).pack(pady=5)
    CTkButton(ventana, text="Eliminar libro", command=eliminar_libro).pack(pady=5)

    CTkButton(ventana, text="Cerrar sesión", fg_color="#C0392B", hover_color="#E74C3C", command=lambda: cerrar_sesion(ventana)).pack(pady=15)

    ventana.mainloop()

login_window = CTk()
login_window.geometry("700x600")
login_window.title("Inicio de Sesion")

CTkLabel(login_window, text="Welcome Back!", font=("Arial", 24, "bold")).pack(pady=(30, 10))
CTkLabel(login_window, text="Sign in to your account", font=("Arial", 14)).pack(pady=(0, 20))

email_entry = CTkEntry(login_window, placeholder_text="Email")
email_entry.pack(pady=10, ipadx=80, ipady=10)

password_entry = CTkEntry(login_window, placeholder_text="Password", show="*")
password_entry.pack(pady=10, ipadx=80, ipady=10)

login_button = CTkButton(login_window, text="Login", fg_color="#6C2BD9", hover_color="#9B59B6", command=login)
login_button.pack(pady=20, ipadx=60, ipady=10)

login_window.mainloop()
