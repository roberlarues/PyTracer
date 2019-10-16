import math
import numpy as np
from . import material

class Sphere:
    """Representa un objeto de tipo esfera
    
    Atributos
    ---------
        position - centro de la esfera
        radius - radio de la esdera
        material - material
        _camera_calc_oc - almacena el vector del centro a la cámara (optimización)
        _camera_calc_pt2 - almacena una parte constante en el cálculo de la intersección"""
                          
    
    _camera_calc_oc = []
    _camera_calc_pt2 = None
    
    def __init__(self, position = (0, 0, 0), radius = 50, material = material.Material()):
        self.position = position
        self.radius = radius
        self.material = material
        
    def getNormalAtPoint(self, point):
        """Calcula el vector normal de la esfera en un punto
        Parámetros
        ----------
            point - punto en el que calcular la normal
          
        Devuelve
        --------
            Vector normal unitario."""
        n = np.subtract(point, self.position)
        return n / np.linalg.norm(n)
            
    def intersects(self, ray):
        """Comprueba si el rayo interecta con el objeto
        
        Parámetros
        ----------
            ray - rayo con el que realizar la comprobación
            
        Devuelve
        --------
            Si existe una o varias intersecciones."""
        if ray.from_camera:
            if len(self._camera_calc_oc) == 0:
                self._camera_calc_oc = np.subtract(ray.position, self.position)
                self._camera_calc_pt2 = np.linalg.norm(self._camera_calc_oc) ** 2 - self.radius ** 2
            oc = self._camera_calc_oc
            pt2 = self._camera_calc_pt2
        else:
            oc = np.subtract(ray.position, self.position)
            pt2 = np.linalg.norm(oc) ** 2 - self.radius ** 2
        pt1 = (np.dot(ray.direction, oc) ** 2)
        return pt1 - pt2 > 0
        
        
    def get_intersection_distance(self, ray):
        """Dado un rayo, si intersecta con el objeto, devuelve la distancia
        desde el origen del rayo hasta el punto de intersección más cercano.
        
        Parámetros
        ----------
            ray - rayo con el que realizar la comprobación
            
        Devuelve
        --------
            Si el rayo intersecta con el objeto, devuelve la distancia
            desde el origen del rayo hasta el punto de intersección más
            cercano. Si no intersecta, devuelve -1."""
        if ray.from_camera:
            if len(self._camera_calc_oc) == 0:
                self._camera_calc_oc = np.subtract(ray.position, self.position)
                self._camera_calc_pt2 = np.linalg.norm(self._camera_calc_oc) ** 2.0 - self.radius ** 2.0
            oc = self._camera_calc_oc
            pt2 = self._camera_calc_pt2
        else:
            oc = np.subtract(ray.position, self.position)
            pt2 = np.linalg.norm(oc) ** 2.0 - self.radius ** 2.0
        loc = np.dot(ray.direction, oc)
        pt1 = loc ** 2.0
        in_sqrt = pt1 - pt2
        if in_sqrt >= 0.0:
            sqrt_res = math.sqrt(in_sqrt)
            sol1 = -loc - sqrt_res
            sol2 = -loc + sqrt_res
            return sol1 if sol1 <= sol2 else sol2
        else:
            return -1