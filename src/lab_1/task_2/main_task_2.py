from pprint import pprint

from config import (
    PIP_FULL,
    SN,
    POW_LINEAR,
    POW_START_NONCE,
    POW_SUFFIX,
    POW_MAX_NONCE,
    BLOCKS_TO_MINE_FOR_REWARD,
    USER_TX_AMOUNT,
    MINER_ADDRESS,
)
from blockchain import KarakaiOleksandrBlockchain


def run_task_2() -> None:
    print("=== Blockchain Lab #1 (Python) ===")
    print(f"PIP: {PIP_FULL}")
    print(f"SN: {SN}")
    print(f"PoW mode: {'LINEAR' if POW_LINEAR else 'RANDOM'}")
    print(f"PoW start nonce: {POW_START_NONCE}")
    print(f"PoW hash suffix: {POW_SUFFIX}")
    print(f"PoW max nonce: {POW_MAX_NONCE}")
    print()

    bc = KarakaiOleksandrBlockchain()

    print("Genesis block created (WITH coinbase + PoW).")
    print("Chain (compact):")
    pprint(bc.KarakaiOleksandr_dump_chain())
    print("\nBalances after genesis:")
    pprint(bc.KarakaiOleksandr_dump_balances())
    print()

    # -----------------------------
    # Завдання №2, п.3:
    # Намайнити ((DD+1) mod 13) блоків і отримати винагороди
    # -----------------------------
    print(f"Mining reward blocks count = {BLOCKS_TO_MINE_FOR_REWARD}")
    for _ in range(BLOCKS_TO_MINE_FOR_REWARD):
        meta = bc.KarakaiOleksandr_mine_block()
        print(
            f"Block #{meta['index']} mined | "
            f"reward={meta['reward']:.6f} | "
            f"iterations={meta['iterations']} | "
            f"nonce={meta['nonce']} | "
            f"hash_end={meta['hash'][-4:]}"
        )

    print("\nChain after reward mining (verbose):")
    pprint(bc.KarakaiOleksandr_dump_chain_verbose())

    print("\nBalances after reward mining:")
    pprint(bc.KarakaiOleksandr_dump_balances())
    print("\nMempool state:", bc.KarakaiOleksandr_dump_mempool())
    print()

    # -----------------------------
    # Завдання №2, п.4-6:
    # Мempool + баланси + майнінг блоків з user-транзакціями (переказ DD монет)
    # -----------------------------
    wallet_a = "WalletA"
    wallet_b = "WalletB"

    print("=== Funding wallets from miner (so users can transfer) ===")
    print("Mempool BEFORE:", bc.KarakaiOleksandr_dump_mempool())

    # Перекидаємо по 13 монет з майнера двом гаманцям
    bc.KarakaiOleksandr_new_transaction(MINER_ADDRESS, wallet_a, USER_TX_AMOUNT)
    bc.KarakaiOleksandr_new_transaction(MINER_ADDRESS, wallet_b, USER_TX_AMOUNT)

    print("Mempool AFTER funding tx:", bc.KarakaiOleksandr_dump_mempool())

    print("\nMining block with funding tx...")
    meta = bc.KarakaiOleksandr_mine_block()
    print(f"Mined block #{meta['index']} | tx_count={meta['tx_count']} | reward={meta['reward']:.6f} | hash_end={meta['hash'][-4:]}")

    print("\nBalances after funding block:")
    pprint(bc.KarakaiOleksandr_dump_balances())
    print("Mempool state:", bc.KarakaiOleksandr_dump_mempool())
    print()

    print("=== User transfers WalletA <-> WalletB by DD coins ===")
    bc.KarakaiOleksandr_new_transaction(wallet_a, wallet_b, USER_TX_AMOUNT)
    bc.KarakaiOleksandr_new_transaction(wallet_b, wallet_a, USER_TX_AMOUNT)

    print("Mempool before mining user-tx block:", bc.KarakaiOleksandr_dump_mempool())

    print("\nMining block with user transactions...")
    meta = bc.KarakaiOleksandr_mine_block()
    print(f"Mined block #{meta['index']} | tx_count={meta['tx_count']} | reward={meta['reward']:.6f} | hash_end={meta['hash'][-4:]}")

    print("\nFinal chain (verbose):")
    pprint(bc.KarakaiOleksandr_dump_chain_verbose())

    print("\nFinal balances:")
    pprint(bc.KarakaiOleksandr_dump_balances())

    print("\nFinal mempool state:", bc.KarakaiOleksandr_dump_mempool())

