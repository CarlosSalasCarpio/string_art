import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors

def plot_lines_from_file(filename, line_thickness=0.5, line_color='black'):
    # Load the matrix from a file
    matrix = np.load(filename)

    print('Matrix size:', matrix.shape)
    
    # Convert the input to a proper 2D array
    matrix = np.atleast_2d(matrix)
    
    # Determine the size of the grid
    num_vectors = matrix.shape[0]
    vector_length = matrix.shape[1]
    size = int(np.sqrt(vector_length))
    if size * size != vector_length:
        raise ValueError("Invalid vector length for a square grid.")
    
    # Create a vertical gradient background
    x = np.linspace(-1, 1, size)
    y = np.linspace(-1, 1, size)
    Y = np.tile(np.abs(x), (size, 1))  # Repeat the absolute value of x in rows
    gradient = np.clip(1 - Y, 0, 1)  # Normalize Y to 0-1 range for color intensity, center to edges
    background_cmap = mcolors.LinearSegmentedColormap.from_list('blue_white_gradient', [(0, 'blue'), (1, 'white')])
    
    # Plot the grid
    plt.figure(figsize=(8, 8))
    plt.imshow(gradient, cmap=background_cmap, extent=[0, size, 0, size], vmin=0, vmax=1)
    plt.axis('off')  # Hide the axes
    
    for i in range(num_vectors):
        vector = matrix[i]
        positions = np.where(vector == 1)[0]
        if len(positions) != 2:
            raise ValueError("Each vector should have exactly two 1s representing the line endpoints.")
        # Determine the coordinates of the 1s
        x1, y1 = divmod(positions[0], size)
        x2, y2 = divmod(positions[1], size)
        plt.plot([y1 + 0.5, y2 + 0.5], [size - x1 - 0.5, size - x2 - 0.5], color=line_color, linewidth=line_thickness)

    plt.show()

# Usage example
filename = 'matrix/fedoragirl-90-002.npy'  # Assumes the file is in the root directory
plot_lines_from_file(filename)
