import json

conf = None

def read_file(file):
    """Carga la configuración desde un fichero
    
    Parámetros
    ----------
        file - fichero de entrada"""
    global conf
    with open(file) as json_file:
        conf = json.load(json_file)
    