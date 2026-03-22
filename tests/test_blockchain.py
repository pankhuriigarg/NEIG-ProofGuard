import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))

from web3 import Web3
from config import GANACHE_URL

def test_blockchain_connection():
    w3 = Web3(Web3.HTTPProvider(GANACHE_URL))
    assert w3.is_connected()
    print("✅ Blockchain connected!")

def test_account_has_balance():
    w3 = Web3(Web3.HTTPProvider(GANACHE_URL))
    from config import ACCOUNT_ADDRESS
    balance = w3.eth.get_balance(ACCOUNT_ADDRESS)
    assert balance > 0
    print(f"✅ Account balance: {w3.from_wei(balance, 'ether')} ETH")

def test_contract_deployed():
    from config import CONTRACT_ADDRESS
    assert CONTRACT_ADDRESS != ""
    assert len(CONTRACT_ADDRESS) == 42
    print(f"✅ Contract deployed at: {CONTRACT_ADDRESS[:20]}...")

if __name__ == "__main__":
    test_blockchain_connection()
    test_account_has_balance()
    test_contract_deployed()
    print("\n✅ All blockchain tests passed!")