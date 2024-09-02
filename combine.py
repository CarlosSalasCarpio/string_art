from itertools import combinations
from border import border_pixels
from find import draw_line
import numpy as np

def combine_border_and_find(image_size):
    """
    Combina las funciones de border_pixels y draw_line.
    Para un tamaño de imagen dado, determina los píxeles del borde y
    luego genera una matriz donde cada fila representa el vector resultante 
    de draw_line entre todos los pares de píxeles del borde.

    Args:
        image_size (int): Tamaño de la imagen (imagen de image_size x image_size).

    Returns:
        np.ndarray: Matriz donde cada fila es un vector binario que indica si
                    la línea entre dos píxeles del borde pasa por cada píxel de la imagen.
    """
    # Get border coordinates
    border_coords = border_pixels(image_size)

    # Generate all combinations of pairs
    coord_pairs = list(combinations(border_coords, 2))

    # Create a list to store the resulting vectors
    result_vectors = []

    # Loop over each pair and use draw_line
    for coord1, coord2 in coord_pairs:
        _, vector = draw_line(image_size, coord1, coord2)
        result_vectors.append(vector)

    # Convert to a NumPy array
    result_matrix = np.array(result_vectors)

    return result_matrix

# Example usage
matrix = combine_border_and_find(3)
#print(matrix)
