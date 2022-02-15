import random
import sys
from Clases import *

def main():
    
    global SCREEN
    pygame.init()
    SCREEN = pygame.display.set_mode((ancho_monitor - 100, largo_monitor - 100), pygame.RESIZABLE)
    mundo = Mundo(int(mundo_x), int(mundo_y), True)
    global casillas_totales, casillas_aleatorias, aleatoria_x, aleatoria_y
    casillas_totales = int(mundo_x) * int(mundo_y)
    casillas_aleatorias = int(casillas_totales) * (int(porcentaje_obstaculos) / 100)
    if int(obstaculos) == 1:
        while (int(casillas_aleatorias) != 0):
            aleatoria_x = random.randint(1, int(mundo_x))
            aleatoria_y = random.randint(1, int(mundo_y))
            if (not mundo.es_barrera(int(aleatoria_x - 1), int(aleatoria_y - 1)) and not mundo.es_final(int(aleatoria_x - 1), int(aleatoria_y - 1)) and not mundo.es_inicio(int(aleatoria_x - 1), int(aleatoria_y - 1))):
                mundo.set_barrera(aleatoria_x, aleatoria_y)
                casillas_aleatorias = int(casillas_aleatorias) - 1
            if mundo.todo_barrera():
                break
    elif int(obstaculos) == 2:
        with open("Obstaculos.txt", "rt") as f:
            for linea in f:
                obstaculos_x = linea
                obstaculos_y = f.readline().strip()
                if (not mundo.es_barrera(int(obstaculos_x), int(obstaculos_y)) and not mundo.es_final(int(obstaculos_x), int(obstaculos_y)) and not mundo.es_inicio(int(obstaculos_x), int(obstaculos_y))):
                    mundo.set_barrera(int(obstaculos_x),int(obstaculos_y))
    while True:
        SCREEN.fill(COLORFONDO)
        mundo.DibujarMundo(SCREEN)
        pygame.display.update()
        mundo.set_inicio(int(coche_x), int(coche_y))
        mundo.set_final(int(destino_x), int(destino_y))
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if int(obstaculos) == 0:
                #click izquierdo añade
                if pygame.mouse.get_pressed()[0]: 
                    click = pygame.mouse.get_pos()
                    filas , columnas = mundo.posicion_clicked(SCREEN, click)
                    mundo.set_barrera(filas + 1, columnas + 1)
            
                #click derecho borra
                if pygame.mouse.get_pressed()[2]:
                    click = pygame.mouse.get_pos()
                    filas , columnas = mundo.posicion_clicked(SCREEN, click)

                    if(mundo.es_final(filas, columnas) == False and mundo.es_inicio(filas, columnas) == False):
                        mundo.set_limpiar(filas + 1, columnas + 1)
            if event.type == pygame.VIDEORESIZE:
              # There's some code to add back window content here.
              SCREEN = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
        
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    global trace
                    inicio_x = int(coche_x) - 1
                    inicio_y = int(coche_y) - 1 
                    final_x = int(destino_x) - 1
                    final_y = int(destino_y) - 1
                    inicio = time.time()
                    vector = AlgoritmoAestrella(mundo, inicio_x, inicio_y, final_x, final_y, heuristica)
                    final = time.time()
                    tiempo = final - inicio
                    mundo.traza()                  
                    mundo.camino(vector)
                    mundo.DibujarMundo
                    DatosFinales(tiempo)
                    
main()  