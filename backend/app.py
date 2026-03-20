from flask import Flask, request, render_template
from hashing import generate_hash
from blockchain import store_hash, verify_hash, is_connected
import json
import os

app = Flask(__name__, 
            template_folder='../frontend/templates', 
            static_folder='../frontend/static')

UPLOAD_FOLDER = '../uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Contract data load karo
with open('contract_data.json', 'r') as f:
    contract_data = json.load(f)

CONTRACT_ADDRESS = contract_data['address']
CONTRACT_ABI = contract_data['abi']

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return "No file selected", 400
    
    file = request.files['file']
    case_id = request.form.get('case_id', 'CASE001')
    
    if file.filename == '':
        return "No file selected", 400
    
    # File save karo
    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(file_path)
    
    # Hash generate karo
    hash_value = generate_hash(file_path)
    
    # Blockchain pe store karo
    tx_hash = store_hash(
        case_id, 
        hash_value, 
        file.filename,
        CONTRACT_ADDRESS,
        CONTRACT_ABI
    )
    
    return render_template('result.html', 
                         filename=file.filename,
                         case_id=case_id,
                         hash_value=hash_value,
                         tx_hash=tx_hash)

@app.route('/court')
def court_portal():
    return render_template('court_portal.html')

@app.route('/verify', methods=['POST'])
def verify():
    if 'file' not in request.files:
        return "No file selected", 400
    
    file = request.files['file']
    case_id = request.form.get('case_id', '')
    
    if file.filename == '':
        return "No file selected", 400
    
    # File save karo
    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(file_path)
    
    # Hash generate karo
    hash_value = generate_hash(file_path)
    
    # Blockchain se verify karo
    is_authentic = verify_hash(
        case_id,
        hash_value,
        CONTRACT_ADDRESS,
        CONTRACT_ABI
    )
    
    return render_template('verdict.html',
                         filename=file.filename,
                         case_id=case_id,
                         hash_value=hash_value,
                         is_authentic=is_authentic)

if __name__ == "__main__":
    app.run(debug=True)