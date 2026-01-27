# src/demo.py
from pprint import pprint

from config import PIP_FULL, SN, POW_LINEAR, POW_START_NONCE, POW_SUFFIX, POW_MAX_NONCE
from blockchain import KarakaiOleksandrBlockchain


def run_task_1() -> None:
    print("=== Blockchain Lab #1 (Python) ===")
    print(f"PIP: {PIP_FULL}")
    print(f"SN: {SN}")
    print(f"PoW mode: {'LINEAR' if POW_LINEAR else 'RANDOM'}")
    print(f"PoW start nonce: {POW_START_NONCE}")
    print(f"PoW hash suffix: {POW_SUFFIX}")
    print(f"PoW max nonce: {POW_MAX_NONCE}")
    print()

    bc = KarakaiOleksandrBlockchain()

    print("Genesis block created.")
    pprint(bc.KarakaiOleksandr_dump_chain())
    print()

    next_index = bc.KarakaiOleksandr_new_transaction("Alice", "Bob", 10)
    print(f"Added transaction -> will be included in block #{next_index}")

    next_index = bc.KarakaiOleksandr_new_transaction("Bob", "Charlie", 3)
    print(f"Added transaction -> will be included in block #{next_index}")
    print()

    print("Mining a new block with PoW...")
    meta = bc.KarakaiOleksandr_mine_block()
    print("Mined!")
    print(f"Block index: {meta['index']}")
    print(f"Iterations: {meta['iterations']}")
    print(f"Nonce found: {meta['nonce']}")
    print(f"Hash: {meta['hash']}")
    print()

    print("Current chain:")
    pprint(bc.KarakaiOleksandr_dump_chain())
