import tkinter as tk
from tkinter import messagebox
from datetime import datetime

class Usuario:
    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self._password = password
        self.amigos = []
        self.publicaciones = []

    def cambiar_contraseña(self, old_password, new_password):
        if self._password == old_password:
            self._password = new_password
            return "Contraseña actualizada con éxito."
        else:
            return "Error: la contraseña actual no coincide."

    def realizar_publicacion(self, texto, imagen=None):
        publicacion = Publicacion(autor=self, texto=texto, imagen=imagen)
        self.publicaciones.append(publicacion)
        return "Publicación realizada con éxito."

    def seguir_amigo(self, amigo):
        if amigo not in self.amigos:
            self.amigos.append(amigo)
            return f"Ahora sigues a {amigo.username}."
        else:
            return "Error: ya sigues a este usuario."

class Publicacion:
    def __init__(self, autor, texto, imagen=None):
        self.autor = autor
        self.texto = texto
        self.imagen = imagen
        self.me_gusta = 0
        self.comentarios = []
        self.fecha = datetime.now()

    def dar_megusta(self):
        self.me_gusta += 1
        return "Le diste 'Me gusta' a esta publicación."

    def agregar_comentario(self, autor, texto):
        comentario = Comentario(autor, texto)
        self.comentarios.append(comentario)
        return "Comentario agregado con éxito."

class Comentario:
    def __init__(self, autor, texto):
        self.autor = autor
        self.texto = texto
        self.fecha = datetime.now()

class RedSocial:
    def __init__(self):
        self.usuarios = []

    def crear_usuario(self, username, email, password):
        if self.buscar_usuario(username):
            return "Error: el nombre de usuario ya existe."
        usuario = Usuario(username, email, password)
        self.usuarios.append(usuario)
        return "Usuario creado con éxito."

    def buscar_usuario(self, username):
        for usuario in self.usuarios:
            if usuario.username == username:
                return usuario
        return None

    def iniciar_sesion(self, username, password):
        usuario = self.buscar_usuario(username)
        if usuario and usuario._password == password:
            return usuario
        else:
            return None

class RedSocialApp:
    def __init__(self, root, red_social):
        self.red_social = red_social
        self.usuario_actual = None

        self.root = root
        self.root.title("Red Social")
        self.root.geometry("600x500")
        self.root.config(bg="#2e3b4e")

        self.frame_login = tk.Frame(root, bg="#2e3b4e")
        self.frame_login.pack(pady=20)

        tk.Label(self.frame_login, text="Usuario:", bg="#2e3b4e", fg="white").grid(row=0, column=0)
        self.entry_usuario = tk.Entry(self.frame_login, width=30)
        self.entry_usuario.grid(row=0, column=1)

        tk.Label(self.frame_login, text="Contraseña:", bg="#2e3b4e", fg="white").grid(row=1, column=0)
        self.entry_password = tk.Entry(self.frame_login, show="*", width=30)
        self.entry_password.grid(row=1, column=1)

        self.button_login = tk.Button(self.frame_login, text="Iniciar sesión", command=self.iniciar_sesion, bg="#4CAF50", fg="white", width=15)
        self.button_login.grid(row=2, column=0, columnspan=2, pady=10)

        self.button_register = tk.Button(self.frame_login, text="Registrarse", command=self.registrar_usuario, bg="#1E88E5", fg="white", width=15)
        self.button_register.grid(row=3, column=0, columnspan=2, pady=5)

        self.frame_usuario = tk.Frame(root, bg="#2e3b4e")
        
        self.label_bienvenida = tk.Label(self.frame_usuario, text="", bg="#2e3b4e", fg="white", font=("Arial", 14))
        self.label_bienvenida.pack(pady=10)

        self.button_publicar = tk.Button(self.frame_usuario, text="Realizar publicación", command=self.mostrar_publicar, bg="#8E24AA", fg="white", width=20)
        self.button_publicar.pack(pady=5)
        
        self.button_feed = tk.Button(self.frame_usuario, text="Ver feed", command=self.mostrar_feed, bg="#FF9800", fg="white", width=20)
        self.button_feed.pack(pady=5)
        
        self.button_amigos = tk.Button(self.frame_usuario, text="Seguir amigo", command=self.mostrar_seguir_amigo, bg="#03A9F4", fg="white", width=20)
        self.button_amigos.pack(pady=5)
        
        self.button_logout = tk.Button(self.frame_usuario, text="Cerrar sesión", command=self.cerrar_sesion, bg="#F44336", fg="white", width=20)
        self.button_logout.pack(pady=10)

    def iniciar_sesion(self):
        username = self.entry_usuario.get()
        password = self.entry_password.get()
        usuario = self.red_social.iniciar_sesion(username, password)
        if usuario:
            self.usuario_actual = usuario
            messagebox.showinfo("Éxito", f"¡Bienvenido, {username}!")
            self.mostrar_usuario()
        else:
            messagebox.showerror("Error", "Usuario o contraseña incorrectos")

    def registrar_usuario(self):
        username = self.entry_usuario.get()
        password = self.entry_password.get()
        email = username + "@example.com" 
        resultado = self.red_social.crear_usuario(username, email, password)
        messagebox.showinfo("Registro", resultado)

    def mostrar_usuario(self):
        self.frame_login.pack_forget()
        self.label_bienvenida.config(text=f"Bienvenido, {self.usuario_actual.username}")
        self.frame_usuario.pack(pady=20)

    def mostrar_publicar(self):
        ventana_publicar = tk.Toplevel(self.root)
        ventana_publicar.title("Nueva publicación")
        ventana_publicar.config(bg="#5C6BC0")
        
        tk.Label(ventana_publicar, text="Escribe tu publicación:", bg="#5C6BC0", fg="white").pack(pady=5)
        entry_publicacion = tk.Entry(ventana_publicar, width=40)
        entry_publicacion.pack()

        def realizar_publicacion():
            texto = entry_publicacion.get()
            if texto:
                resultado = self.usuario_actual.realizar_publicacion(texto)
                messagebox.showinfo("Publicación", resultado)
                ventana_publicar.destroy()
            else:
                messagebox.showwarning("Advertencia", "La publicación no puede estar vacía.")

        tk.Button(ventana_publicar, text="Publicar", command=realizar_publicacion, bg="#4CAF50", fg="white", width=15).pack(pady=10)

    def mostrar_feed(self):
        ventana_feed = tk.Toplevel(self.root)
        ventana_feed.title("Feed de publicaciones")
        ventana_feed.geometry("500x400")
        ventana_feed.config(bg="#4E342E")

        frame_feed = tk.Frame(ventana_feed, bg="#4E342E")
        frame_feed.pack(pady=10)

        for publicacion in self.usuario_actual.publicaciones:
            self.mostrar_publicacion(frame_feed, publicacion, self.usuario_actual)

        for amigo in self.usuario_actual.amigos:
            for publicacion in amigo.publicaciones:
                self.mostrar_publicacion(frame_feed, publicacion, amigo)

    def mostrar_publicacion(self, frame, publicacion, autor):
        frame_publicacion = tk.Frame(frame, bg="#3E2723")
        frame_publicacion.pack(pady=5, fill='x')

        label_publicacion = tk.Label(frame_publicacion, text=f"{autor.username}: {publicacion.texto} ({publicacion.me_gusta} Me gusta)", bg="#3E2723", fg="white")
        label_publicacion.pack(side='left')

        button_me_gusta = tk.Button(frame_publicacion, text="Me gusta", command=lambda: self.dar_me_gusta(publicacion), bg="#4CAF50", fg="white")
        button_me_gusta.pack(side='left', padx=5)

        button_comentar = tk.Button(frame_publicacion, text="Comentar", command=lambda: self.agregar_comentario(publicacion), bg="#FF9800", fg="white")
        button_comentar.pack(side='left', padx=5)

        for comentario in publicacion.comentarios:
            label_comentario = tk.Label(frame_publicacion, text=f"{comentario.autor.username}: {comentario.texto}", bg="#3E2723", fg="lightgray")
            label_comentario.pack(anchor='w')

    def dar_me_gusta(self, publicacion):
        resultado = publicacion.dar_megusta()
        messagebox.showinfo("Me gusta", resultado)
        self.mostrar_feed() 

    def agregar_comentario(self, publicacion):
        ventana_comentar = tk.Toplevel(self.root)
        ventana_comentar.title("Agregar comentario")
        ventana_comentar.config(bg="#5C6BC0")
        
        tk.Label(ventana_comentar, text="Escribe tu comentario:", bg="#5C6BC0", fg="white").pack(pady=5)
        entry_comentario = tk.Entry(ventana_comentar, width=40)
        entry_comentario.pack()

        def realizar_comentario():
            texto = entry_comentario.get()
            if texto:
                resultado = publicacion.agregar_comentario(self.usuario_actual, texto)
                messagebox.showinfo("Comentario", resultado)
                ventana_comentar.destroy()
                self.mostrar_feed()  # Refrescar el feed
            else:
                messagebox.showwarning("Advertencia", "El comentario no puede estar vacío.")

        tk.Button(ventana_comentar, text="Comentar", command=realizar_comentario, bg="#4CAF50", fg="white", width=15).pack(pady=10)

    def mostrar_seguir_amigo(self):
        ventana_seguir = tk.Toplevel(self.root)
        ventana_seguir.title("Seguir a un amigo")
        ventana_seguir.config(bg="#00796B")
        
        tk.Label(ventana_seguir, text="Nombre de usuario del amigo:", bg="#00796B", fg="white").pack(pady=5)
        entry_amigo = tk.Entry(ventana_seguir)
        entry_amigo.pack()

        def seguir_amigo():
            amigo_nombre = entry_amigo.get()
            amigo = self.red_social.buscar_usuario(amigo_nombre)
            if amigo:
                resultado = self.usuario_actual.seguir_amigo(amigo)
                messagebox.showinfo("Seguir amigo", resultado)
                ventana_seguir.destroy()
            else:
                messagebox.showerror("Error", "Usuario no encontrado.")

        tk.Button(ventana_seguir, text="Seguir", command=seguir_amigo, bg="#4CAF50", fg="white", width=15).pack(pady=10)

    def cerrar_sesion(self):
        self.usuario_actual = None
        self.frame_usuario.pack_forget()
        self.frame_login.pack(pady=10)
        messagebox.showinfo("Cerrar sesión", "Has cerrado sesión exitosamente.")


root = tk.Tk()
red_social = RedSocial()
app = RedSocialApp(root, red_social)
root.mainloop()
