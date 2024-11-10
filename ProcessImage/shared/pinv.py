import matplotlib
matplotlib.use('Agg')  # Set the backend to non-interactive before importing pyplot

import numpy as np
import matplotlib.pyplot as plt
from itertools import combinations
from PIL import Image
from border import border_pixels
from find import draw_line
from image import load_and_process_image, image_to_vector
from graph import plot_lines
from io import BytesIO

def is_edge_line(x1, y1, x2, y2, image_size):
    if (x1 == 0 and x2 == 0) or (x1 == image_size - 1 and x2 == image_size - 1):
        return True
    if (y1 == 0 and y2 == 0) or (y1 == image_size - 1 and y2 == image_size - 1):
        return True
    return False

def distance(point1, point2):
    x1, y1 = point1
    x2, y2 = point2
    return np.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)

def solve_pinv_for_image(image, image_size):
    border_coords = border_pixels(image_size)
    coord_pairs = list(combinations(border_coords, 2))

    A = []
    borders_list = []
    for coord1, coord2 in coord_pairs:
        _, vector, borders = draw_line(image_size, coord1, coord2)
        A.append(vector)
        borders_list.append(borders)

    A = np.array(A).T
    borders_array = np.array(borders_list).T

    processed_image = load_and_process_image(image, image_size)
    b = image_to_vector(processed_image)

    A_pinv = np.linalg.pinv(A)
    x = np.dot(A_pinv, b)

    x_greedy = np.zeros_like(x)
    residual = b - np.dot(A, x_greedy)
    indices = np.argsort(-np.abs(x))

    for i in indices:
        new_residual = residual - A[:, i] * x[i]
        if np.linalg.norm(new_residual) < np.linalg.norm(residual):
            residual = new_residual
            x_greedy[i] = 1 if x[i] > 0 else -1

    x = x_greedy
    C = borders_array.T[x == 1]

    size = image_size
    coordinates = []
    for vector in C:
        positions = np.where(vector == 1)[0]
        if len(positions) == 2:
            x1, y1 = divmod(positions[0], size)
            x2, y2 = divmod(positions[1], size)
            if not is_edge_line(x1, y1, x2, y2, size):
                coordinates.append((x1, y1, x2, y2))

    # Save the coordinates to a CSV buffer
    csv_buffer = BytesIO()
    np.savetxt(csv_buffer, coordinates, delimiter=",", fmt='%d')
    csv_buffer.seek(0)

    # Generate the image
    plt.figure(figsize=(6, 6))
    plot_lines(C)
    plt.axis('off')
    image_buffer = BytesIO()
    plt.savefig(image_buffer, format='PNG', bbox_inches='tight', pad_inches=0)
    plt.close()
    image_buffer.seek(0)
    
    return image_buffer, csv_buffer