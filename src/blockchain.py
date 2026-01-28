# src/blockchain.py
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
import hashlib
import random
from typing import List, Dict, Any, Tuple

from config import (
    PIP_FULL,
    SN,
    POW_START_NONCE,
    POW_SUFFIX,
    POW_MAX_NONCE,
    POW_LINEAR,
    GENESIS_PREV_HASH,
    COINBASE_SENDER,
    MINER_ADDRESS,
    REWARD_INITIAL,
    REWARD_DIVISOR,
)


@dataclass(frozen=True)
class KarakaiOleksandrTransaction:
    sender: str
    recipient: str
    amount: float


@dataclass(frozen=True)
class KarakaiOleksandrBlock:
    index: int
    timestamp: int
    transactions: List[KarakaiOleksandrTransaction]
    nonce: int
    previous_hash: str
    current_hash: str


class KarakaiOleksandrBlockchain:
    """
    Завдання №1: скелет блокчейну + PoW (hash має закінчуватись на MM="09")
    Завдання №2: coinbase, нагорода, мемпул, баланси
    """

    def __init__(self) -> None:
        self.KarakaiOleksandr_chain: List[KarakaiOleksandrBlock] = []
        self.KarakaiOleksandr_mempool: List[KarakaiOleksandrTransaction] = []
        self.KarakaiOleksandr_balances: Dict[str, float] = {}

        # Генезис: prev_hash = SN, + coinbase, + PoW, + нарахування винагороди
        self.KarakaiOleksandr_create_genesis_block()

    # ----------------------------
    # Balances
    # ----------------------------
    def KarakaiOleksandr_get_balance(self, address: str) -> float:
        return float(self.KarakaiOleksandr_balances.get(address, 0.0))

    def KarakaiOleksandr_apply_transaction(self, tx: KarakaiOleksandrTransaction) -> None:
        """
        Застосовує транзакцію до балансів.
        Coinbase: sender == COINBASE -> просто додаємо отримувачу.
        """
        if tx.sender == COINBASE_SENDER:
            self.KarakaiOleksandr_balances[tx.recipient] = self.KarakaiOleksandr_get_balance(tx.recipient) + tx.amount
            return

        sender_balance = self.KarakaiOleksandr_get_balance(tx.sender)
        if sender_balance < tx.amount:
            raise ValueError(f"Insufficient funds: {tx.sender} has {sender_balance}, needs {tx.amount}")

        self.KarakaiOleksandr_balances[tx.sender] = sender_balance - tx.amount
        self.KarakaiOleksandr_balances[tx.recipient] = self.KarakaiOleksandr_get_balance(tx.recipient) + tx.amount

    # ----------------------------
    # Mempool / transactions
    # ----------------------------
    def KarakaiOleksandr_new_transaction(self, sender: str, recipient: str, amount: float) -> int:
        """
        User-транзакція у мемпул.
        Coinbase у мемпул не додаємо (вона додається автоматично під час майнінгу).
        """
        if sender == COINBASE_SENDER:
            raise ValueError("Coinbase transaction is created automatically during mining.")

        if amount <= 0:
            raise ValueError("Amount must be positive.")

        # Простий чек: баланс відправника має покривати amount (pending у мемпулі не враховуємо)
        effective = self.KarakaiOleksandr_get_effective_balance(sender)
        if effective < amount:
            raise ValueError(f"Insufficient funds for mempool tx: {sender} has {effective}")

        tx = KarakaiOleksandrTransaction(sender=sender, recipient=recipient, amount=float(amount))
        self.KarakaiOleksandr_mempool.append(tx)
        return self.KarakaiOleksandr_last_block().index + 1

    # ----------------------------
    # Reward / coinbase
    # ----------------------------
    def KarakaiOleksandr_get_block_reward(self, block_index: int) -> float:
        """
        Початкова винагорода = YYYY.
        Кожні 2 блоки винагорода зменшується у (MM+1) разів.

        Враховуємо генезис у правилі "кожні 2 блоки":
          index 0-1: 1991
          index 2-3: 1991/10
          index 4-5: 1991/100 ...
        """
        reduction_steps = max(0, block_index) // 2
        return float(REWARD_INITIAL) / float(REWARD_DIVISOR ** reduction_steps)

    def KarakaiOleksandr_create_coinbase_transaction(self, reward: float) -> KarakaiOleksandrTransaction:
        return KarakaiOleksandrTransaction(
            sender=COINBASE_SENDER,
            recipient=MINER_ADDRESS,
            amount=float(reward),
        )

    # ----------------------------
    # Blocks / chain
    # ----------------------------
    def KarakaiOleksandr_last_block(self) -> KarakaiOleksandrBlock:
        return self.KarakaiOleksandr_chain[-1]

    def KarakaiOleksandr_create_genesis_block(self) -> KarakaiOleksandrBlock:
        """
        Генезис-блок:
          - previous_hash = SN ("Karakai")
          - містить coinbase з reward для block_index=0
          - проходить PoW (hash закінчується на "09")
          - одразу нараховує reward у баланси
        """
        timestamp = int(datetime.now(tz=timezone.utc).timestamp())
        prev = GENESIS_PREV_HASH  # "Karakai"

        reward = self.KarakaiOleksandr_get_block_reward(0)
        coinbase_tx = self.KarakaiOleksandr_create_coinbase_transaction(reward)
        txs = [coinbase_tx]

        nonce, iterations, cur_hash = self.KarakaiOleksandr_proof_of_work(
            index=0,
            timestamp=timestamp,
            transactions=txs,
            previous_hash=prev,
        )

        genesis = KarakaiOleksandrBlock(
            index=0,
            timestamp=timestamp,
            transactions=txs,
            nonce=nonce,
            previous_hash=prev,
            current_hash=cur_hash,
        )
        self.KarakaiOleksandr_chain.append(genesis)

        # Застосовуємо coinbase до балансів
        self.KarakaiOleksandr_apply_transaction(coinbase_tx)

        return genesis

    def KarakaiOleksandr_mine_block(self) -> Dict[str, Any]:
        """
        Майнінг блоку:
          - coinbase додається автоматично
          - user-транзакції беруться з mempool
          - PoW за правилом hash.endswith("09")
          - після майнінгу транзакції застосовуються до балансів
        """
        last = self.KarakaiOleksandr_last_block()
        new_index = last.index + 1
        prev_hash = last.current_hash
        timestamp = int(datetime.now(tz=timezone.utc).timestamp())

        reward = self.KarakaiOleksandr_get_block_reward(new_index)
        coinbase_tx = self.KarakaiOleksandr_create_coinbase_transaction(reward)

        txs = [coinbase_tx] + list(self.KarakaiOleksandr_mempool)
        self.KarakaiOleksandr_mempool.clear()

        nonce, iterations, cur_hash = self.KarakaiOleksandr_proof_of_work(
            index=new_index,
            timestamp=timestamp,
            transactions=txs,
            previous_hash=prev_hash,
        )

        block = KarakaiOleksandrBlock(
            index=new_index,
            timestamp=timestamp,
            transactions=txs,
            nonce=nonce,
            previous_hash=prev_hash,
            current_hash=cur_hash,
        )
        self.KarakaiOleksandr_chain.append(block)

        # застосовуємо транзакції до балансів
        for tx in txs:
            self.KarakaiOleksandr_apply_transaction(tx)

        return {
            "index": new_index,
            "iterations": iterations,
            "nonce": nonce,
            "hash": cur_hash,
            "reward": reward,
            "tx_count": len(txs),
        }

    # ----------------------------
    # Hashing / PoW
    # ----------------------------
    @staticmethod
    def KarakaiOleksandr_hash_payload(
        index: int,
        timestamp: int,
        transactions: List[KarakaiOleksandrTransaction],
        nonce: int,
        previous_hash: str,
    ) -> str:
        """
        SHA-256 від payload у фіксованому порядку.
        """
        tx_part = "".join(f"{t.sender}->{t.recipient}:{t.amount};" for t in transactions)
        payload = f"{index}|{timestamp}|{tx_part}|{nonce}|{previous_hash}"
        return hashlib.sha256(payload.encode("utf-8")).hexdigest()

    def KarakaiOleksandr_is_pow_valid(self, block_hash: str) -> bool:
        return block_hash.endswith(POW_SUFFIX)

    def KarakaiOleksandr_proof_of_work(
        self,
        index: int,
        timestamp: int,
        transactions: List[KarakaiOleksandrTransaction],
        previous_hash: str,
    ) -> Tuple[int, int, str]:
        """
        Повертає (nonce, iterations, hash).
        """
        iterations = 0

        if POW_LINEAR:
            # лінійний перебір
            nonce = POW_START_NONCE
            while nonce <= POW_MAX_NONCE:
                iterations += 1
                h = self.KarakaiOleksandr_hash_payload(index, timestamp, transactions, nonce, previous_hash)
                if self.KarakaiOleksandr_is_pow_valid(h):
                    return nonce, iterations, h
                nonce += 1
            raise RuntimeError("PoW failed: nonce exceeded POW_MAX_NONCE (linear search).")

        # RANDOM перебір (для Karakai)
        # щоб було "випадковим чином", але без зависання: уникаємо повторів nonce
        max_range = POW_MAX_NONCE - POW_START_NONCE + 1
        max_attempts = max(50_000, max_range)
        seen = set()

        while iterations < max_attempts and len(seen) < max_range:
            iterations += 1
            nonce = random.randint(POW_START_NONCE, POW_MAX_NONCE)
            if nonce in seen:
                continue
            seen.add(nonce)

            h = self.KarakaiOleksandr_hash_payload(index, timestamp, transactions, nonce, previous_hash)
            if self.KarakaiOleksandr_is_pow_valid(h):
                return nonce, iterations, h

        raise RuntimeError("PoW failed: could not find valid nonce within attempts (random search).")

    # ----------------------------
    # Output helpers
    # ----------------------------
    def KarakaiOleksandr_dump_chain(self) -> List[Dict[str, Any]]:
        out: List[Dict[str, Any]] = []
        for b in self.KarakaiOleksandr_chain:
            out.append(
                {
                    "index": b.index,
                    "timestamp": b.timestamp,
                    "prev_hash": b.previous_hash,
                    "curr_hash": b.current_hash,
                    "nonce": b.nonce,
                    "tx_count": len(b.transactions),
                }
            )
        return out

    def KarakaiOleksandr_dump_chain_verbose(self) -> List[Dict[str, Any]]:
        """
        Розширений дамп: показати ще й транзакції в кожному блоці (зручно для скрінів).
        """
        out: List[Dict[str, Any]] = []
        for b in self.KarakaiOleksandr_chain:
            out.append(
                {
                    "index": b.index,
                    "timestamp": b.timestamp,
                    "prev_hash": b.previous_hash,
                    "curr_hash": b.current_hash,
                    "nonce": b.nonce,
                    "transactions": [
                        {"sender": t.sender, "recipient": t.recipient, "amount": t.amount}
                        for t in b.transactions
                    ],
                }
            )
        return out

    def KarakaiOleksandr_dump_mempool(self) -> List[Dict[str, Any]]:
        return [
            {"sender": t.sender, "recipient": t.recipient, "amount": t.amount}
            for t in self.KarakaiOleksandr_mempool
        ]

    def KarakaiOleksandr_dump_balances(self) -> Dict[str, float]:
        return dict(sorted(self.KarakaiOleksandr_balances.items(), key=lambda x: x[0].lower()))
    
    def KarakaiOleksandr_get_effective_balance(self, address: str) -> float:
        """
        Баланс з урахуванням mempool:
        confirmed_balance + pending_in - pending_out
        (coinbase у mempool не буває, ми його туди не додаємо)
        """
        confirmed = self.KarakaiOleksandr_get_balance(address)
        pending_in = 0.0
        pending_out = 0.0

        for tx in self.KarakaiOleksandr_mempool:
            if tx.recipient == address:
                pending_in += tx.amount
            if tx.sender == address:
                pending_out += tx.amount

        return confirmed + pending_in - pending_out


    def KarakaiOleksandr_new_transaction(self, sender: str, recipient: str, amount: float) -> int:
        """
        User-транзакція у мемпул.
        Coinbase у мемпул не додаємо (вона додається автоматично під час майнінгу).
        """
        if sender == COINBASE_SENDER:
            raise ValueError("Coinbase transaction is created automatically during mining.")

        if amount <= 0:
            raise ValueError("Amount must be positive.")

        # Перевіряємо баланс з урахуванням pending транзакцій у mempool
        effective_balance = self.KarakaiOleksandr_get_effective_balance(sender)
        if effective_balance < amount:
            raise ValueError(
                f"Insufficient funds for mempool tx: {sender} has {effective_balance}"
            )

        tx = KarakaiOleksandrTransaction(sender=sender, recipient=recipient, amount=float(amount))
        self.KarakaiOleksandr_mempool.append(tx)
        return self.KarakaiOleksandr_last_block().index + 1

