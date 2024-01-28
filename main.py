from flask import Flask, request, jsonify
from flask_cors import CORS
from pdf2image import convert_from_bytes
import pytesseract

app = Flask(__name__)
CORS(app)

@app.route('/extract_text', methods=['POST'])
def extract_text():
    if 'image' not in request.files:
        return jsonify({'error': 'No image or PDF file provided'}), 400

    file = request.files['image']
    print(file)
    file_extension = file.filename.rsplit('.', 1)[1].lower()

    if file_extension == 'pdf':
        try:
            images = convert_from_bytes(file.read())
            extracted_text = ''
            for image in images:
                text = pytesseract.image_to_string(image)
                extracted_text += text + '\n'
            return jsonify({'text': extracted_text})
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    elif file_extension in {'png', 'jpg', 'jpeg', 'gif'}:
        try:
            text = pytesseract.image_to_string(Image.open(file))
            return jsonify({'text': text})
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    else:
        return jsonify({'error': 'Unsupported file format'}), 400

if __name__ == '__main__':
    from waitress import serve
    serve(app, port=8080)
