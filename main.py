"""
Programa principal que se ejcuta para visualizar el Sistema Multiagentes

Autores:
David Rodríguez Fragoso A01748760
Erick Hernández Silva A01750170
Israel Sánchez Miranda A01378705
Renata Monserrat de Luna Flores A01750484
Roberto Valdez  Jasso A01746863

10/11/2021
"""

#Librerías a usar
from mesa.visualization.modules import CanvasGrid
from mesa.visualization.modules import ChartModule
from LimpiadorModel import *
from mesa.visualization.ModularVisualization import ModularServer

def agentPortrayal(agent):
    """
    Función que define como se visualizarán los agentes en pantalla
    Parámetros: 
    agent - agente(s) que se visualizarán
    Retorno:
    portrayal - diccionario con las especificaciones de como se visualizarán los agentes
    """
    portrayal = {
        "Filled": "true",
    }
    if(type(agent) is AgenteLimpiador):
        portrayal["Shape"] = "circle"
        portrayal["Color"] = "red"
        portrayal["r"] = 0.5
        portrayal["Layer"] = 1
    else:
        portrayal["Shape"] = "rect"
        portrayal["Color"] = "green"
        portrayal["w"] = 1
        portrayal["h"] = 1
        portrayal["Layer"] = 0
    return portrayal

grid = CanvasGrid(agentPortrayal, 50, 50, 500, 500)  #Se crea el grid con las dimensiones especificadas
#Se crean las gráficas correspondientes a lo recolectado por el Datacollector
movimientos = ChartModule(
    [{
        "Label": "Movimientos",
        "Color": "Black"
    }],
    data_collector_name = 'datacollector'
)
celdasLimpias = ChartModule(
    [{
        "Label": "% Celdas Limpias",
        "Color": "Blue"
    }],
    data_collector_name = 'datacollector'
)
tiempo = ChartModule(
    [{
        "Label": "Tiempo",
        "Color": "Green"
    }],
    data_collector_name = 'datacollector'
)
#Se crea el servidor
server = ModularServer(
    LimpiadorModel, 
    [grid, tiempo, celdasLimpias, movimientos],
    "Modelo de robots limpiadores",
    {"N": 150, "width": 50, "height": 50, "percent": 70, "time": 450} 
)

#Se lanza el servidor
server.port = 8082
server.launch()
