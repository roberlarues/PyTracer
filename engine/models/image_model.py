
BASE_COLOR = (0, 0, 0)

class ImageModel:
    """Representa una imagen a guardar
    
    Atributos
    ---------
        w - ancho de la imagen
        h - alto de la imagen
        _img - matriz de colores de la imagen"""
        
    
    def __init__(self, w=640, h=480):
        self._img = []
        self.create(w, h)
     
    def create(self, w, h):
        """Inicializa la imagen con el color base
        
        Parámetros
        ----------
            w - ancho de la imagen
            h - alto de la imagen"""
        self.w = w
        self.h = h
        for row in range(0, h):
            rowList = []
            for col in range(0, w):
                rowList.append(BASE_COLOR)
            self._img.append(rowList)
            
    def set_color(self, row, col, color):
        """Establece el color en un píxel de la imagen
        
        Parámetros
        ----------
            row - fila del píxel
            col - columna del píxel
            color - color del píxel"""
        self._img[row][col] = color
        
    def get_color(self, row, col):
        """Devuelve el color de un pixel de la imagen
        
        Parámetros
        ----------
            row - fila del píxel
            col - columna del píxel
            
        Devuelve
        --------
            Color del píxel indicado"""
        return self._img[row][col]
        
        
    # Getters
    
    def get_image(self):
        return self._img
        
    def get_h(self):
        return self.h
        
    def get_w(self):
        return self.w
    