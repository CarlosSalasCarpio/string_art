import cv2
import numpy as np
from PIL import Image, ImageEnhance
import matplotlib.pyplot as plt

def load_and_process_image(image_path, image_size):
    # Cargar la imagen usando PIL
    image = Image.open(image_path).convert("L")
    # Ajustar el contraste
    enhancer = ImageEnhance.Contrast(image)
    image = enhancer.enhance(2.0)  # Aumenta el contraste (puedes ajustar el valor)
    # Aplicar una curva para oscurecer más
    image = image.point(lambda p: p * 0.8 if p < 128 else p * 1.2)
    # Redimensionar la imagen a image_size x image_size píxeles
    image = image.resize((image_size, image_size), Image.LANCZOS)
    # Convertir la imagen a una matriz numpy
    image_array = np.array(image)
    return image_array

def image_to_vector(image_array):
    # Invertir y normalizar la imagen
    normalized_image = 1 - (image_array / 255.0)
    # Convertir la imagen a un vector
    vector = normalized_image.flatten()

    plt.imshow(image_array, cmap='gray')
    plt.show()

    return vector
