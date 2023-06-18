from solcx import compile_standard, install_solc
import json
from web3 import Web3

with open('./SimpleStorage.sol', 'r') as file:
    simple_storage_file = file.read()
    
import solcx
version = solcx.get_solc_version()
print('solcx version:', version)

install_solc('0.8.19')

compiled_sol = compile_standard(
    {
        'language': 'Solidity',
        'sources': {'SimpleStorage.sol': {'content': simple_storage_file}},
        'settings': {
            'outputSelection': {
                '*': {'*': ['abi', 'metadata', 'evm.bytecode', 'evm.sourceMap']}
            }
        },
    },
    solc_version='0.8.19',
)

with open('compiled_code.json', 'w') as file:
    json.dump(compiled_sol, file)
    
# get bytecode
bytecode = compiled_sol['contracts']['SimpleStorage.sol']['SimpleStorage']['evm']['bytecode']['object']

# get abi
abi = compiled_sol['contracts']['SimpleStorage.sol']['SimpleStorage']['abi']

# connect to ganache
w3 = Web3(Web3.HTTPProvider('HTTP://127.0.0.1:7545'))
chain_id = w3.eth.chain_id  # 5777
my_address = '0x2313E71C42Ae754DE0A63996c5CCb4B0d672fc82'
private_key = 'f2dee25c974e10a9b72e8895644b6e7bc34bba1ccc6654aac6268f9841d43a4f'

# create the contract
SimpleStorage = w3.eth.contract(abi=abi, bytecode=bytecode)

# get latest transaction
nonce = w3.eth.get_transaction_count(my_address)
print('nonce:', nonce)

# 1. build a transaction
# 2. sign a transaction
# 3. send a transaction
transaction = SimpleStorage.constructor().build_transaction(
    {'gasPrice': w3.eth.gas_price, 
     'chainId': chain_id,
     'from': my_address,
     'nonce': nonce
     }
)

print(transaction)

signed_txn = w3.eth.account.sign_transaction(transaction, private_key=private_key)
print('signed_txn:', signed_txn)
tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
print('tx_hash:', tx_hash)
tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
print('tx_receipt:', tx_receipt)

# working with the contract you need contract address and abi
simple_storage = w3.eth.contract(address=tx_receipt.contractAddress, abi=abi)
# call -> simulate making the call and getting a return value
# transact -> actually make a state change
print(simple_storage.functions.retrieve().call())  # get favoriteNumber
