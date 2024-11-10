import gradio as gr
import requests
from io import BytesIO
from zipfile import ZipFile
from PIL import Image
import tempfile
import os

API_URL = "http://127.0.0.1:5001/process-image"

def process_image(image, size):
    """
    Sends the image and size to the Flask API, receives the processed image and CSV.
    """
    if image is None:
        return None, None

    try:
        # Convert the image to bytes for the POST request
        image_bytes = BytesIO()
        image.save(image_bytes, format='PNG')
        image_bytes.seek(0)

        files = {'image': image_bytes}
        data = {'size': size}

        # Send request to the Flask API
        response = requests.post(API_URL, files=files, data=data)
        
        if response.status_code != 200:
            print(f"Error: Received status code {response.status_code}")
            print(f"Response content: {response.text}")
            return "Error processing the image", None

        # Unzip the response
        zip_buffer = BytesIO(response.content)
        with ZipFile(zip_buffer, 'r') as zip_file:
            processed_image_data = zip_file.read('processed_image.png')
            coordinates_data = zip_file.read('coordinates.csv')

        # Load the processed image
        processed_image = Image.open(BytesIO(processed_image_data))

        # Save the CSV data to a temporary file
        temp_dir = tempfile.gettempdir()
        csv_path = os.path.join(temp_dir, "coordinates.csv")
        with open(csv_path, 'wb') as csv_file:
            csv_file.write(coordinates_data)

        return processed_image, csv_path

    except Exception as e:
        print(f"Exception occurred: {e}")
        return "Error processing the image", None

# Create the Gradio interface
def gradio_ui():
    interface = gr.Interface(
        fn=process_image,
        inputs=[
            gr.Image(type="pil", label="Upload Image"),
            gr.Slider(minimum=3, maximum=90, step=1, value=20, label="Image Size")
        ],
        outputs=[
            gr.Image(type="pil", label="Processed Image"),
            gr.File(label="Download Coordinates CSV")
        ],
        title="String Art Image Processing",
        description="Upload an image, adjust the size, and download the coordinates for string art.",
        allow_flagging="never",
        live=False
    )
    return interface

if __name__ == "__main__":
    ui = gradio_ui()
    ui.launch()