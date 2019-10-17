#!/usr/bin/python

import sys
from engine import engine
from engine.io import ppm_writer, config_reader
from engine.models import image_model, scene

if __name__ == '__main__':
    config_reader.read_conf_file("config.json")
    
    # Validación de parámetros
    if len(sys.argv) == 1:
        print("\n Usage:\n    >pytracer.py [scene].pyrt")
        quit()
        
    file_scene = sys.argv[1]

    # Inicializa la imagen de salida y la escena que se va a renderizar
    # y ejecuta el motor de renderizado
    image_conf = config_reader.conf["image"]
    image = image_model.ImageModel(image_conf["width"], image_conf["height"])
    scene = scene.Scene(file_scene, image)
    engine.start(image, scene)
    ppm_writer.write_image_model(image)
