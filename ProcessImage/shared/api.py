from flask import Flask, request, jsonify, send_file
from PIL import Image
from io import BytesIO
from zipfile import ZipFile
from pinv import solve_pinv_for_image

app = Flask(__name__)

@app.route('/process-image', methods=['POST'])
def process_image():
    try:
        if 'image' not in request.files:
            return jsonify({'error': 'No image provided'}), 400

        image_file = request.files['image']
        size = int(request.form.get('size', 20))
        
        image = Image.open(image_file)
        image_buffer, csv_buffer = solve_pinv_for_image(image, size)

        # Create a ZIP file containing the image and the CSV
        zip_buffer = BytesIO()
        with ZipFile(zip_buffer, 'w') as zip_file:
            zip_file.writestr('processed_image.png', image_buffer.getvalue())
            zip_file.writestr('coordinates.csv', csv_buffer.getvalue())
        zip_buffer.seek(0)

        return send_file(zip_buffer, mimetype='application/zip', download_name='results.zip')
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)