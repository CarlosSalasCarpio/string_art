import numpy as np
import matplotlib.pyplot as plt

def plot_lines(matrix, line_thickness=0.08, line_color='black'):
    # Convert the input to a proper 2D array
    matrix = np.atleast_2d(matrix)
    
    # Determine the size of the grid
    num_vectors = matrix.shape[0]
    vector_length = matrix.shape[1]
    size = int(np.sqrt(vector_length))
    if size * size != vector_length:
        raise ValueError("Invalid vector length for a square grid.")
    
    # Plot the grid
    plt.figure()
    plt.imshow(np.zeros((size, size)), cmap='Greys', extent=[0, size, 0, size])
    plt.xticks(np.arange(size + 1))
    plt.yticks(np.arange(size + 1))
    plt.gca().grid(False)  # Turn off grid lines
    
    for i in range(num_vectors):
        vector = matrix[i]
        positions = np.where(vector == 1)[0]
        if len(positions) != 2:
            raise ValueError("Each vector should have exactly two 1s.")
        # Determine the coordinates of the 1s
        x1, y1 = divmod(positions[0], size)
        x2, y2 = divmod(positions[1], size)
        plt.plot([y1 + 0.5, y2 + 0.5], [size - x1 - 0.5, size - x2 - 0.5], color=line_color, linewidth=line_thickness)
    
    plt.show()
