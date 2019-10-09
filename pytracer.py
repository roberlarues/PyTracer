import engine
import ppm_writer
from models import image_model, scene

if __name__ == '__main__':
    # Inicializa la imagen de salida y la escena que se va a renderizar
    # y ejecuta el motor de renderizado
    image = image_model.ImageModel(640, 480)
    scene = scene.Scene(image)
    engine.start(image, scene)
    ppm_writer.write_image_model(image)
