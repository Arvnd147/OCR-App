from flask import Flask, render_template, request
from PIL import Image
import pytesseract

app = Flask(__name__)

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload',methods=['POST'])
def upload():
    if 'file' not in request.files:
        return "No file Part"
    
    file = request.files['file']
    if file.filename == '':
        return "No selected file"
    
    img = Image.open(file)
    text = pytesseract.image_to_string(img, lang='eng+tam')
    
    return render_template('result.html', text=text)

if __name__ == '__main__':
    app.run(debug=True)