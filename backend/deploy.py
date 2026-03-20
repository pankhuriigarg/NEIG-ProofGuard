from web3 import Web3
from solcx import compile_source, install_solc
import json
from config import GANACHE_URL, ACCOUNT_ADDRESS, PRIVATE_KEY

# Solc install karo
install_solc('0.8.0')

# Solidity contract read karo
with open('../blockchain/contracts/EvidenceStorage.sol', 'r') as f:
    contract_source = f.read()

# Compile karo
compiled = compile_source(
    contract_source,
    output_values=['abi', 'bin'],
    solc_version='0.8.0'
)

# ABI aur bytecode nikalo
contract_interface = compiled['<stdin>:EvidenceStorage']
abi = contract_interface['abi']
bytecode = contract_interface['bin']

# Ganache se connect karo
w3 = Web3(Web3.HTTPProvider(GANACHE_URL))

# Deploy karo
contract = w3.eth.contract(abi=abi, bytecode=bytecode)

tx = contract.constructor().build_transaction({
    'from': ACCOUNT_ADDRESS,
    'nonce': w3.eth.get_transaction_count(ACCOUNT_ADDRESS),
    'gas': 2000000,
    'gasPrice': w3.to_wei('20', 'gwei')
})

signed_tx = w3.eth.account.sign_transaction(tx, PRIVATE_KEY)
tx_hash = w3.eth.send_raw_transaction(signed_tx.raw_transaction)
receipt = w3.eth.wait_for_transaction_receipt(tx_hash)

contract_address = receipt.contractAddress
print(f"Contract deployed at: {contract_address}")

# ABI aur address save karo
with open('contract_data.json', 'w') as f:
    json.dump({
        'address': contract_address,
        'abi': abi
    }, f)

print("contract_data.json saved!")