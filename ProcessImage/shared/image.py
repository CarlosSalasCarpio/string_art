import numpy as np
from PIL import Image, ImageEnhance
import matplotlib.pyplot as plt

def load_and_process_image(image, image_size):
    """
    Carga y procesa la imagen para el análisis.

    Args:
        image (PIL.Image): Imagen cargada desde el usuario.
        image_size (int): Tamaño al cual ajustar la imagen.

    Returns:
        np.ndarray: Imagen procesada.
    """
    # Convertir la imagen a escala de grises si no lo está
    image = image.convert("L")
    
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
    """
    Convierte la imagen en un vector para el procesamiento.

    Args:
        image_array (np.ndarray): Matriz de la imagen procesada.

    Returns:
        np.ndarray: Vector de la imagen procesada.
    """
    # Invertir y normalizar la imagen
    normalized_image = 1 - (image_array / 255.0)
    
    # Convertir la imagen a un vector
    vector = normalized_image.flatten()

    # Mostrar la imagen procesada
    plt.imshow(image_array, cmap='gray')
    plt.show()

    return vector