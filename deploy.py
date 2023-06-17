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
my_address = '0xE6F04d6C5f2CfA3480a53435F81Ae94383CEb18f'
private_key = '6672d9370a2d6ef643d7ccc58c924fb1752aad11878fbe58dd558315ab5105b3'

# create the contract
SimpleStorage = w3.eth.contract(abi=abi, bytecode=bytecode)

# get latest transaction
nonce = w3.eth.get_transaction_count(my_address)
print(nonce)

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

# print(transaction)
