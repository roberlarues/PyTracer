
class Material:
    """Representa un material
    
    Atributos
    ---------
        color - albedo del material
        k_s - componente especular
        k_d - componente difuso
        k_a - componente ambiente
        apha - grado de reflectancia
        mirror - si es tipo espejo"""
    
    def __init__(self, color = (255, 255, 255), k_s = 0.2, k_d = 0.7, k_a = 0.1, alpha = 2, mirror = False):
        self.color = color
        self.k_s = k_s
        self.k_d = k_d
        self.k_a = k_a
        self.alpha = alpha
        self.mirror = mirror