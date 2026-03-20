from web3 import Web3
import json
import os
from config import GANACHE_URL, ACCOUNT_ADDRESS, PRIVATE_KEY

# Ganache se connect karo
w3 = Web3(Web3.HTTPProvider(GANACHE_URL))

def is_connected():
    return w3.is_connected()

def store_hash(case_id, file_hash, file_name, contract_address, contract_abi):
    contract = w3.eth.contract(
        address=contract_address,
        abi=contract_abi
    )
    
    # Transaction banao
    tx = contract.functions.storeEvidence(
        case_id,
        file_hash,
        file_name
    ).build_transaction({
        'from': ACCOUNT_ADDRESS,
        'nonce': w3.eth.get_transaction_count(ACCOUNT_ADDRESS),
        'gas': 2000000,
        'gasPrice': w3.to_wei('20', 'gwei')
    })
    
    # Sign karo
    signed_tx = w3.eth.account.sign_transaction(tx, PRIVATE_KEY)
    
    # Send karo
    tx_hash = w3.eth.send_raw_transaction(signed_tx.raw_transaction)
    
    # Receipt lo
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