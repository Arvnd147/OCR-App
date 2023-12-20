from flask import Flask, render_template, request, jsonify
from PIL import Image
import pytesseract
import dlib
import face_recognition
import numpy as np

app = Flask(__name__)

# load dlib obj detectot
detector = dlib.get_frontal_face_detector()

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload',methods=['POST'])
def upload():
    if 'ocrFile' not in request.files or 'referenceFile' not in request.files:
        return "Both files are required"
    
    ocr_file = request.files['ocrFile']
    reference_file = request.files['referenceFile']
    
    # Check if file names are not empty
    if ocr_file.filename == '' or reference_file.filename == '':
        return "Both files must be selected."
    
    img_ocr = Image.open(ocr_file)
    text_ocr = pytesseract.image_to_string(img_ocr, lang='eng+tam')
    
     # Convert PIL Image to NumPy array for dlib face detection
    img_array_ocr = np.array(img_ocr)

    # Perform face detection with dlib
    faces = detector(img_array_ocr, 1)

    # Load reference image for comparison
    reference_image = face_recognition.load_image_file(reference_file)
    reference_encoding = face_recognition.face_encodings(reference_image)
    
    if not reference_encoding:
        return "No face found in the reference image. Please provide an image with a face for comparison."
    
    #use the first face encoding
    reference_encoding = reference_encoding[0]
    

    # Perform image comparison
    uploaded_encoding = face_recognition.face_encodings(img_array_ocr)
    
    if not uploaded_encoding:
        return "No face found in the reference image. Please provide an image with a face for comparison."
    
    #use the first face encoding
    uploaded_encoding = uploaded_encoding[0]
    
    face_distances = face_recognition.face_distance([reference_encoding], uploaded_encoding)

    # Determine if the images belong to the same person
    is_same_person = face_recognition.compare_faces([reference_encoding], uploaded_encoding)[0]

    # Compute accuracy score (smaller distance values indicate a closer match)
    accuracy_score = 1 - face_distances[0]

    return render_template('result.html', text_ocr=text_ocr, is_same_person=is_same_person, accuracy_score=accuracy_score)

if __name__ == '__main__':
    app.run(debug=True)