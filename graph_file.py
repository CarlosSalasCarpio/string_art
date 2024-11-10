import numpy as np
import matplotlib.pyplot as plt
import gradio as gr
from PIL import Image

def plot_lines_from_csv(filename, line_thickness=0.1, line_color='black'):
    """
    Grafica líneas basadas en un archivo CSV que contiene pares de coordenadas.
    Args:
        filename (str): Ruta del archivo CSV que contiene las coordenadas.
        line_thickness (float): Grosor de las líneas a graficar.
        line_color (str): Color de las líneas.
    """
    # Cargar las coordenadas desde el archivo CSV
    coordinates = np.loadtxt(filename, delimiter=',', dtype=int)

    # Crear una figura de Matplotlib con fondo blanco
    plt.figure(figsize=(8, 8), facecolor='white')
    
    # Graficar las líneas
    for coord in coordinates:
        x1, y1, x2, y2 = coord
        plt.plot([y1, y2], [x1, x2], color=line_color, linewidth=line_thickness)
    
    plt.gca().invert_yaxis()  # Invertir el eje Y para que coincida con el formato de las imágenes
    plt.axis('off')  # Ocultar los ejes para una visualización más limpia

    # Guardar la imagen temporalmente en una ruta local
    output_image_path = 'output_string_art.png'
    plt.savefig(output_image_path, bbox_inches='tight', pad_inches=0)
    plt.close()

    # Cargar y devolver la imagen
    result_image = Image.open(output_image_path)
    return result_image

# Interfaz de Gradio
def plot_image_from_csv(file):
    return plot_lines_from_csv(file.name)

# Crear interfaz de Gradio
iface = gr.Interface(
    fn=plot_image_from_csv,
    inputs=gr.File(label="Subir archivo CSV con coordenadas"),
    outputs=gr.Image(type="pil"),
    title="Visualización de String Art",
    description="Sube un archivo CSV con pares de coordenadas para visualizar las líneas generadas.",
)

iface.launch()