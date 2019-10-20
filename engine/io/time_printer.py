
    
def save_time(image_to_write, file_name="output.ppm"):
    """Guarda una imagen en un fichero con el formato PPM
    
    Parámetros
    ----------
        image_to_write - imagen a guardar"""
    f = open(file_name, "w")
    f.write("P3\n")
    f.write("# Renderizado con PyTracer\n")
    f.write(str(image_to_write.get_w()) + " " + str(image_to_write.get_h()) + "\n")
    f.write("255\n")
    img = image_to_write.get_image()
    h = image_to_write.get_h()
    w = image_to_write.get_w()
    for row in range(0, h):
        for col in range(0, w):
            color = img[row][col]
            r = 0
            g = 0
            b = 0
            if color[0] > 0:
                r = min(int(color[0]), 255)
            if color[1] > 0:
                g = min(int(color[1]), 255)
            if color[2] > 0:
                b = min(int(color[2]), 255)
            f.write(str(r) + " " + str(g) + " " + str(b) + "   ")
        f.write("\n")
    f.close()
