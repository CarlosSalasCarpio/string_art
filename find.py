import cv2
import numpy as np
from PIL import Image
import itertools
import matplotlib.pyplot as plt

def draw_line(image_size, coord1, coord2):
    """
    Dibuja una línea entre dos puntos en una imagen y devuelve la lista de puntos por los que pasa la línea, 
    así como dos vectores que indican si la línea pasa por each píxel de la imagen y si el píxel es uno de los extremos.

    Args:
        image_size (int): Tamaño de la imagen (imagen de image_size x image_size).
        coord1 (tuple): Coordenada del primer punto como (x1, y1).
        coord2 (tuple): Coordenada del segundo punto como (x2, y2).

    Returns:
        tuple: Una tupla que contiene:
            - points (list): Lista de puntos (x, y) por los que pasa la línea.
            - vector (list): Vector binario que indica si la línea pasa por each píxel de la imagen.
            - borders (list): Vector binario que indica si el píxel es uno de los extremos de la línea.
    """
    def bresenham(x1, y1, x2, y2):
        """Bresenham's Line Algorithm."""
        points = []
        dx = abs(x2 - x1)
        dy = abs(y2 - y1)
        sx = 1 if x1 < x2 else -1
        sy = 1 if y1 < y2 else -1
        err = dx - dy

        while True:
            points.append((x1, y1))
            if x1 == x2 and y1 == y2:
                break
            e2 = err * 2
            if e2 > -dy:
                err -= dy
                x1 += sx
            if e2 < dx:
                err += dx
                y1 += sy

        return points

    # Get all the points using Bresenham's algorithm
    points = bresenham(coord1[0], coord1[1], coord2[0], coord2[1])

    # Create the vector and borders
    vector = [0] * (image_size * image_size)
    borders = [0] * (image_size * image_size)

    for x, y in points:
        index = y * image_size + x
        vector[index] = 1 * 0.3

    # Mark the borders (endpoints)
    borders[points[0][1] * image_size + points[0][0]] = 1
    borders[points[-1][1] * image_size + points[-1][0]] = 1

    # Display vector
    #plt.imshow(np.reshape(vector, (image_size, image_size)), cmap='Greys')
    #plt.title("Vector")
    #plt.axis("off")
    #plt.show()

    # Display borders
    #plt.imshow(np.reshape(borders, (image_size, image_size)), cmap='Greys')
    #plt.title("Borders")
    #plt.axis("off")
    #plt.show()

    return points, vector, borders