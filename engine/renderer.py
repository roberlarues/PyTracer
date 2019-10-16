import sys
import numpy as np 
import numpy.matlib 
import random
import psutil
import gc
from functools import partial
from engine.models import rays

SAMPLES_PER_PIXEL = 1
    
def shade_intersection(n, material, intersection_point, ray, scene):
    """Calcula el color que se mostrará en el punto de intersección de un rayo con un objeto
    
    Parámetros
    ----------
        n - vector normal del objeto en el punto de intersección
        material - material del objeto
        intersection_point - coordenadas del punto de intersección
        ray - rayo que conforma la intersección
        scene - escena a renderizar
        
    Devuelve
    --------
        color que se visualiza en la intersección desde el origen del rayo"""
    v = np.subtract(intersection_point, scene.getCamera().position)
    v = v / np.linalg.norm(v)
     
    if material.mirror == False:
        # Luz directa + luz indirecta
        color = _phong(material, scene, intersection_point, n, v) + _trace_path(intersection_point, ray, scene, n)
    else:
        r = np.subtract(np.multiply(n, -2.0 * np.dot(v, n)), v)
        r = r / np.linalg.norm(r)
        reflection_ray = rays.Ray(intersection_point + r, r, from_camera=False)
        color = scene.traceRay(reflection_ray)
    
    if color[0] > 255:
        color[0] = 255
    if color[1] > 255:
        color[1] = 255
    if color[2] > 255:
        color[2] = 255
    
    gc.collect()
    return color
        
def _phong(material, scene, intersection_point, n, v):
    """Calcula la luz directa en un punto utilizando la BRDF de _phong
    
    Parámetros
    ----------
        material - material del objeto
        scene - escena a renderizar
        intersection_point - coordenadas del punto de intersección
        ray - rayo que conforma la intersección
        n - vector normal del objeto en el punto de intersección
        v - vector que apunta desde la intersección al punto desde el que se está visualizando
        
    Devuelve
    --------
        Color visible desde el punto de vista en el punto de la intersección gracias a la luz directa"""
        
    intensity = np.array((material.k_a, 0, 0))
    for light in scene.lights:
        ol = np.subtract(light.position, intersection_point)
        ol_module = np.linalg.norm(ol)
        l = ol / ol_module
        
        is_shadow = False
        light_ray = rays.Ray(intersection_point, l, from_camera=False)
        for obj in scene.objects:
            intersection_distance = obj.get_intersection_distance(light_ray)
            if intersection_distance > 0.0 and intersection_distance < ol_module:
                is_shadow = True
                break
        
        if is_shadow == False:
            light_intensity = light.intensity / (ol_module ** 2)
            r = np.subtract(np.multiply(n, 2.0 * np.dot(l, n)), l)
            ln = np.dot(l, n)
            diff = ln * material.k_d
            spec = 0
            if (ln > 0):
                spec = (abs(np.dot(r, v)) ** material.alpha) * material.k_s
            intensity += numpy.array((0, diff * light_intensity, spec * light_intensity))
    
    color = numpy.array(np.multiply(intensity[0] + intensity[1], material.color)) + numpy.array(np.multiply(intensity[2], (255, 255, 255)))
    return color

def _trace_path_ray(intersection_point, ray, scene, n):
    """Traca un rayo aleatorio para el cálculo de path-tracing
    
    Parámetros
    ----------
        intersection_point - coordenadas del punto de intersección
        ray - rayo que conforma la intersección
        scene - escena a renderizar
        n - vector normal del objeto en el punto de intersección
        
    Devuelve
    --------
        Color que se obtiene con el rayo aleatorio trazado, ponderado con el coseno con la normal"""
    r_vec, cos_vec = _get_random_vector_in_hemisphere(n)
    ray_path = rays.Ray(intersection_point, r_vec, from_camera=False, max_indirect_bounces=ray.max_indirect_bounces-1)
    return  np.multiply(scene.traceRay(ray_path), 2 * cos_vec)
    
def _trace_path(intersection_point, ray, scene, n):
    """Calcula la luz indirecta mediante el algoritmo de path-tracing
    
    Parámetros
    ----------
        intersection_point - coordenadas del punto de intersección
        ray - rayo que conforma la intersección
        scene - escena a renderizar
        n - vector normal del objeto en el punto de intersección
        
    Devuelve
    --------
        Color que se obtiene con el rayo aleatorio trazado, ponderado con el coseno con la normal"""
    color = (0, 0, 0)
    if ray.max_indirect_bounces==0:
        return color
        
    for i in range(SAMPLES_PER_PIXEL):
        color = color + _trace_path_ray(intersection_point, ray, scene, n)
    color = np.array(color) / SAMPLES_PER_PIXEL
    
    return color
    
def _get_random_vector_in_hemisphere(n):
    """Calcula un vector aleatorio dentro de una semiesfera
    
    Parámetros
    ----------
        n - vector que apunta al cénit de la semiesfera
        
    Devuelve
    --------
        random_vector - vector unitario aleatorio dentro de la semiesfera
        vector_cos - coseno del vector devuelto con n"""
    random_vector = np.array((random.random() - 0.5, random.random() - 0.5, random.random() - 0.5))
    random_vector = random_vector / np.linalg.norm(random_vector)
    vector_cos = np.dot(n, random_vector)
    if vector_cos < 0:
        random_vector = np.multiply(random_vector , -1)
        vector_cos = -vector_cos
    
    return random_vector, vector_cos