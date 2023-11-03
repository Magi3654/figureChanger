import PIL
from PIL import ImageTk
import math
from tkinter import colorchooser
import graflib as gl
import numpy as np
import tkinter as tk
from tkinter import *

# Crear una ventana de Tkinter
app = tk.Tk()

# Configuración de la interfaz
app.geometry('1000x500')
app.title('Sombreado de un Poligono')

# Variables para el tamaño del lienzo
ancho_var = tk.StringVar()
alto_var = tk.StringVar()

# Variables de condición
canva_creado = False
poligono_creado = False

# Coordenadas de los vértices del polígono
vertices = []
# Creación de Frames
frame1 = tk.Frame(app, bg='white')
frame2 = tk.Frame(app, bg='#006d77')

# Función del botón "Crear Canva"
def dibujarFigura():
    global canva_creado, ancho, alto  # Agregar ancho y alto como variables globales

    if not canva_creado:
        tk.Label(frame2, fg='white', bg='#006d77').pack()

        ancho = int(ancho_var.get())
        alto = int(alto_var.get())

        # Definir un lienzo
        canvas = PIL.Image.new('RGB', (ancho, alto), (255, 255, 255))

        tkpic = ImageTk.PhotoImage(canvas)
        label = tk.Label(frame2, image=tkpic)
        label.image = tkpic  # Guardar una referencia a la imagen para evitar que se elimine
        label.pack()
        app.geometry(f"{ancho + 800}x{alto + 500}")

        def callback(event):
                color = (0, 0, 0)
                gl.pointAround(canvas, event.x, event.y, (ancho, alto), color)
                tkpic = ImageTk.PhotoImage(canvas)
                label.config(image=tkpic)
                label.image = tkpic  # Save reference to image
                vertices.append((event.x, event.y))

        label.bind("<Button-1>", callback)

        def crearPoligono():
            
            global poligono_creado, color  # Agregar color como variable global
            
            if not poligono_creado:
                relleno = colorchooser.askcolor(title="Choose color")
                color = tuple(int(c) for c in relleno[0])
                print(color)

                gl.drawPolygon(gl.matrixToCartessian(vertices, ancho, alto), (0, 0, 0), canvas)
                gl.drawGradientPolygon(gl.matrixToCartessian(vertices, ancho, alto), color, canvas)

                tkpic = ImageTk.PhotoImage(canvas)
                label.config(image=tkpic)
                label.image = tkpic  # Save reference to image
                label.pack()

                def callback(event):
                    centroid = (event.x, event.y)
                    gl.drawGradientPolygon(gl.matrixToCartessian(vertices, ancho, alto), color, canvas, centroid)
                    tkpic = ImageTk.PhotoImage(canvas)
                    label.config(image=tkpic)
                    label.image = tkpic  # Save reference to image

                label.bind("<Button-1>", callback)
                poligono_creado = True
    
        tk.Label(
            frame1,
            text='Ahora puedes dibujar los puntos de tu poligono en el canva!',
            fg='black',
            bg='white',
        ).pack(pady=10)
        
        tk.Button(
            frame1,
            text='Crear Poligono',
            font=('Courier', 10),
            bg='#006d77',
            fg='white',
            command=crearPoligono,
        ).pack()

        canva_creado = True


# Matriz de transformación inicial (identidad)
transformation_matrix = np.identity(3)

# Función para aplicar una transformación
def apply_transformation(transformation):
    global vertices
    new_vertices = []
    for vertex in vertices:
        vertex = np.array([vertex[0], vertex[1], 1])
        transformed_vertex = np.dot(transformation, vertex)
        new_vertices.append((transformed_vertex[0], transformed_vertex[1]))
    return new_vertices

# Función para rotar la figura
def rotate(degrees):
    global transformation_matrix
    radians = math.radians(degrees)
    rotation_matrix = np.array([[math.cos(radians), -math.sin(radians), 0],
                                [math.sin(radians), math.cos(radians), 0],
                                [0, 0, 1]])
    transformation_matrix = np.dot(rotation_matrix, transformation_matrix)
    vertices = apply_transformation(transformation_matrix)
    update_canvas()

# Función para trasladar la figura
def translate(dx, dy):
    global transformation_matrix
    translation_matrix = np.array([[1, 0, dx],
                                   [0, 1, dy],
                                   [0, 0, 1]])
    transformation_matrix = np.dot(translation_matrix, transformation_matrix)
    vertices = apply_transformation(transformation_matrix)
    update_canvas()

# Función para escalar la figura
def scale(sx, sy):
    global transformation_matrix
    scale_matrix = np.array([[sx, 0, 0],
                            [0, sy, 0],
                            [0, 0, 1]])
    transformation_matrix = np.dot(scale_matrix, transformation_matrix)
    vertices = apply_transformation(transformation_matrix)
    update_canvas()

# Función para cambiar la cámara
def change_camera(x, y):
    global transformation_matrix
    camera_matrix = np.array([[1, 0, -x],
                             [0, 1, -y],
                             [0, 0, 1]])
    transformation_matrix = np.dot(camera_matrix, transformation_matrix)
    update_canvas()

# Función para actualizar el lienzo
def update_canvas():
    global vertices
    if canva_creado:
        # Actualiza el lienzo con las coordenadas transformadas
        canvas = PIL.Image.new('RGB', (ancho, alto), (255, 255, 255))
        gl.drawPolygon(gl.matrixToCartessian(vertices, ancho, alto), (0, 0, 0), canvas)
        gl.drawGradientPolygon(gl.matrixToCartessian(vertices, ancho, alto), color, canvas)
        tkpic = ImageTk.PhotoImage(canvas)
        label.config(image=tkpic)
        label.image = tkpic

frame1.pack(side=LEFT, expand=True, fill=BOTH)
frame2.pack(side=LEFT, expand=True, fill=BOTH)
app.mainloop()
