from engine import engine
from engine.io import ppm_writer, config_reader
from engine.models import image_model, scene

if __name__ == '__main__':
    config_reader.read_file("config.json")

    # Inicializa la imagen de salida y la escena que se va a renderizar
    # y ejecuta el motor de renderizado
    image_conf = config_reader.conf["image"]
    image = image_model.ImageModel(image_conf["width"], image_conf["height"])
    scene = scene.Scene(image)
    engine.start(image, scene)
    ppm_writer.write_image_model(image)
