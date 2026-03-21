from flask import Flask, request, render_template
from hashing import generate_hash
from blockchain import store_hash, verify_hash, is_connected, get_all_cases, get_custody_history, transfer_custody
from zkp import generate_proof, verify_proof
import json
import os

app = Flask(__name__, 
            template_folder='../frontend/templates', 
            static_folder='../frontend/static')

UPLOAD_FOLDER = '../uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

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
    investigator_name = request.form.get('investigator_name', 'Unknown')
    
    if file.filename == '':
        return "No file selected", 400
    
    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(file_path)
    
    hash_value = generate_hash(file_path)
    proof = generate_proof(hash_value)
    
    tx_hash = store_hash(
        case_id,
        hash_value,
        file.filename,
        investigator_name,
        CONTRACT_ADDRESS,
        CONTRACT_ABI
    )
    
    return render_template('result.html', 
                         filename=file.filename,
                         case_id=case_id,
                         investigator_name=investigator_name,
                         hash_value=hash_value,
                         tx_hash=tx_hash,
                         proof=proof)

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
    
    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(file_path)
    
    hash_value = generate_hash(file_path)
    is_authentic = verify_hash(case_id, hash_value, CONTRACT_ADDRESS, CONTRACT_ABI)
    
    # Custody history bhi lo
    custody_history = get_custody_history(case_id, CONTRACT_ADDRESS, CONTRACT_ABI)
    
    return render_template('verdict.html',
                         filename=file.filename,
                         case_id=case_id,
                         hash_value=hash_value,
                         is_authentic=is_authentic,
                         custody_history=custody_history)

@app.route('/dashboard')
def dashboard():
    cases = get_all_cases(CONTRACT_ADDRESS, CONTRACT_ABI)
    return render_template('dashboard.html', cases=cases)

@app.route('/transfer', methods=['GET', 'POST'])
def transfer():
    if request.method == 'POST':
        case_id = request.form.get('case_id')
        from_custodian = request.form.get('from_custodian')
        to_custodian = request.form.get('to_custodian')
        remarks = request.form.get('remarks')
        
        tx_hash = transfer_custody(
            case_id,
            from_custodian,
            to_custodian,
            remarks,
            CONTRACT_ADDRESS,
            CONTRACT_ABI
        )
        
        return render_template('transfer_result.html',
                             case_id=case_id,
                             from_custodian=from_custodian,
                             to_custodian=to_custodian,
                             tx_hash=tx_hash)
    
    return render_template('transfer.html')

if __name__ == "__main__":
    app.run(debug=True)