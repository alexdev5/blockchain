# src/config.py

# Вихідні дані
PIP_FULL = "Karakai Oleksandr"
SN = "Karakai"

DD = 13
MM = 9
YYYY = 1991

# Правила PoW (завдання №1)
POW_START_NONCE = int(f"{DD:02d}{MM:02d}")          # DDMM = 1309
POW_SUFFIX = f"{MM:02d}"                           # "09"
POW_MAX_NONCE = int(f"{MM:02d}{YYYY}")             # MMYYYY = 091991 -> 91991

SURNAME_LEN = len(SN)
POW_LINEAR = (SURNAME_LEN % 2 == 0)                # Karakai -> 7 -> False (рандом)

# Генезис-блок: previousHash = [SN]
GENESIS_PREV_HASH = SN
