
class Ray:
    """Representa un rayo a trazar
    
    Atributos
    ---------
        position - origen del rayo
        direction - vector dirección del rayo
        from_camera - indica si proviene de la cámara
        max_direct_bounces - máximo de rebotes de luz directa (para reflejos)
        max_indirect_bounces - máximo de rebotes de luz indirecta"""
    
    def __init__(self, position, direction, from_camera, max_direct_bounces = 2, max_indirect_bounces = 1):
        self.position = position
        self.direction = direction
        self.from_camera = from_camera
        self.max_direct_bounces = max_direct_bounces
        self.max_indirect_bounces = max_indirect_bounces
        