from tkinter.constants import END, FALSE, TRUE, X
import pygame
from queue import PriorityQueue
from pygame.constants import APPACTIVE, RESIZABLE
from math import sqrt
import random
import sys
from A_Inicio_tkinter import *
import decimal
import time

#Código de colores
ROJO_FINAL = (255, 0, 0)
VERDE = (0, 255, 0)
BLANCO = (255, 255, 255)
NEGRO_BARRERA = (0, 0, 0)
AMARILLO_CAMINO = (228, 255, 0)
NARANJA_TRAZA = (255, 127, 0)

#Código de números (matríz)
FONDO_VACIO = 0
INICIO = 1
FINAL = 2
BARRERA = 3
CAMINO = 4
TRAZA = 5

COLORFONDO = (255, 255, 255)


context = decimal.getcontext()
FLOTANTE_MAX = float(context.Emax)

nodos_celdas= []
trace = []
contador = 1
nodos_camino = 1
############################################################################################################################
#                                                   Clase Mundo                                                            #
############################################################################################################################
class Mundo:
    def __init__(self, filas, columnas, modo):
        self.filas = filas
        self.columnas = columnas
        self.Mundo = self.__make_Mundo(modo)

################################################ Getters y setters ################################################
    
    def get_n_filas(self):
        return self.filas
    
    def get_n_columnas(self):
        return self.columnas
    
    def get_Mundo(self):
        return self.Mundo

    def set_inicio(self, fila, columna):
        self.Mundo[fila - 1][columna -1] = INICIO
    
    def set_final(self, fila, columna):
        self.Mundo[fila - 1][columna -1] = FINAL

    def set_barrera(self, fila, columna):
        self.Mundo[fila - 1][columna - 1] = BARRERA
    
    def set_limpiar(self, fila, columna):
        self.Mundo[fila - 1][columna -1] = FONDO_VACIO
    
    def set_camino(self, fila, columna):
        self.Mundo[fila][columna] = CAMINO
    
    def set_traza(self, fila, columna):
        self.Mundo[fila][columna] = TRAZA
################################################ Estado de cada nodo ################################################    
    def es_inicio(self, fila, columna):
        return self.Mundo[fila][columna] == INICIO
    
    def es_final(self, fila, columna):
        return self.Mundo[fila][columna] == FINAL
    
    def es_barrera(self, fila, columna):
        return self.Mundo[fila][columna] == BARRERA
    
    def es_libre(self, fila, columna):
        return self.Mundo[fila][columna] == FONDO_VACIO
    
    def es_valido(self, fila, columna):
        return (fila >= 0) and (fila <= int(self.get_n_filas() - 1)) and (columna >= 0) and (columna <= int(self.get_n_columnas() - 1))
    
    def todo_barrera(self):
      for i in range(self.get_n_filas()):
        for j in range(self.get_n_columnas()):
            if (self.es_libre(int(i), int(j))):
              return False
      return True
    
################################################ Posicion clickada ################################################ 
    def posicion_clicked(self, SCREEN ,click):
        x , y = click

        Tamaño_bloque_i = SCREEN.get_width() / self.get_n_columnas()
        Tamaño_bloque_j = SCREEN.get_height() / self.get_n_filas()

        columna = int( (x / Tamaño_bloque_i) % self.get_n_columnas() )
        fila = int( (y / Tamaño_bloque_j) % self.get_n_filas() )

        return fila, columna
    
################################################ Matriz Mundo ################################################
    def __make_Mundo(self, modo):
        aux = []
        for i in range(self.get_n_filas()):
          aux.append([])
          for j in range(self.get_n_columnas()):
            aux[i].append(FONDO_VACIO)  
        return aux
      
################################################ Dibujar Mundo ################################################    
    def DibujarMundo(self, SCREEN):
      Tamaño_bloque_i = SCREEN.get_width() / self.get_n_columnas()
      Tamaño_bloque_j = SCREEN.get_height() / self.get_n_filas()
      i = 0
      while( i < SCREEN.get_width()):
        aux_i = round(i / Tamaño_bloque_i) % self.get_n_columnas()
        j = 0
        while( j < SCREEN.get_height()):
          aux_j = round(j / Tamaño_bloque_j) % self.get_n_filas()

          rect = pygame.Rect(i, j, Tamaño_bloque_i, Tamaño_bloque_j)
          if(int(self.Mundo[int(aux_j)][int(aux_i)]) == FONDO_VACIO):
            pygame.draw.rect(SCREEN, COLORFONDO, rect, 0)
          elif(int(self.Mundo[int(aux_j)][int(aux_i)]) == INICIO):
            pygame.draw.rect(SCREEN, VERDE, rect, 0)
          elif(int(self.Mundo[int(aux_j)][int(aux_i)]) == FINAL):
            pygame.draw.rect(SCREEN, ROJO_FINAL, rect, 0)
          elif(int(self.Mundo[int(aux_j)][int(aux_i)]) == BARRERA):
            pygame.draw.rect(SCREEN, NEGRO_BARRERA, rect, 0)
          elif(int(self.Mundo[int(aux_j)][int(aux_i)]) == CAMINO):
            pygame.draw.rect(SCREEN, AMARILLO_CAMINO, rect, 0)
          elif(int(self.Mundo[int(aux_j)][int(aux_i)]) == TRAZA):
            pygame.draw.rect(SCREEN, NARANJA_TRAZA, rect, 0)


          j += Tamaño_bloque_j
        i += Tamaño_bloque_i

################################################ Posicion valida ################################################    
    def PosicionValida(self, x, y):
      if int(x) >= 0 and int(y) >= 0 and int(x) <= int(self.filas-1) and int(y) <= int(self.columnas-1) and not self.es_barrera(x, y):
          return True
      else:
        return False
################################################ Interpretar camino  ################################################     
    def camino(self, camino):
      if (camino == None):
        return 

      for punto in camino:
        x , y = punto
        if not self.es_final(int(x), int(y)):
          self.set_camino(x, y)

    def definir_traza(self):
      global trace
      for punto in trace:
        x , y = punto
        if not self.es_final(int(x), int(y)) and not self.es_inicio(int(x), int(y)):
          self.set_traza(x, y)

    def traza(self): 
      global nodos_celdas, trace, contador, FLOTANTE_MAX
      for i in range(self.get_n_filas()):
        for j in range(self.get_n_columnas()):
          if  nodos_celdas[i][j].f != FLOTANTE_MAX :
            trace.append(nodos_celdas[i][j].posicion)
            contador = contador + 1
      self.definir_traza()
          
############################################################################################################################
#                                                   Clase Nodo                                                             #
############################################################################################################################

class Nodo:
  def __init__(self, x, y, padre_x, padre_y, f, g, h):
    self.x = x 
    self.y = y 
    self.posicion = x,y
    self.padre_x = padre_x
    self.padre_y = padre_y
    self.f = f
    self.g = g
    self.h = h

  #Comparamos los nodos
  def __eq__(self, other):
      return self.posicion == other.posicion
  
  #Función que ayuda a ordenar los nodos
  def __lt__(self, other):
    return self.f < other.f

################################################ Heurísticos  ################################################     
def DistanciaManhattan(actual_x, actual_y, destino_x, destino_y):
  return abs(actual_x- destino_x) + abs(actual_y - destino_y)

def DistanciaEuclidea(actual_x, actual_y, destino_x, destino_y):
  return sqrt((actual_x - destino_x)**2 + (actual_y -destino_y)**2)
################################################ Interpretar Camino  ################################################ 
def HacerCamino(nodos_celda, destino_x, destino_y):
  global coche_x, coche_y, nodos_camino
  fila = destino_x
  columna = destino_y
  camino = []
  coche_x = int(coche_x) - 1
  coche_y = int(coche_y) - 1
  while (True):
    nodos_camino = nodos_camino + 1
    posicion = fila, columna
    camino.append(posicion)
    aux_fila = nodos_celda[fila][columna].padre_x
    aux_columna = nodos_celda[fila][columna].padre_y
    fila = aux_fila
    columna = aux_columna
    if fila == coche_x and columna == coche_y:
      return camino[::1]

################################################ Algoritmo A* ocho ################################################ 
def AlgoritmoAestrella(mundo, inicio_x, inicio_y, destino_x, destino_y, heuristica):
  global nodos_celdas
  #Traza
  #Lista cerrada
  lista_cerrada = []
  #inicializamos los valores de la lista cerrada a falso.
  for i in range(mundo.get_n_filas()):
    lista_cerrada.append([])
    for j in range(mundo.get_n_columnas()):
      lista_cerrada[i].append(False)
  
  #Lista abierta
  lista_abierta = []

  #Inicializamos auxiliar Detalles celdas
  for i in range(mundo.get_n_filas()):
    nodos_celdas.append([])
    for j in range(mundo.get_n_columnas()):
      nodos_celdas[i].append(Nodo( i, j, -1, -1, FLOTANTE_MAX, FLOTANTE_MAX, FLOTANTE_MAX))

  #incializamos los parámetros para el nodo inicial
  nodos_celdas[inicio_x][inicio_y].f = 0.0
  nodos_celdas[inicio_x][inicio_y].g = 0.0
  nodos_celdas[inicio_x][inicio_y].h = 0.0
  nodos_celdas[inicio_x][inicio_y].padre_x = inicio_x
  nodos_celdas[inicio_x][inicio_y].padre_y = inicio_y

  #Insertamos el nodo en la lista abierta.
  lista_abierta.append(nodos_celdas[inicio_x][inicio_y])

  #final encontrado
  final_encontrado = False

  while len(lista_abierta) > 0:
    lista_abierta.sort()
    #Extraemos el valor de la lista abierta
    nodo_actual = lista_abierta.pop(0)
    #Añadimos el nodo a la lista cerrada.
    lista_cerrada[nodo_actual.x][nodo_actual.y] = True

    #Obtenemos los sucesores.
#sucesor norte.
    if mundo.es_valido(int(nodo_actual.x - 1), int(nodo_actual.y)) == True:
      #Caso en el que nos encontremos en el final con nuestro vecino
      if mundo.es_final(int(nodo_actual.x - 1), int(nodo_actual.y)) == True:
        nodos_celdas[int(nodo_actual.x - 1)][int(nodo_actual.y)].padre_x = nodo_actual.x
        nodos_celdas[int(nodo_actual.x - 1)][int(nodo_actual.y)].padre_y = nodo_actual.y
        camino = HacerCamino(nodos_celdas, destino_x, destino_y)
        final_encontrado = True
        return camino
      #En caso de que nos contremos que nuestro vecino no este en la lista cerrada o si no se encuentra bloqueado
      elif lista_cerrada[int(nodo_actual.x - 1)][int(nodo_actual.y)] == False and mundo.es_libre(int(nodo_actual.x - 1), int(nodo_actual.y)) == True:
        nueva_g = int(nodos_celdas[int(nodo_actual.x)][nodo_actual.y].g + 1)
        if(int(heuristica) == 1):
          nueva_h = DistanciaManhattan(int(nodo_actual.x - 1), int(nodo_actual.y), destino_x, destino_y)
        elif(int(heuristica) == 2):
          nueva_h= DistanciaEuclidea(int(nodo_actual.x - 1), int(nodo_actual.y), destino_x, destino_y)
        nueva_f = nueva_g + nueva_h

        #Si no se encuentra en la lista abierta se agrega o Si está en la lista compror si este camino es mejor que el existente
        if nodos_celdas[int(nodo_actual.x - 1)][int(nodo_actual.y)].f == FLOTANTE_MAX or nodos_celdas[int(nodo_actual.x - 1)][int(nodo_actual.y)].f > nueva_f:
          #Actualizamos los datos 
          nodos_celdas[int(nodo_actual.x - 1)][int(nodo_actual.y)].f = nueva_f
          nodos_celdas[int(nodo_actual.x - 1)][int(nodo_actual.y)].g = nueva_g
          nodos_celdas[int(nodo_actual.x - 1)][int(nodo_actual.y)].h = nueva_h
          nodos_celdas[int(nodo_actual.x - 1)][int(nodo_actual.y)].padre_x = nodo_actual.x
          nodos_celdas[int(nodo_actual.x - 1)][int(nodo_actual.y)].padre_y = nodo_actual.y
          
          
          #Guardamos el nodo en la lista abierta
          lista_abierta.append(nodos_celdas[int(nodo_actual.x - 1)][int(nodo_actual.y)])

#sucesor Sur
    if mundo.es_valido(int(nodo_actual.x + 1), int(nodo_actual.y)) == True:
      #Caso en el que nos encontremos en el final con nuestro vecino
      if mundo.es_final(int(nodo_actual.x + 1), int(nodo_actual.y)) == True:
        nodos_celdas[int(nodo_actual.x + 1)][int(nodo_actual.y)].padre_x = nodo_actual.x
        nodos_celdas[int(nodo_actual.x + 1)][int(nodo_actual.y)].padre_y = nodo_actual.y
        camino = HacerCamino(nodos_celdas, destino_x, destino_y)
        final_encontrado = True
        return camino
      #En caso de que nos contremos que nuestro vecino no este en la lista cerrada o si no se encuentra bloqueado
      elif lista_cerrada[int(nodo_actual.x + 1)][int(nodo_actual.y)] == False and mundo.es_libre(int(nodo_actual.x + 1), int(nodo_actual.y)) == True:
        nueva_g = int(nodos_celdas[int(nodo_actual.x)][int(nodo_actual.y)].g + 1)
        if(int(heuristica) == 1):
          nueva_h = DistanciaManhattan(int(nodo_actual.x + 1), int(nodo_actual.y), destino_x, destino_y)
        elif(int(heuristica) == 2):
          nueva_h= DistanciaEuclidea(int(nodo_actual.x + 1), int(nodo_actual.y), destino_x, destino_y)
        nueva_f = nueva_g + nueva_h

        #Si no se encuentra en la lista abierta se agrega o Si está en la lista compror si este camino es mejor que el existente
        if nodos_celdas[int(nodo_actual.x + 1)][int(nodo_actual.y)].f == FLOTANTE_MAX or nodos_celdas[int(nodo_actual.x + 1)][int(nodo_actual.y)].f > nueva_f:
          #Actualizamos los datos 
          nodos_celdas[int(nodo_actual.x + 1)][int(nodo_actual.y)].f = nueva_f
          nodos_celdas[int(nodo_actual.x + 1)][int(nodo_actual.y)].g = nueva_g
          nodos_celdas[int(nodo_actual.x + 1)][int(nodo_actual.y)].h = nueva_h
          nodos_celdas[int(nodo_actual.x + 1)][int(nodo_actual.y)].padre_x = nodo_actual.x
          nodos_celdas[int(nodo_actual.x + 1)][int(nodo_actual.y)].padre_y = nodo_actual.y
          
          #Guardamos el nodo en la lista abierta
          lista_abierta.append(nodos_celdas[int(nodo_actual.x + 1)][int(nodo_actual.y)])

#sucesor del este  
    if mundo.es_valido(int(nodo_actual.x), int(nodo_actual.y + 1 )) == True:
      #Caso en el que nos encontremos en el final con nuestro vecino
      if mundo.es_final(int(nodo_actual.x), int(nodo_actual.y + 1)) == True:
        nodos_celdas[int(nodo_actual.x)][int(nodo_actual.y + 1)].padre_x = nodo_actual.x
        nodos_celdas[int(nodo_actual.x)][int(nodo_actual.y + 1)].padre_y = nodo_actual.y
        camino = HacerCamino(nodos_celdas, destino_x, destino_y)
        final_encontrado = True
        return camino
      #En caso de que nos contremos que nuestro vecino no este en la lista cerrada o si no se encuentra bloqueado
      elif lista_cerrada[int(nodo_actual.x)][int(nodo_actual.y + 1)] == False and mundo.es_libre(int(nodo_actual.x), int(nodo_actual.y + 1)) == True:
        nueva_g = int(nodos_celdas[int(nodo_actual.x)][int(nodo_actual.y)].g + 1)
        if(int(heuristica) == 1):
          nueva_h = DistanciaManhattan(int(nodo_actual.x), int(nodo_actual.y + 1), destino_x, destino_y)
        elif(int(heuristica) == 2):
          nueva_h= DistanciaEuclidea(int(nodo_actual.x), int(nodo_actual.y + 1), destino_x, destino_y)
        nueva_f = nueva_g + nueva_h

        #Si no se encuentra en la lista abierta se agrega o Si está en la lista compror si este camino es mejor que el existente
        if nodos_celdas[int(nodo_actual.x)][nodo_actual.y + 1].f == FLOTANTE_MAX or nodos_celdas[int(nodo_actual.x)][int(nodo_actual.y + 1)].f > nueva_f:
          #Actualizamos los datos 
          nodos_celdas[int(nodo_actual.x)][int(nodo_actual.y + 1)].f = nueva_f
          nodos_celdas[int(nodo_actual.x)][int(nodo_actual.y + 1)].g = nueva_g
          nodos_celdas[int(nodo_actual.x)][int(nodo_actual.y + 1)].h = nueva_h
          nodos_celdas[int(nodo_actual.x)][int(nodo_actual.y + 1)].padre_x = nodo_actual.x
          nodos_celdas[int(nodo_actual.x)][int(nodo_actual.y + 1)].padre_y = nodo_actual.y
          

          #Guardamos el nodo en la lista abierta
          lista_abierta.append(nodos_celdas[int(nodo_actual.x)][int(nodo_actual.y + 1)])
  
#sucesor del oeste
    if mundo.es_valido(int(nodo_actual.x), int(nodo_actual.y - 1 )) == True:
      #Caso en el que nos encontremos en el final con nuestro vecino
      if mundo.es_final(int(nodo_actual.x), int(nodo_actual.y - 1)) == True:
        nodos_celdas[int(nodo_actual.x)][int(nodo_actual.y - 1)].padre_x = nodo_actual.x
        nodos_celdas[int(nodo_actual.x)][int(nodo_actual.y - 1)].padre_y = nodo_actual.y
        camino = HacerCamino(nodos_celdas, destino_x, destino_y)
        final_encontrado = True
        return camino
      #En caso de que nos contremos que nuestro vecino no este en la lista cerrada o si no se encuentra bloqueado
      elif lista_cerrada[int(nodo_actual.x)][int(nodo_actual.y - 1)] == False and mundo.es_libre(int(nodo_actual.x), int(nodo_actual.y - 1)) == True:
        nueva_g = int(nodos_celdas[int(nodo_actual.x)][nodo_actual.y].g + 1)
        if(int(heuristica) == 1):
          nueva_h = DistanciaManhattan(int(nodo_actual.x), int(nodo_actual.y - 1), destino_x, destino_y)
        elif(int(heuristica) == 2):
          nueva_h= DistanciaEuclidea(int(nodo_actual.x), int(nodo_actual.y - 1), destino_x, destino_y)
        nueva_f = nueva_g + nueva_h

        #Si no se encuentra en la lista abierta se agrega o Si está en la lista compror si este camino es mejor que el existente
        if nodos_celdas[int(nodo_actual.x)][nodo_actual.y - 1].f == FLOTANTE_MAX or nodos_celdas[int(nodo_actual.x)][int(nodo_actual.y - 1)].f > nueva_f:
          #Actualizamos los datos 
          nodos_celdas[int(nodo_actual.x)][int(nodo_actual.y - 1)].f = nueva_f
          nodos_celdas[int(nodo_actual.x)][int(nodo_actual.y - 1)].g = nueva_g
          nodos_celdas[int(nodo_actual.x)][int(nodo_actual.y - 1)].h = nueva_h
          nodos_celdas[int(nodo_actual.x)][int(nodo_actual.y - 1)].padre_x = nodo_actual.x
          nodos_celdas[int(nodo_actual.x)][int(nodo_actual.y - 1)].padre_y = nodo_actual.y
          

          #Guardamos el nodo en la lista abierta
          lista_abierta.append(nodos_celdas[int(nodo_actual.x)][int(nodo_actual.y - 1)])
    
    if direcciones == False:
  #sucesor del nor-este  
      if mundo.es_valido(int(nodo_actual.x - 1), int(nodo_actual.y + 1 )) == True:
        #Caso en el que nos encontremos en el final con nuestro vecino
        if mundo.es_final(int(nodo_actual.x - 1), int(nodo_actual.y + 1)) == True:
          nodos_celdas[int(nodo_actual.x - 1)][int(nodo_actual.y + 1)].padre_x = nodo_actual.x
          nodos_celdas[int(nodo_actual.x - 1)][int(nodo_actual.y + 1)].padre_y = nodo_actual.y
          camino = HacerCamino(nodos_celdas, destino_x, destino_y)
          final_encontrado = True
          return camino
        #En caso de que nos contremos que nuestro vecino no este en la lista cerrada o si no se encuentra bloqueado
        elif lista_cerrada[int(nodo_actual.x - 1)][int(nodo_actual.y + 1)] == False and mundo.es_libre(int(nodo_actual.x - 1), int(nodo_actual.y + 1)) == True:
          nueva_g = float(nodos_celdas[int(nodo_actual.x)][int(nodo_actual.y)].g + 1.41)
          if(int(heuristica) == 1):
            nueva_h = DistanciaManhattan(int(nodo_actual.x - 1), int(nodo_actual.y + 1), destino_x, destino_y)
          elif(int(heuristica) == 2):
            nueva_h= DistanciaEuclidea(int(nodo_actual.x - 1), int(nodo_actual.y + 1), destino_x, destino_y)
          nueva_f = nueva_g + nueva_h

          #Si no se encuentra en la lista abierta se agrega o Si está en la lista compror si este camino es mejor que el existente
          if nodos_celdas[int(nodo_actual.x - 1)][nodo_actual.y + 1].f == FLOTANTE_MAX or nodos_celdas[int(nodo_actual.x - 1)][int(nodo_actual.y + 1)].f > nueva_f:
            #Actualizamos los datos 
            nodos_celdas[int(nodo_actual.x - 1)][int(nodo_actual.y + 1)].f = nueva_f
            nodos_celdas[int(nodo_actual.x - 1)][int(nodo_actual.y + 1)].g = nueva_g
            nodos_celdas[int(nodo_actual.x - 1)][int(nodo_actual.y + 1)].h = nueva_h
            nodos_celdas[int(nodo_actual.x - 1)][int(nodo_actual.y + 1)].padre_x = nodo_actual.x
            nodos_celdas[int(nodo_actual.x - 1)][int(nodo_actual.y + 1)].padre_y = nodo_actual.y
            
            #Guardamos el nodo en la lista abierta
            lista_abierta.append(nodos_celdas[int(nodo_actual.x - 1)][int(nodo_actual.y + 1)])

  #sucesor del nor-oeste  
      if mundo.es_valido(int(nodo_actual.x - 1), int(nodo_actual.y - 1 )) == True:
        #Caso en el que nos encontremos en el final con nuestro vecino
        if mundo.es_final(int(nodo_actual.x - 1), int(nodo_actual.y - 1)) == True:
          nodos_celdas[int(nodo_actual.x - 1)][int(nodo_actual.y - 1)].padre_x = nodo_actual.x
          nodos_celdas[int(nodo_actual.x - 1)][int(nodo_actual.y - 1)].padre_y = nodo_actual.y
          camino = HacerCamino(nodos_celdas, destino_x, destino_y)
          final_encontrado = True
          return camino
        #En caso de que nos contremos que nuestro vecino no este en la lista cerrada o si no se encuentra bloqueado
        elif lista_cerrada[int(nodo_actual.x - 1)][int(nodo_actual.y - 1)] == False and mundo.es_libre(int(nodo_actual.x - 1), int(nodo_actual.y - 1)) == True:
          nueva_g = float(nodos_celdas[int(nodo_actual.x)][int(nodo_actual.y)].g + 1.41)
          if(int(heuristica) == 1):
            nueva_h = DistanciaManhattan(int(nodo_actual.x - 1), int(nodo_actual.y - 1), destino_x, destino_y)
          elif(int(heuristica) == 2):
            nueva_h= DistanciaEuclidea(int(nodo_actual.x - 1), int(nodo_actual.y - 1), destino_x, destino_y)
          nueva_f = nueva_g + nueva_h

          #Si no se encuentra en la lista abierta se agrega o Si está en la lista compror si este camino es mejor que el existente
          if nodos_celdas[int(nodo_actual.x - 1)][nodo_actual.y - 1].f == FLOTANTE_MAX or nodos_celdas[int(nodo_actual.x - 1)][int(nodo_actual.y - 1)].f > nueva_f:
            #Actualizamos los datos 
            nodos_celdas[int(nodo_actual.x - 1)][int(nodo_actual.y - 1)].f = nueva_f
            nodos_celdas[int(nodo_actual.x - 1)][int(nodo_actual.y - 1)].g = nueva_g
            nodos_celdas[int(nodo_actual.x - 1)][int(nodo_actual.y - 1)].h = nueva_h
            nodos_celdas[int(nodo_actual.x - 1)][int(nodo_actual.y - 1)].padre_x = nodo_actual.x
            nodos_celdas[int(nodo_actual.x - 1)][int(nodo_actual.y - 1)].padre_y = nodo_actual.y
            

            #Guardamos el nodo en la lista abierta
            lista_abierta.append(nodos_celdas[int(nodo_actual.x - 1)][int(nodo_actual.y - 1)])

  #sucesor del sur-este 
      if mundo.es_valido(int(nodo_actual.x + 1), int(nodo_actual.y + 1 )) == True:
        #Caso en el que nos encontremos en el final con nuestro vecino
        if mundo.es_final(int(nodo_actual.x + 1), int(nodo_actual.y + 1)) == True:
          nodos_celdas[int(nodo_actual.x + 1)][int(nodo_actual.y + 1)].padre_x = nodo_actual.x
          nodos_celdas[int(nodo_actual.x + 1)][int(nodo_actual.y + 1)].padre_y = nodo_actual.y
          camino = HacerCamino(nodos_celdas, destino_x, destino_y)
          final_encontrado = True
          return camino
        #En caso de que nos contremos que nuestro vecino no este en la lista cerrada o si no se encuentra bloqueado
        elif lista_cerrada[int(nodo_actual.x + 1)][int(nodo_actual.y + 1)] == False and mundo.es_libre(int(nodo_actual.x + 1), int(nodo_actual.y + 1)) == True:
          nueva_g = float(nodos_celdas[int(nodo_actual.x)][int(nodo_actual.y)].g + 1.41)
          if(int(heuristica) == 1):
            nueva_h = DistanciaManhattan(int(nodo_actual.x + 1), int(nodo_actual.y + 1), destino_x, destino_y)
          elif(int(heuristica) == 2):
            nueva_h= DistanciaEuclidea(int(nodo_actual.x + 1), int(nodo_actual.y + 1), destino_x, destino_y)
          nueva_f = nueva_g + nueva_h

          #Si no se encuentra en la lista abierta se agrega o Si está en la lista compror si este camino es mejor que el existente
          if nodos_celdas[int(nodo_actual.x + 1)][nodo_actual.y + 1].f == FLOTANTE_MAX or nodos_celdas[int(nodo_actual.x + 1)][int(nodo_actual.y + 1)].f > nueva_f:
            #Actualizamos los datos 
            nodos_celdas[int(nodo_actual.x + 1)][int(nodo_actual.y + 1)].f = nueva_f
            nodos_celdas[int(nodo_actual.x + 1)][int(nodo_actual.y + 1)].g = nueva_g
            nodos_celdas[int(nodo_actual.x + 1)][int(nodo_actual.y + 1)].h = nueva_h
            nodos_celdas[int(nodo_actual.x + 1)][int(nodo_actual.y + 1)].padre_x = nodo_actual.x
            nodos_celdas[int(nodo_actual.x + 1)][int(nodo_actual.y + 1)].padre_y = nodo_actual.y
            

            #Guardamos el nodo en la lista abierta
            lista_abierta.append(nodos_celdas[int(nodo_actual.x + 1)][int(nodo_actual.y + 1)])

  #sucesor del sur-oeste
      if mundo.es_valido(int(nodo_actual.x + 1), int(nodo_actual.y - 1 )) == True:
        #Caso en el que nos encontremos en el final con nuestro vecino
        if mundo.es_final(int(nodo_actual.x + 1), int(nodo_actual.y - 1)) == True:
          nodos_celdas[int(nodo_actual.x + 1)][int(nodo_actual.y - 1)].padre_x = nodo_actual.x
          nodos_celdas[int(nodo_actual.x + 1)][int(nodo_actual.y - 1)].padre_y = nodo_actual.y
          camino = HacerCamino(nodos_celdas, destino_x, destino_y)
          final_encontrado = True
          return camino
        #En caso de que nos contremos que nuestro vecino no este en la lista cerrada o si no se encuentra bloqueado
        elif lista_cerrada[int(nodo_actual.x + 1)][int(nodo_actual.y - 1)] == False and mundo.es_libre(int(nodo_actual.x - 1), int(nodo_actual.y - 1)) == True:
          nueva_g = float(nodos_celdas[int(nodo_actual.x)][int(nodo_actual.y)].g + 1.41)
          if(int(heuristica) == 1):
            nueva_h = DistanciaManhattan(int(nodo_actual.x + 1), int(nodo_actual.y - 1), destino_x, destino_y)
          elif(int(heuristica) == 2):
            nueva_h= DistanciaEuclidea(int(nodo_actual.x + 1), int(nodo_actual.y - 1), destino_x, destino_y)
          nueva_f = nueva_g + nueva_h

          #Si no se encuentra en la lista abierta se agrega o Si está en la lista compror si este camino es mejor que el existente
          if nodos_celdas[int(nodo_actual.x + 1)][nodo_actual.y - 1].f == FLOTANTE_MAX or nodos_celdas[int(nodo_actual.x + 1)][int(nodo_actual.y - 1)].f > nueva_f:
            #Actualizamos los datos 
            nodos_celdas[int(nodo_actual.x + 1)][int(nodo_actual.y - 1)].f = nueva_f
            nodos_celdas[int(nodo_actual.x + 1)][int(nodo_actual.y - 1)].g = nueva_g
            nodos_celdas[int(nodo_actual.x + 1)][int(nodo_actual.y - 1)].h = nueva_h
            nodos_celdas[int(nodo_actual.x + 1)][int(nodo_actual.y - 1)].padre_x = nodo_actual.x
            nodos_celdas[int(nodo_actual.x + 1)][int(nodo_actual.y - 1)].padre_y = nodo_actual.y
            

            #Guardamos el nodo en la lista abierta
            lista_abierta.append(nodos_celdas[int(nodo_actual.x + 1)][int(nodo_actual.y - 1)])

  if(final_encontrado == False):
    aviso_vacio = Tk()
    aviso_vacio.minsize(width=250, height=100)
    aviso_vacio.title("No hay solucion")
    Label(aviso_vacio, text="No hay solucion.",font=("04b", 15)).pack()
    aviso_vacio.mainloop()
    return None

def DatosFinales(tiempo):
  global contador, nodos_camino, heuristica, resultado
  if int(heuristica) == 1:
    funcion = "Manhattan:"
  else:
    funcion = "Euclidea: "
  camino_nodos = "El camino tiene: " + str(nodos_camino) + " nodos."
  nodos_visitados = "El algoritmo visito: " + str(contador) + " nodos."  
  tiempo_final = "El algoritmo tardo: " + str(tiempo*1000) + " milisegundos."
  resultado = Tk()
  resultado.minsize(width=250, height=250)
  resultado.title("Resultado")
  Label(resultado, text=funcion,font=("Times New Roman", 25)).pack()
  Label(resultado, text=camino_nodos,font=("Times New Roman", 15)).pack()
  Label(resultado, text=nodos_visitados,font=("Times New Roman", 15)).pack()
  Label(resultado, text=tiempo_final,font=("Times New Roman", 15)).pack()
  Button(resultado, text="Confirmar", font=("Times New Roman", 10), bg="white", fg = "red",command=destroy).pack()
  resultado.mainloop()

def destroy():
  global resultado
  resultado.destroy()