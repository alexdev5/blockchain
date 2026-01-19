# src/blockchain.py
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
import hashlib
import random
from typing import List, Optional, Dict, Any

from config import (
    PIP_FULL,
    SN,
    POW_START_NONCE,
    POW_SUFFIX,
    POW_MAX_NONCE,
    POW_LINEAR,
    GENESIS_PREV_HASH,
)


@dataclass(frozen=True)
class KarakaiOleksandrTransaction:
    sender: str
    recipient: str
    amount: int


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
    Скелет блокчейну + PoW відповідно до індивідуального завдання №1.
    """

    def __init__(self) -> None:
        self.KarakaiOleksandr_chain: List[KarakaiOleksandrBlock] = []
        self.KarakaiOleksandr_mempool: List[KarakaiOleksandrTransaction] = []

        # Генезис-блок: previousHash = [SN] = "Karakai"
        self.KarakaiOleksandr_create_genesis_block()

    # ----------------------------
    # Transaction / mempool
    # ----------------------------
    def KarakaiOleksandr_new_transaction(self, sender: str, recipient: str, amount: int) -> int:
        tx = KarakaiOleksandrTransaction(sender=sender, recipient=recipient, amount=amount)
        self.KarakaiOleksandr_mempool.append(tx)
        # повертаємо індекс блоку, куди потрапить транзакція (наступний, який буде намайнено)
        return self.KarakaiOleksandr_last_block().index + 1

    # ----------------------------
    # Blocks / chain
    # ----------------------------
    def KarakaiOleksandr_last_block(self) -> KarakaiOleksandrBlock:
        return self.KarakaiOleksandr_chain[-1]

    def KarakaiOleksandr_create_genesis_block(self) -> KarakaiOleksandrBlock:
        # nonce/proof тут формально будь-який; ставимо 0
        timestamp = int(datetime.now(tz=timezone.utc).timestamp())
        nonce = 0
        prev = GENESIS_PREV_HASH  # "Karakai"
        cur_hash = self.KarakaiOleksandr_hash_payload(
            index=0,
            timestamp=timestamp,
            transactions=[],
            nonce=nonce,
            previous_hash=prev,
        )
        genesis = KarakaiOleksandrBlock(
            index=0,
            timestamp=timestamp,
            transactions=[],
            nonce=nonce,
            previous_hash=prev,
            current_hash=cur_hash,
        )
        self.KarakaiOleksandr_chain.append(genesis)
        return genesis

    def KarakaiOleksandr_mine_block(self) -> Dict[str, Any]:
        """
        Майнимо новий блок.
        PoW:
          - старт Nonce = DDMM = 1309
          - валідність: hash ... закінчується на [MM] => "09"
          - перебір: якщо прізвище парне -> лінійний, інакше -> випадковий
          - max nonce = MMYYYY => 91991
        Повертаємо метадані для виводу (ітерації, nonce).
        """
        last = self.KarakaiOleksandr_last_block()
        new_index = last.index + 1
        prev_hash = last.current_hash

        # транзакції з mempool переносимо в блок (копія), mempool очищаємо
        txs = list(self.KarakaiOleksandr_mempool)
        self.KarakaiOleksandr_mempool.clear()

        timestamp = int(datetime.now(tz=timezone.utc).timestamp())

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

        return {
            "index": new_index,
            "iterations": iterations,
            "nonce": nonce,
            "hash": cur_hash,
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
        Хеш блоку на основі полів у незмінному порядку.
        Використовуємо SHA-256.
        """
        tx_part = "".join(f"{t.sender}->{t.recipient}:{t.amount};" for t in transactions)
        payload = f"{index}|{timestamp}|{tx_part}|{nonce}|{previous_hash}"
        return hashlib.sha256(payload.encode("utf-8")).hexdigest()

    def KarakaiOleksandr_is_pow_valid(self, block_hash: str) -> bool:
        # підтвердження доказу: наявність в кінці хешу [MM] => "09"
        return block_hash.endswith(POW_SUFFIX)

    def KarakaiOleksandr_proof_of_work(
        self,
        index: int,
        timestamp: int,
        transactions: List[KarakaiOleksandrTransaction],
        previous_hash: str,
    ) -> tuple[int, int, str]:
        """
        Повертає (nonce, iterations, hash).
        """
        iterations = 0

        if POW_LINEAR:
            # парна кількість літер у прізвищі -> лінійний перебір
            nonce = POW_START_NONCE
            while nonce <= POW_MAX_NONCE:
                iterations += 1
                h = self.KarakaiOleksandr_hash_payload(index, timestamp, transactions, nonce, previous_hash)
                if self.KarakaiOleksandr_is_pow_valid(h):
                    return nonce, iterations, h
                nonce += 1

            raise RuntimeError("PoW failed: nonce exceeded POW_MAX_NONCE (linear search).")

        # непарна кількість літер -> випадковий перебір (Karakai -> непарна)
        # Щоб уникнути нескінченного циклу — обмежимо кількість спроб розумно:
        max_attempts = max(10_000, POW_MAX_NONCE - POW_START_NONCE + 1)
        seen = set()

        while iterations < max_attempts and len(seen) < (POW_MAX_NONCE - POW_START_NONCE + 1):
            iterations += 1

            # випадковий nonce у діапазоні
            nonce = random.randint(POW_START_NONCE, POW_MAX_NONCE)
            if nonce in seen:
                continue
            seen.add(nonce)

            h = self.KarakaiOleksandr_hash_payload(index, timestamp, transactions, nonce, previous_hash)
            if self.KarakaiOleksandr_is_pow_valid(h):
                return nonce, iterations, h

        raise RuntimeError("PoW failed: could not find valid nonce within attempts (random search).")

    # ----------------------------
    # Helpers for output
    # ----------------------------
    def KarakaiOleksandr_dump_chain(self) -> List[Dict[str, Any]]:
        """
        Повертає chain у вигляді списку словників для зручного друку.
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
                    "tx_count": len(b.transactions),
                }
            )
        return out
