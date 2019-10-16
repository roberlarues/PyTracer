from engine import renderer
import numpy.matlib 
import numpy as np 
from . import camera, sphere, lights, material

MAX_DISTANCE = 9999999999
BACK_COLOR = (0, 0, 0)

class Scene:
    """Representa una escena y los objetos que contiene
    
    Atributos
    ---------
        _camera - cámara
        lights - conjunto de luces
        objects - conjunto de objetos
        image - imagen sobre la que se va a renderizar"""
    _camera = camera.Camera((0, 0, 0))
    lights = []
    objects = []
    
    def __init__(self, image):
        self.load_scene1()
        self._camera.image = image
            
    def traceRay(self, ray):
        """Traza un rayo a través de la escena y devuelve el color del objeto
        con el que impacta
        
        Parámetros
        ----------
            ray - rayo a trazar
            
        Devuelve
        --------
            Color del objeto en el punto de intersección con el rayo. Si no 
            impacta con ningún objeto, devuelve el color base.
        """
        color = BACK_COLOR
        nearest_obj = None
        nearest_obj_distance = MAX_DISTANCE
        for obj in self.objects:
            intersection_distance = obj.get_intersection_distance(ray)
            if intersection_distance >= 0 and intersection_distance < nearest_obj_distance:
                nearest_obj = obj
                nearest_obj_distance = intersection_distance
        
        if nearest_obj != None:
            intersection = ray.position + np.multiply(ray.direction, nearest_obj_distance)
            n = nearest_obj.getNormalAtPoint(intersection)
            color = renderer.shade_intersection(n, nearest_obj.material, intersection, ray, self)
            
        return color
        
    def load_scene1(self):
        """Carga una escena por defecto
        
        Devuelve
        --------
            Escena tipo cornell-box: 4 paredes, suelo y techo. Una esfera 
            especular en el centro, una esfera espejo en una esquina y una
            luz puntual"""
        diffuse_white = material.Material()
        diffuse_red = material.Material(color=(255,0,0))
        diffuse_green = material.Material(color=(0,255,0))
        specular_blue = material.Material(color=(0,0,255), k_s=0.8, alpha = 20)
        mirror = material.Material(mirror = True)
        
        self._camera = camera.Camera(position=(-200.0, 0.0, 0.0), focal_length=200.0)
        
        self.objects.append(sphere.Sphere(position = (0.0, -3150.0, 0.0), radius = 3000.0, material = diffuse_red)) # izd
        self.objects.append(sphere.Sphere(position = (0.0, 3150.0, 0.0), radius = 3000.0, material = diffuse_green)) # rgt
        self.objects.append(sphere.Sphere(position = (0.0, 0.0, 3100.0), radius = 3000.0, material = diffuse_white)) # bot
        self.objects.append(sphere.Sphere(position = (0.0, 0.0, -3100.0), radius = 3000.0, material = diffuse_white)) # top
        self.objects.append(sphere.Sphere(position = (3100.0, 0.0, 0.0), radius = 3000.0, material = diffuse_white)) # front
        self.objects.append(sphere.Sphere(position = (-3300.0, 0.0, 0.0), radius = 3000.0, material = diffuse_white)) # back
        
        self.objects.append(sphere.Sphere(position = (0.0, 0.0, 60.0), radius = 40.0, material = specular_blue)) # center
        self.objects.append(sphere.Sphere(position = (70.0, 120.0, 70.0), radius = 30.0, material = mirror)) # center
        
        
        self.lights.append(lights.SpotLight(position = (-60.0, 60.0, -80.0), intensity=10000))
        
    # Getters
        
    def getCamera(self):
        return self._camera
        
    def getObjects(self):
        return self.objects
        