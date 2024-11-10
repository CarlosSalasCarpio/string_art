import azure.functions as func
from PIL import Image
from io import BytesIO
from zipfile import ZipFile
from .shared.pinv import solve_pinv_for_image
import json

def main(req: func.HttpRequest) -> func.HttpResponse:
    try:
        # Get the image file from the request
        image_file = req.files.get('image')
        if not image_file:
            return func.HttpResponse(
                json.dumps({'error': 'No image provided'}),
                status_code=400,
                mimetype='application/json'
            )

        # Read the image data
        image_data = image_file.read()

        # Get the 'size' parameter from form data
        size = int(req.form.get('size', 20))

        # Open the image and process it
        image = Image.open(BytesIO(image_data))
        image_buffer, csv_buffer = solve_pinv_for_image(image, size)

        # Create a ZIP file containing the processed image and CSV
        zip_buffer = BytesIO()
        with ZipFile(zip_buffer, 'w') as zip_file:
            zip_file.writestr('processed_image.png', image_buffer.getvalue())
            zip_file.writestr('coordinates.csv', csv_buffer.getvalue())
        zip_buffer.seek(0)

        # Return the ZIP file
        return func.HttpResponse(
            body=zip_buffer.getvalue(),
            status_code=200,
            headers={
                'Content-Type': 'application/zip',
                'Content-Disposition': 'attachment; filename="results.zip"'
            }
        )

    except Exception as e:
        print(f"Error processing request: {str(e)}")
        return func.HttpResponse(
            json.dumps({'error': str(e)}),
            status_code=500,
            mimetype='application/json'
        )