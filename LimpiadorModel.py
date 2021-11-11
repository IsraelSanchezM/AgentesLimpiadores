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

def movimientosAgentes(model):
    """
    Función que suma todos los movimientos de los agentes
    Parámetros: 
    model - modelo al que pertenece la función
    Retornos:
    sum(movAgentes) - sumatoria de todos los movimientos de los agentes
    """
    #Se crea un arreglo con todos los movimientos de todos los agentes
    movAgentes = [agent.movimientos for agent in model.schedule.agents]
    #Se regresa la suma de todos los movimientos
    return sum(movAgentes)

def calcCeldasLimpias(model):
    """
    Función que calcula el procentaje de celdas limpias
    Parámetros: 
    model - modelo al que pertenece la función
    Retornos:
    cells - porcentaje de celdas limpias
    """
    #Se le resta al 100% el porcentaje no limpio
    cells = 100 - (len(model.dirtyCells) * 100/ model.cells)
    #Se regresa el procentaje de celdas limpias
    return cells

def calcTiempo(model):
    """
    Función que calcula el tiempo (en pasos) usado hasta ahora
    Parámetros: 
    model - modelo al que pertenece la función
    Retornos:
    model.schedule.time - tiempo (en pasos) que tiene el modelo actualmente
    """
    return model.schedule.time
    

class LimpiadorModel(Model):
    """Modelo de los limpiadores"""
    def __init__(self, N, width, height, percent, time):
        #Atributos
        self.numAgents = N
        self.grid = MultiGrid(width, height, True)
        self.cells = width * height
        self.dirtyCells = []
        self.schedule = SimultaneousActivation(self)
        self.percent = percent
        self.time = time
        self.running = True

        #Se crean los agentes
        for i in range(self.numAgents):
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
            if(temp not in self.dirtyCells):
                #Si no existen las coordenadas en el arreglo de celdas sucias se agregan
                self.dirtyCells.append(temp)
                #Se crea un agente de tipo suciedad, se agrega al schedule y al tablero
                dirt = Suciedad(dirty, self)
                self.schedule.add(dirt)
                self.grid.place_agent(dirt, temp)
                dirty -= 1

        #Se inicializa el collector de datos del modelo
        self.datacollector = DataCollector(
            model_reporters = {"Movimientos": movimientosAgentes,
                                "% Celdas Limpias": calcCeldasLimpias,
                                "Tiempo": calcTiempo}
        )
    
    def step(self):
        """
        Función que avanza un paso en en modelo
        Parámetros: 
        self - modelo al que pertenece la función
        Retorno:
        Nada
        """ 
        if(len(self.dirtyCells) > 0 and self.schedule.time <= self.time):
            #Si todavía hay celdas sucias se continúa iterando
            self.datacollector.collect(self)
            self.schedule.step()
        else:
            #De lo contrario se acaba la simulación
            self.datacollector.collect(self)
            self.running = False            
            print("Tiempo alcanzado: " + str(self.schedule.time))
            print("Celdas faltantes: " + str(self.dirtyCells))
            print("Porcentaje limpiado: " + str(calcCeldasLimpias(self)))
            print("Movimientos totales: " + str(movimientosAgentes(self)))

class AgenteLimpiador(Agent):
    """Agente que limpiará la celda"""
    def __init__(self, unique_id, model):
        #Atributos
        super().__init__(unique_id, model)
        self.celdasLimpiadas = 0
        self.movimientos = 0
    
    def aspirar(self, cell):
        """
        Función que aspira celda actual
        Parámetros: 
        self - agente al que pertenece la función
        cell - celda en la que se encuentra el agente
        Retorno:
        Nada
        """
        #Se limpia la celda, es decir, se quita del arreglo de celdas sucias
        self.celdasLimpiadas += 1
        self.model.dirtyCells.remove(cell)
    
    def move(self):
        """
        Función que mueve al agente a una celda vecina aleatoria
        Parámetros: 
        self - agente al que pertenece la función
        Retorno:
        Nada
        """
        #Se obtienen los vecinos del agente
        self.movimientos += 1
        possibleSteps = self.model.grid.get_neighborhood(
            self.pos,
            moore = True,
            include_center = False
        )
        #Se escoge una posición aleatoria de entre los vecinos
        newPos = self.random.choice(possibleSteps)
        #Se mueve el agente
        self.model.grid.move_agent(self, newPos)

    def step(self):
        """
        Función que realiza ls acciones de cada agente en cada paso
        Parámetros: 
        self - agente al que pertenece la función
        Retorno:
        Nada
        """
        if(self.pos in self.model.dirtyCells):
            #Si la celda está sucia se aspira
            self.aspirar(self.pos)
        else:
            #De lo contrario el agente se mueve
            self.move()

class Suciedad(Agent):
    """Clase que modela la suciedad en el tablero"""
    def __init__(self, unique_id, model):
        #Atributos
        super().__init__(unique_id, model)
        self.dirty = True  #True -> la celda está sucia; False -> la celda está limpia 
        self.movimientos = 0

    def step(self):
        """
        Función que realiza ls acciones de cada agente en cada paso
        Parámetros: 
        self - agente al que pertenece la función
        Retorno:
        Nada
        """
        #Actualizar el tablero
        if(self.pos not in self.model.dirtyCells and self.dirty):
            #Si la celda ya no está sucia se "limpia" del tablero
            self.model.grid.remove_agent(self)
            self.dirty = False
