"""
Modelo y Agentes ocupados para el Sistema Multiagentes que simula
robots que limpian un tablero de N*M dimensiones

Autores:
David Rodríguez Fragoso A01748760
Erick Hernández Silva A01750170
Israel Sánchez Miranda A01378705
Renata Monserrat de Luna Flores A01750484
Roberto Valdez  Jasso A01746863

10/11/2021
"""

#Librerías a usar
from random import random
from mesa import Agent, Model
from mesa.time import SimultaneousActivation
from mesa.space import MultiGrid
from mesa.datacollection import DataCollector

def movimientos_agentes(model):
    """Función que suma todos los movimientos de los agentes"""
    #Se crea un arreglo con todos los movimientos de todos los agentes
    mov_agentes = [agent.movimientos for agent in model.schedule.agents]
    #Se regresa la suma de todos los movimientos
    return sum(mov_agentes)

def calc_celdas_limpias(model):
    """Función que calcula el procentaje de celdas limpias"""
    #Se le resta al 100% el porcentaje no limpio
    cells = 100 - (len(model.dirty_cells) * model.cells / 100)
    #Se regresa el procentaje de celdas limpias
    return cells

def calc_tiempo(model):
    """Función que calcula el tiempo (en pasos) usado hasta ahora"""
    return model.schedule.time
    

class LimpiadorModel(Model):
    """Modelo de los limpiadores"""
    def __init__(self, N, width, height, percent, time):
        self.num_agents = N
        self.grid = MultiGrid(width, height, True)
        self.cells = width * height
        self.dirty_cells = []
        self.schedule = SimultaneousActivation(self)
        self.percent = percent
        self.time = time
        self.running = True

        #Se crean los agentes
        for i in range(self.num_agents):
            limpiador = AgenteLimpiador("Limpiador " + str(i), self)
            self.schedule.add(limpiador)

            #Agregar a todos los agentes en la celda[1][1]
            self.grid.place_agent(limpiador, (0, 0))

        #Inicializar las celdas sucias:
        dirty = (self.percent * self.cells) // 100  #Número de celdas sucias
        while(dirty > 0):
            #Se asignan celdas sucias aleatoriamiente
            x = self.random.randrange(self.grid.width)
            y = self.random.randrange(self.grid.height)
            temp = (x, y)
            if(temp not in self.dirty_cells):
                #Si no existen las coordenadas en el arreglo de celdas sucias se agregan
                self.dirty_cells.append(temp)
                dirty -= 1

        self.datacollector = DataCollector(
            model_reporters = {"Movimientos": movimientos_agentes,
                                "% Celdas Limpias": calc_celdas_limpias,
                                "Tiempo": calc_tiempo}
        )
    
    def step(self):
        """Se avanza un paso en en modelo""" 
        if(len(self.dirty_cells) > 0 and self.schedule.time <= self.time):
            #Si todavía hay celdas sucias se continúa iterando
            self.datacollector.collect(self)
            self.schedule.step()
        else:
            #De lo contrario se acaba la simulación
            self.running = False
            print("Tiempo alcanzado: " + str(self.schedule.time))
            print("Celdas faltantes: " + str(self.dirty_cells))
            print("Porcentaje limpiado: " + str(calc_celdas_limpias(self)))
            print("Movimientos totales: " + str(movimientos_agentes(self)))

class AgenteLimpiador(Agent):
    """Agente que limpiará la celda"""
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.celdas_limpiadas = 0
        self.movimientos = 0
    
    def aspirar(self, cell):
        """Aspriar celda actual"""
        #Se limpia la celda, es decir, se quita del arreglo de celdas sucias
        self.celdas_limpiadas += 1
        self.model.dirty_cells.remove(cell)
    
    def move(self):
        """Mover a una celda vecina aleatoria"""
        #Se obtienen los vecinos del agente
        self.movimientos += 1
        possible_steps = self.model.grid.get_neighborhood(
            self.pos,
            moore = True,
            include_center = False
        )
        #Se escoge una posición aleatoria de entre los vecinos
        new_pos = self.random.choice(possible_steps)
        #Se mueve el agente
        self.model.grid.move_agent(self, new_pos)

    def step(self):
        """Acciones que realizan los agentes en cada paso"""
        if(self.pos in self.model.dirty_cells):
            #Si la celda está sucia se aspira
            self.aspirar(self.pos)
        else:
            #De lo contrario el agente se mueve
            self.move()