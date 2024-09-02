import cv2
import numpy as np
from PIL import Image
import itertools
import matplotlib.pyplot as plt

def border_pixels(image_size):
    """
    Devuelve una lista con las coordenadas de todos los píxeles del borde de una imagen de tamaño image_size x image_size,
    excluyendo esquinas repetidas.

    Args:
        image_size (int): Tamaño de la imagen (imagen de image_size x image_size).

    Returns:
        list: Lista de coordenadas (x, y) de los píxeles del borde.
    """
    # List of border pixels
    border_points = []

    # Top border (excluding corners)
    for x in range(1, image_size - 1):
        border_points.append((x, 0))

    # Bottom border (excluding corners)
    for x in range(1, image_size - 1):
        border_points.append((x, image_size - 1))

    # Left border (including corners)
    for y in range(image_size):
        border_points.append((0, y))

    # Right border (including corners)
    for y in range(image_size):
        border_points.append((image_size - 1, y))

    # Create an empty image
    image = np.zeros((image_size, image_size), dtype=np.uint8)

    # Draw the border pixels
    for x, y in border_points:
        image[y, x] = 255

    # Convert to PIL Image for display
    pil_image = Image.fromarray(image)

    # Show the image
    #plt.imshow(pil_image, cmap='gray')
    #plt.show()

    return border_points
