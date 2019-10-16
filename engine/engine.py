import time

def start(image, scene):
    """Ejecuta el renderizado de una escena sobre una imagen
    
    Parámetros
    ----------
        image - imagen de salida
        scene - escena a renderizar"""

    current_milli_time = lambda: int(round(time.time() * 1000))

    start_time = current_milli_time()
    
    print("Renderizando... [", end="",flush=True)
    _render(scene, image, 0, image.get_h())
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
    ray = scene.getCamera().getPixelRay(row, col)
    return scene.traceRay(ray)
    