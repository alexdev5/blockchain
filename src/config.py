# src/config.py

# Вихідні дані
PIP_FULL = "Karakai Oleksandr"
SN = "Karakai"

DD = 13
MM = 9
YYYY = 1991

# --- Завдання №1 ---
POW_START_NONCE = int(f"{DD:02d}{MM:02d}")         # DDMM = 1309
POW_SUFFIX = f"{MM:02d}"                           # "09"
POW_MAX_NONCE = int(f"{MM:02d}{YYYY}")             # MMYYYY = 091991 -> 91991

SURNAME_LEN = len(SN)
POW_LINEAR = (SURNAME_LEN % 2 == 0)                # Karakai -> 7 -> False (рандом)

# Генезис-блок: previousHash = [SN]
GENESIS_PREV_HASH = SN

# --- Завдання №2 ---

COINBASE_SENDER = "COINBASE"
MINER_ADDRESS = PIP_FULL  # адреса майнера

REWARD_INITIAL = YYYY      # 1991
REWARD_DIVISOR = MM + 1    # 10

BLOCKS_TO_MINE_FOR_REWARD = (DD + 1) % 13  # 1

USER_TX_AMOUNT = DD        # 13
