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

#Librerías ausar
from mesa.visualization.modules import CanvasGrid
from mesa.visualization.modules import ChartModule
from LimpiadorModel import *
from mesa.visualization.ModularVisualization import ModularServer

def agent_portrayal(agent):
    """Función que define como se visualizarán los agentes en pantalla"""
    portrayal = {
        "Shape": "circle",
        "Filled": "true",
    }
    if(agent.state == 0):
        portrayal["Color"] = "red"
        portrayal["r"] = 0.5
        portrayal["Layer"] = 1
    else:
        portrayal["Color"] = "green"
        portrayal["r"] = 1
        portrayal["Layer"] = 0
    return portrayal

grid = CanvasGrid(agent_portrayal, 10, 10, 500, 500)  #Se crea el grid con las dimensiones especificadas
#Se crean las gráficas correspondientes a lo recolectado por el Datacollector
movimientos = ChartModule(
    [{
        "Label": "Movimientos",
        "Color": "Black"
    }],
    data_collector_name = 'datacollector'
)
celdas_limpias = ChartModule(
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
    [grid, tiempo, celdas_limpias, movimientos],
    "Modelo de robots limpiadores",
    {"N": 15, "width": 10, "height": 10, "percent": 70, "time": 50} 
)

#Se lanza el servidor
server.port = 8081
server.launch()
