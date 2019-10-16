
class SpotLight:
    """Representa un punto de luz
    
    Atributos
    ---------
        position - posición de la luz
        color - color de la luz
        intensity - intensidad de la luz"""
    
    def __init__(self, position = (0, 0, 0), color = (0, 0, 255), intensity=5000):
        self.position = position
        self.color = color
        self.intensity = intensity