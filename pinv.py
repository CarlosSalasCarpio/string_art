import numpy as np
import matplotlib.pyplot as plt
from itertools import combinations
import cv2
from PIL import Image
from border import border_pixels
from find import draw_line
from image import load_and_process_image, image_to_vector
from graph import plot_lines

def solve_pinv_for_image(image_path, image_size):
    """
    Integra las funciones de border.py, find.py e image.py para obtener A y b y resolver x = pinv(A) * b
    usando un algoritmo greedy para forzar x a 0 o 1.

    Args:
        image_path (str): Ruta de la imagen.
        image_size (int): Tamaño de la imagen (imagen de image_size x image_size).

    Returns:
        tuple: Tupla que contiene:
            - np.ndarray: Matriz A.
            - np.ndarray: Vector b.
            - np.ndarray: Vector x.
            - np.ndarray: Vector borders.
    """
    print("Iniciando proceso con la imagen:", image_path)
    
    border_coords = border_pixels(image_size)
    coord_pairs = list(combinations(border_coords, 2))
    print("Píxeles de borde calculados.")

    A = []
    borders_list = []

    print("Calculando líneas entre pares de píxeles de borde...")
    total_pairs = len(coord_pairs)
    print(f"Total de pares de coordenadas a procesar: {total_pairs}")

    for index, (coord1, coord2) in enumerate(coord_pairs):
        _, vector, borders = draw_line(image_size, coord1, coord2)
        A.append(vector)
        borders_list.append(borders)
        if (index + 1) % 1000 == 0:
            print(f"Procesados {index + 1} pares de coordenadas de {total_pairs}")

    print("Líneas calculadas.")

    A = np.array(A)
    borders_array = np.array(borders_list)
    A = A.T
    borders_array = borders_array.T

    print("Cargando y procesando la imagen...")
    processed_image = load_and_process_image(image_path, image_size)
    b = image_to_vector(processed_image)
    print("Imagen procesada.")

    print("Calculando la solución del sistema...")
    A_pinv = np.linalg.pinv(A)
    x = np.dot(A_pinv, b)

    print("Optimizando la solución con un algoritmo greedy...")
    x_greedy = np.zeros_like(x)
    residual = b - np.dot(A, x_greedy)
    indices = np.argsort(-np.abs(x))

    for i in indices:
        new_residual = residual - A[:, i] * x[i]
        if np.linalg.norm(new_residual) < np.linalg.norm(residual):
            residual = new_residual
            x_greedy[i] = 1 if x[i] > 0 else -1
    x = x_greedy
    print("Optimización completada.")

    print("Filtrando la matriz...")
    C = borders_array.T[x == 1]
    print("Matriz filtrada.")

    # Guardar la matriz C
    np.save("matrix_C.npy", C)
    print("Matriz C guardada como 'matrix_C.npy'.")

    print('C', C)

    return C

# Ejemplo de uso
size = 90
image_path = "images/fedora_girl.jpg"

print("Empezando el proceso para la imagen.")
C = solve_pinv_for_image(image_path, size)

print("Dibujando líneas...")
plot_lines(C)
print("Proceso completado.")
