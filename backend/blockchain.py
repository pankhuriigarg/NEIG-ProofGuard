from web3 import Web3
import json
import os
from config import GANACHE_URL, ACCOUNT_ADDRESS, PRIVATE_KEY
from datetime import datetime
# Ganache se connect karo
w3 = Web3(Web3.HTTPProvider(GANACHE_URL))

def is_connected():
    return w3.is_connected()

def store_hash(case_id, file_hash, file_name, investigator_name, contract_address, contract_abi):
    contract = w3.eth.contract(
        address=contract_address,
        abi=contract_abi
    )
    
    tx = contract.functions.storeEvidence(
        case_id,
        file_hash,
        file_name,
        investigator_name
    ).build_transaction({
        'from': ACCOUNT_ADDRESS,
        'nonce': w3.eth.get_transaction_count(ACCOUNT_ADDRESS),
        'gas': 2000000,
        'gasPrice': w3.to_wei('20', 'gwei')
    })
    
    signed_tx = w3.eth.account.sign_transaction(tx, PRIVATE_KEY)
    tx_hash = w3.eth.send_raw_transaction(signed_tx.raw_transaction)
    receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
    
    return receipt.transactionHash.hex()

def transfer_custody(case_id, from_custodian, to_custodian, remarks, contract_address, contract_abi):
    contract = w3.eth.contract(
        address=contract_address,
        abi=contract_abi
    )
    
    tx = contract.functions.transferCustody(
        case_id,
        from_custodian,
        to_custodian,
        remarks
    ).build_transaction({
        'from': ACCOUNT_ADDRESS,
        'nonce': w3.eth.get_transaction_count(ACCOUNT_ADDRESS),
        'gas': 2000000,
        'gasPrice': w3.to_wei('20', 'gwei')
    })
    
    signed_tx = w3.eth.account.sign_transaction(tx, PRIVATE_KEY)
    tx_hash = w3.eth.send_raw_transaction(signed_tx.raw_transaction)
    receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
    
    return receipt.transactionHash.hex()

def verify_hash(case_id, file_hash, contract_address, contract_abi):
    contract = w3.eth.contract(
        address=contract_address,
        abi=contract_abi
    )
    
    result = contract.functions.verifyEvidence(
        case_id,
        file_hash
    ).call()
    
    return result

def get_evidence(case_id, contract_address, contract_abi):
    contract = w3.eth.contract(
        address=contract_address,
        abi=contract_abi
    )
    
    result = contract.functions.getEvidence(case_id).call()
    
    return {
        'file_hash': result[0],
        'file_name': result[1],
        'timestamp': result[2]
    }

def get_custody_history(case_id, contract_address, contract_abi):
    contract = w3.eth.contract(
        address=contract_address,
        abi=contract_abi
    )
    
    count = contract.functions.getCustodyCount(case_id).call()
    history = []
    
    for i in range(count):
        record = contract.functions.getCustodyRecord(case_id, i).call()
        history.append({
            'from': record[0],
            'to': record[1],
            'timestamp': datetime.fromtimestamp(record[2]).strftime('%d %b %Y, %I:%M %p'),
            'remarks': record[3]
        })
    
    return history

def get_all_cases(contract_address, contract_abi):
    contract = w3.eth.contract(
        address=contract_address,
        abi=contract_abi
    )
    
    count = contract.functions.getCaseCount().call()
    cases = []
    
    for i in range(count):
        case_id = contract.functions.getCaseId(i).call()
        evidence = get_evidence(case_id, contract_address, contract_abi)
        custody_count = contract.functions.getCustodyCount(case_id).call()
        cases.append({
            'case_id': case_id,
            'file_name': evidence['file_name'],
            'timestamp': datetime.fromtimestamp(evidence['timestamp']).strftime('%d %b %Y, %I:%M %p'),
            'custody_count': custody_count
        })
    
    return cases