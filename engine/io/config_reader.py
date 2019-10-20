import json

conf = None

def read_conf_file(file):
    """Carga la configuración desde un fichero
    
    Parámetros
    ----------
        file - fichero de entrada"""
    global conf
    with open(file) as json_file:
        conf = json.load(json_file)
        json_file.close()
    
def read_file(file):
    """Carga los datos de un fichero
    
    Parámetros
    ----------
        file - fichero de entrada
    
    Devuelve
    ----------
        estructura de datos con el contenido del fichero"""
    with open(file) as json_file:
        f = json.load(json_file)
        json_file.close()
        return f
    