import gradio as gr
import requests
from io import BytesIO
from zipfile import ZipFile
from PIL import Image
import tempfile
import os

API_URL = "http://localhost:7071/ProcessImage"

def process_image(image, size):
    """
    Sends the image and size to the Azure Function, receives the processed image and CSV.
    """
    if image is None:
        return None, None

    try:
        # Convert the image to bytes for the POST request
        image_bytes = BytesIO()
        image.save(image_bytes, format='PNG')
        image_bytes.seek(0)

        files = {'image': ('image.png', image_bytes, 'image/png')}
        data = {'size': str(size)}

        # Send request to the Azure Function
        response = requests.post(API_URL, files=files, data=data)
        
        if response.status_code != 200:
            print(f"Error: Received status code {response.status_code}")
            print(f"Response content: {response.text}")
            return None, None

        # Parse JSON errors if returned by the server
        if 'application/json' in response.headers.get('Content-Type', ''):
            error_message = response.json().get('error', 'Unknown error')
            print(f"Error from server: {error_message}")
            return None, None

        # Check if the response is a ZIP file
        if 'application/zip' in response.headers.get('Content-Type', ''):
            zip_buffer = BytesIO(response.content)
            
            # Extract the ZIP file content
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

        print("Error: Unexpected response format")
        return None, None

    except Exception as e:
        print(f"Exception occurred: {e}")
        return None, None

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
        live=False  # Removed flagging_dir
    )
    return interface

if __name__ == "__main__":
    ui = gradio_ui()
    ui.launch()