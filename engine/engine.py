import time, math
from engine import renderer
from engine.io import config_reader, ppm_writer
from engine.models import image_model


current_milli_time = lambda: int(round(time.time() * 1000))
    
def start(image, scene):
    """Ejecuta el renderizado de una escena sobre una imagen
    
    Parámetros
    ----------
        image - imagen de salida
        scene - escena a renderizar"""

    renderer.configure(config_reader.conf["lighting"]["direct-bounces"], \
        config_reader.conf["lighting"]["indirect-bounces"], 
        config_reader.conf["lighting"]["indirect-samples"])

    start_time = current_milli_time()
    
    print("Renderizando... [", end="",flush=True)
    if not config_reader.conf["fast-mode"]:
        _render_stats(scene, image, 0, image.get_h())
    else:
        _fast_render(scene, image, 0, image.get_h())
        
    print("]")
    
    elapsed_time_ms = current_milli_time() - start_time
    elapsed_time_secs = elapsed_time_ms // 1000
    elapsed_time_ms   = elapsed_time_ms % 1000
    elapsed_time_mins = elapsed_time_secs // 60
    elapsed_time_secs = elapsed_time_secs % 60
    
    print("Tiempo de ejecución:", elapsed_time_mins, "min", elapsed_time_secs, "s", elapsed_time_ms, "ms")
           
           
def _render(scene, image, init, end):
    """Renderiza la escena para un rango de filas de píxels en la imagen de salida
    
    Parámetros
    ----------
        scene - escena a renderizar
        image - imagen de salida
        init - primera fila de pixels a renderizar
        end - última fila de pixels a renderizar"""
    for i in range(init, end):
        for j in range(0, image.get_w()):
            image.set_color(i, j, _calculate_pixel_color(scene, i, j))
        if i % (image.get_h() // 50) == 0:
            print("=", end="", flush=True)
           
def _render_stats(scene, image, init, end):
    """Renderiza la escena para un rango de filas de píxels en la imagen de salida
    
    Parámetros
    ----------
        scene - escena a renderizar
        image - imagen de salida
        init - primera fila de pixels a renderizar
        end - última fila de pixels a renderizar"""
    timesImg = image_model.ImageModel(image.get_w(), image.get_h())
    min_pixel_time = 9999999999
    max_pixel_time = 0
    f = open("time_list.data", "w")
    for i in range(init, end):
        for j in range(0, image.get_w()):
        
            start_time_pixel = current_milli_time()
            
            image.set_color(i, j, _calculate_pixel_color(scene, i, j))
            
            elapsed_time_pixel = current_milli_time() - start_time_pixel
            if elapsed_time_pixel < min_pixel_time:
                min_pixel_time = elapsed_time_pixel
            if elapsed_time_pixel > max_pixel_time:
                max_pixel_time = elapsed_time_pixel
            timesImg.set_color(i, j, elapsed_time_pixel)
        if i % (image.get_h() // 50) == 0:
            print("=", end="", flush=True)
            f.write(str(int(elapsed_time_pixel)) + ",\n")
    f.close()

    print("min:" + str(min_pixel_time))
    print("max: " + str(max_pixel_time))
    time_scaling = max_pixel_time - min_pixel_time
    time_scaling = math.log(time_scaling) / 255.0
    for i in range(init, end):
        for j in range(0, image.get_w()):
            r = 0
            rv = (timesImg.get_color(i, j) - min_pixel_time)
            if rv > 0:
                r = math.log(rv) / time_scaling
            g = 0
            b = 0
            v = [r, r, r]
            timesImg.set_color(i, j, v)
    ppm_writer.write_image_model(timesImg, file_name="pixel_time_map.ppm")
    
    
def _fast_render(scene, image, init, end):
    """Realiza un renderizado rápido, omitiendo los píxels impares
    
    Parámetros
    ----------
        scene - escena a renderizar
        image - imagen de salida
        init - primera fila de pixels a renderizar
        end - última fila de pixels a renderizar"""
    for i in range(init, end):
        for j in range(0, image.get_w()):
            if  (i + j) % 2:
                image.set_color(i, j, _calculate_pixel_color(scene, i, j))
        if i % (image.get_h() // 50) == 0:
            print("=", end="", flush=True)
        
        
def _calculate_pixel_color(scene, row, col):
    """Calcula el color que mostrará un píxel determinado
    
    Parámetros
    ----------
        scene - escena a renderizar
        row - fila del píxel
        col - columna del píxel"""
    ray = scene.get_camera().get_pixel_ray(row, col)
    return scene.traceRay(ray)
    