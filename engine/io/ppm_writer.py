
    
def write_image_model(image_model, file_name="output.ppm"):
    """Guarda una imagen en un fichero con el formato PPM
    
    Parámetros
    ----------
        image_model - imagen a guardar"""
    f = open(file_name, "w")
    f.write("P3\n")
    f.write("# Renderizado con PyTracer\n")
    f.write(str(image_model.getW()) + " " + str(image_model.getH()) + "\n")
    f.write("255\n")
    img = image_model.getImage()
    h = image_model.getH()
    w = image_model.getW()
    for row in range(0, h):
        for col in range(0, w):
            color = img[row][col]
            r = 0
            g = 0
            b = 0
            if color[0] > 0:
                r = min(color[0].astype(int), 255)
            if color[1] > 0:
                g = min(color[1].astype(int), 255)
            if color[2] > 0:
                b = min(color[2].astype(int), 255)
            f.write(str(r) + " " + str(g) + " " + str(b) + "   ")
        f.write("\n")
    f.close()
