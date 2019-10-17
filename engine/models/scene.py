from engine import renderer
import numpy.matlib 
import numpy as np 
from . import camera, sphere, lights, material
from engine.io import config_reader

MAX_DISTANCE = 9999999999
BACK_COLOR = (0, 0, 0)

class Scene:
    """Representa una escena y los objetos que contiene
    
    Atributos
    ---------
        _camera - cámara
        lights - conjunto de luces
        objects - conjunto de objetos
        file_scene - archivo con los datos de la escena
        image - imagen sobre la que se va a renderizar"""
    lights = []
    objects = []
    
    def __init__(self, file_scene, image):
        _camera = camera.Camera((0, 0, 0))
        self.load_scene(file_scene)
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
            impacta con ningún objeto, devuelve el color base."""
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
        
    def load_scene(self, file):
        """Carga una escena desde un fichero
        
        Parámetros
        ----------
            file - archivo con los datos de la escena"""
        scene_data = config_reader.read_file(file)
        
        self._camera = camera.Camera(**scene_data["camera"])
            
        for l in scene_data["lights"]:
            if l["type"] == "spot":
                l.pop("type")
                self.lights.append(lights.SpotLight(**l))
                    
        m_dict = {}
        for m in scene_data["materials"]:
            id = m["id"]
            m.pop("id")
            m_dict[id] = material.Material(**m)
            
        for o in scene_data["objects"]:
            o["material"] = m_dict[o["material"]]
            self.objects.append(sphere.Sphere(**o))
            
    # Getters
        
    def get_camera(self):
        return self._camera
        
    def getObjects(self):
        return self.objects
        