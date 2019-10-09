import numpy as np 
import numpy.matlib 
from . import rays

class Camera:
    """Representa una cámara tipo pin-hole"""
    
    image = None
    
    def __init__(self, position, direction=(1,0,0), focal_length=100):
        self.position = position
        self.direction = direction
        self.focal_length = focal_length
        self._fpoint = self.position + np.multiply(self.direction, self.focal_length)
        
            
    def getPixelRay(self, row, col):
        """Calcula el rayo que se trazará sobre un píxel
        
        Parámetros
        ----------
            row - fila del píxel
            col - columna del píxel
        
        Devuelve
        --------
            El rayo a trazar sobre el píxel"""
        direction = self._get_cam_to_pixel_vector(row, col)
        direction = direction / np.linalg.norm(direction)
        return rays.Ray(self.position, direction, from_camera=True)
        
    def _get_cam_to_pixel_vector(self, row, col):
        """Devuelve un vector desde la posición de la cámara hasta un píxel
        
        Parámetros
        ----------
            row - fila del píxel
            col - columna del píxel
        
        Devuelve
        --------
            Vector que apunta hacia el píxel"""
        pixel_pos = self._fpoint + np.array((0, col - self.image.get_w() / 2, row - self.image.get_h() / 2))
        return np.subtract(pixel_pos, self.position)