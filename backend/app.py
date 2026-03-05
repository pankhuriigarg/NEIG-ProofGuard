from flask import Flask, request, render_template
from hashing import generate_hash
import os

app = Flask(__name__, template_folder='../frontend/templates', 
            static_folder='../frontend/static')

UPLOAD_FOLDER = '../uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return "No file selected", 400
    
    file = request.files['file']
    
    if file.filename == '':
        return "No file selected", 400
    
    # File save karo
    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(file_path)
    
    # Hash generate karo
    hash_value = generate_hash(file_path)
    
    return render_template('result.html', 
                         filename=file.filename, 
                         hash_value=hash_value)

if __name__ == "__main__":
    app.run(debug=True)