################################################################################################################
#                                        INFORMACION DEL MONITOR                                               #
################################################################################################################
from screeninfo import get_monitors

ancho_monitor = 0
largo_monitor = 0
for m in get_monitors():
    ancho_monitor = m.width
    largo_monitor = m.height
################################################################################################################
#                                        VARIABLES QUE USAREMOS                                                #
################################################################################################################
# Datos del mundo
mundo_x = -1
mundo_y = -1
obstaculos = -1 # 0 será manual, 1 aleatorio y 2 por fichero 
# Datos del coche
coche_x = -1
coche_y = -1
direcciones = -1
# Datos de la persona
destino_x = -1
destino_y = -1
# Obstaculos
porcentaje_obstaculos = 1
obstaculos_x = -1
obstaculos_y = -1
# Heuristica
heuristica = -1

################################################################################################################
#                                            VENTANA TKINTER                                                   #
################################################################################################################
from tkinter import *
from PIL import ImageTk, Image
########################################## Datos de la ventana ########################################
window = Tk()
window.columnconfigure(0, weight=1)
window.rowconfigure(0, weight=1)
window_size = str(ancho_monitor) + 'x' + str(largo_monitor)
window.geometry(window_size)
window.resizable(0, 0)
window.title("Pixel Uber")
window.iconphoto(False, PhotoImage(file='Imagenes/icono.png'))
fondo = ImageTk.PhotoImage(file="Imagenes/back.gif")
canvas = Canvas(window, width= 800, height=600)
canvas.pack(fill="both",expand=TRUE)
canvas.create_image(0, 0, image=fondo, anchor="nw")
############################################## Funciones ##############################################

def resizer(e):
    global fondo1, resized_fondo1, fondo_nuevo
    fondo1 = Image.open("Imagenes/back.gif")
    resized_fondo1 = fondo1.resize((e.width, e.height), Image.ANTIALIAS)
    fondo_nuevo = ImageTk.PhotoImage(resized_fondo1)
    canvas.create_image(0, 0, image=fondo_nuevo, anchor="nw")
    canvas.create_text((ancho_monitor/2),30, font=('04b','30'), text="Pixel Uber", fill="white")
    canvas.create_text((ancho_monitor/2),70, font=('04b','20'), text="Selecciona las opciones",fill="red")
    canvas.create_text((ancho_monitor/4),100, font=('04b','15'), text="Ancho del mundo")
    canvas.create_text(((ancho_monitor/4)*3),100, font=('04b','15'), text="Largo del mundo")
    canvas.create_text((ancho_monitor/2),180, font=('04b','15'), text="Obstaculos")
    canvas.create_text((ancho_monitor/4),250, font=('04b','15'), text="Cordenadas del coche")
    canvas.create_text((ancho_monitor/4)*3,250, font=('04b','15'), text="Destino")
    canvas.create_text((ancho_monitor/2), 320, font=('04b','15'), text="Direcciones del coche")
    canvas.create_text((ancho_monitor/2), 450, font=('04b','15'), text="Funcion heuristica")


def Manualmente():
    global obstaculos
    obstaculos = 0

def Random():
    global obstaculos
    obstaculos = 1

def Ficheros():
    global obstaculos
    obstaculos = 2

def CuatroDir():
    global direcciones
    direcciones = True

def OchoDir():
    global direcciones
    direcciones = False

def Manhattan():
    global heuristica
    heuristica = 1

def Euclidea():
    global heuristica
    heuristica = 2

def ComprobarDatos():
    global window
    global mundo_x
    global mundo_y
    global coche_x
    global coche_y
    global destino_x
    global destino_y
    global direcciones
    global obstaculos
    if mundo_x == -1 or mundo_y == -1 or obstaculos == -1 or coche_x == -1 or coche_y == -1 or direcciones == -1 or destino_x == -1 or destino_y == -1 or heuristica == -1:
        aviso_vacio = Tk()
        aviso_vacio.minsize(width=250, height=100)
        aviso_vacio.title("Campos vacíos")
        Label(aviso_vacio, text="Hay campos sin rellenar",font=("04b", 15)).pack()
    elif not mundo_x.isdigit() or not mundo_y.isdigit() or not coche_x.isdigit() or not coche_y.isdigit() or not destino_x.isdigit() or not destino_y.isdigit():
        aviso_tipo = Tk()
        aviso_tipo.minsize(width=250, height=100)
        aviso_tipo.title("Tipos incompatibles")
        Label(aviso_tipo, text="Tipos de datos incompatibles, por favor revise cada campo.",font=("04b", 15)).pack()
    elif int(coche_x) > int(mundo_x) or int(coche_y) > int(mundo_y) or int(destino_x) > int(mundo_x) or int(destino_y) > int(mundo_y):
        aviso_limites = Tk()
        aviso_limites.minsize(width=250, height=100)
        aviso_limites.title("¡ Fuera de limites !")
        Label(aviso_limites, text="Las coordenadas del coche o del destino estan fuera del rango del mundo.",font=("04b", 15)).pack()
    elif int(coche_x) == int(destino_x) and int(coche_y) == int(destino_y):
        aviso_limites = Tk()
        aviso_limites.minsize(width=250, height=100)
        aviso_limites.title("No pueden ser iguales !")
        Label(aviso_limites, text="Las coordenadas del coche y del destino no pueden ser iguales.",font=("04b", 15)).pack()
    elif int(coche_x) < 1 or int(coche_y) < 1 or int(destino_x) < 1 or int(destino_y) < 1:
        aviso_limites = Tk()
        aviso_limites.minsize(width=250, height=100)
        aviso_limites.title("¡ Limites !")
        Label(aviso_limites, text="Por favor introduzca valores mayores que 0.",font=("04b", 15)).pack()
    else:
        window.destroy()

def Start():
    global mundo_x
    global mundo_y
    global coche_x
    global coche_y
    global destino_x
    global destino_y
    mundo_y = entrada_mundo_x.get() 
    mundo_x = entrada_mundo_y.get()
    coche_y = entrada_coche_x.get() 
    coche_x = entrada_coche_y.get() 
    destino_y = entrada_destino_x.get()
    destino_x = entrada_destino_y.get()
    ComprobarDatos()

########################################## Widgets del canvas #########################################

canvas.create_text((ancho_monitor/2),30, font=('04b','30'), text="Pixel Uber", fill="white")
canvas.create_text((ancho_monitor/2),70, font=('04b','20'), text="Selecciona las opciones",fill="red")

canvas.create_text((ancho_monitor/4),100, font=('04b','15'), text="Ancho del mundo")
canvas.create_text(((ancho_monitor/4)*3),100, font=('04b','15'), text="Largo del mundo")

entrada_mundo_x = Entry(window,font=("04b", 15),fg="red")
entrada_mundo_x_window = canvas.create_window((ancho_monitor/4), 140, window=entrada_mundo_x)

entrada_mundo_y = Entry(window,font=("04b", 15),fg="red")
entrada_mundo_y_window = canvas.create_window(((ancho_monitor/4)*3), 140, window=entrada_mundo_y)

canvas.create_text((ancho_monitor/2),180, font=('04b','15'), text="Obstaculos")
aleatorios = Button(window, text="Aleatoriamente", font=("04b", 10), bg="white", fg = "red",command=Random)
manuales = Button(window, text="Manualmente", font=("04b", 10), bg="white", fg = "red", command=Manualmente)
fichero = Button(window, text="Por fichero", font=("04b", 10), bg="white", fg = "red", command=Ficheros)
aleatorios.place(x = (ancho_monitor/8)*3,y = 200)
manuales.place(x = (ancho_monitor/6)*3,y = 200)
fichero.place(x = (ancho_monitor/11)*5,y = 250)

canvas.create_text((ancho_monitor/4),250, font=('04b','15'), text="Cordenadas del coche")
entrada_coche_x = Entry(window,font=("04b", 15),fg="red")
entrada_coche_y = Entry(window,font=("04b", 15),fg="red")
entrada_coche_x_window = canvas.create_window((ancho_monitor/10)*2, 280, width=150,window=entrada_coche_x)
entrada_coche_y_window = canvas.create_window((ancho_monitor/10)*3, 280, width=150,window=entrada_coche_y)

canvas.create_text((ancho_monitor/4)*3,250, font=('04b','15'), text="Destino")
entrada_destino_x = Entry(window,font=("04b", 15),fg="red")
entrada_destino_y = Entry(window,font=("04b", 15),fg="red")
entrada_destino_x_window = canvas.create_window((ancho_monitor/10)*7, 280, width=150,window=entrada_destino_x)
entrada_destino_y_window = canvas.create_window((ancho_monitor/10)*8, 280, width=150,window=entrada_destino_y)

canvas.create_text((ancho_monitor/2), 320, font=('04b','15'), text="Direcciones del coche")
aleatorios = Button(window, text="4-Direcciones", font=("04b", 10), fg="red", command=CuatroDir)
manuales = Button(window, text="8-Direcciones", font=("04b", 10), fg="red", command=OchoDir)
aleatorios.place(x=(ancho_monitor/8)*3,y = 380)
manuales.place(x=(ancho_monitor/6)*3,y = 380)

canvas.create_text((ancho_monitor/2), 450, font=('04b','15'), text="Funcion heuristica")
manhattan = Button(window, text="Manhattan", font=("04b", 10), fg="red", command=Manhattan)
euclidea = Button(window, text="Euclidea", font=("04b", 10), fg="red", command=Euclidea)
manhattan.place(x=(ancho_monitor/8)*3,y = 500)
euclidea.place(x=(ancho_monitor/6)*3,y = 500)



start = Button(window, text="START", font=("04b", 30), fg="red", command=Start)
start.place(x=(ancho_monitor/10)*4, y=650)

canvas.update()
window.bind('<Configure>', resizer)
window.mainloop()
########################################## Ventana obstáculos #########################################
ventana_obstaculos = Tk()

def Comprobar():
    global porcentaje_obstaculos
    porcentaje_obstaculos = entrada_porcentaje.get()
    if not porcentaje_obstaculos.isdigit() or int(porcentaje_obstaculos) > 100:
        aviso = Tk()
        aviso.minsize(250,250)
        aviso.title("Cuidado")
        Label(aviso, text="Porfavor, elija un numero mayor a 0 y menor que 100",font=("04b", 10)).pack()
    else:
        ventana_obstaculos.destroy()

if obstaculos == 1:
    global porcentaje
    ventana_obstaculos.geometry('700x300')
    ventana_obstaculos.resizable(0,0)
    ventana_obstaculos.title("Obstaculos")
    Label(ventana_obstaculos, text="Porcentaje de los obstaculos",font=("04b", 10)).pack()
    entrada_porcentaje = Entry(ventana_obstaculos, font=("04b", 10),fg="red")
    entrada_porcentaje.pack()
    comprobar = Button(ventana_obstaculos, text="Comprobar", font=("04b", 10), command=Comprobar)
    comprobar.pack()
else:
    ventana_obstaculos.destroy()

ventana_obstaculos.mainloop()