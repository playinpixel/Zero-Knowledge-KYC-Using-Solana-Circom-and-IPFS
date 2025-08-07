from web3 import Web3
w3 = Web3(Web3.HTTPProvider('http://127.0.0.1:7545'))
print(w3.is_connected())

contract = w3.eth.contract(address=CONTRACT_ADDRESS, abi=ABI)
print(contract.functions)  # Should not error if contract exists