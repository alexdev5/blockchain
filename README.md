# Лабораторна робота №1
## Завдання 1 (тест)
=== Blockchain Lab #1 (Python) ===
karakai-blockchain  | PIP: Karakai Oleksandr
karakai-blockchain  | SN: Karakai
karakai-blockchain  | PoW mode: RANDOM
karakai-blockchain  | PoW start nonce: 1309
karakai-blockchain  | PoW hash suffix: 09
karakai-blockchain  | PoW max nonce: 91991
karakai-blockchain  |
karakai-blockchain  | Genesis block created.
karakai-blockchain  | [{'curr_hash': 'ad04891bbef99998974445f4296a828e454c874dffe1bb3590770bfbbd6c9209',
karakai-blockchain  |   'index': 0,
karakai-blockchain  |   'nonce': 75231,
karakai-blockchain  |   'prev_hash': 'Karakai',
karakai-blockchain  |   'timestamp': 1769598493,
karakai-blockchain  |   'tx_count': 1}]
karakai-blockchain  |
karakai-blockchain  | Added transaction -> will be included in block #1
karakai-blockchain  | Added transaction -> will be included in block #1
karakai-blockchain  |
karakai-blockchain  | Mining a new block with PoW...
karakai-blockchain  | Mined!
karakai-blockchain  | Block index: 1
karakai-blockchain  | Iterations: 305
karakai-blockchain  | Nonce found: 68049
karakai-blockchain  | Hash: de677b2282bf896f4904f0139826ef55182951def1c02874dc0b55e4e6bd9509
karakai-blockchain  |
karakai-blockchain  | Current chain:
karakai-blockchain  | [{'curr_hash': 'ad04891bbef99998974445f4296a828e454c874dffe1bb3590770bfbbd6c9209',
karakai-blockchain  |   'index': 0,
karakai-blockchain  |   'nonce': 75231,
karakai-blockchain  |   'prev_hash': 'Karakai',
karakai-blockchain  |   'timestamp': 1769598493,
karakai-blockchain  |   'tx_count': 1},
karakai-blockchain  |  {'curr_hash': 'de677b2282bf896f4904f0139826ef55182951def1c02874dc0b55e4e6bd9509',
karakai-blockchain  |   'index': 1,
karakai-blockchain  |   'nonce': 68049,
karakai-blockchain  |   'prev_hash': 'ad04891bbef99998974445f4296a828e454c874dffe1bb3590770bfbbd6c9209',
karakai-blockchain  |   'timestamp': 1769598493,
karakai-blockchain  |   'tx_count': 5}]

## Завдання 2 (тест)
karakai-blockchain  | Mining block with funding tx...
karakai-blockchain  | Mined block #2 | tx_count=3 | reward=199.100000 | hash_end=8209
karakai-blockchain  |
karakai-blockchain  | Balances after funding block:
karakai-blockchain  | {'Karakai Oleksandr': 4155.1, 'WalletA': 13.0, 'WalletB': 13.0}
karakai-blockchain  | Mempool state: []
karakai-blockchain  |
karakai-blockchain  | === User transfers WalletA <-> WalletB by DD coins ===
karakai-blockchain  | Mempool before mining user-tx block: [{'sender': 'WalletA', 'recipient': 'WalletB', 'amount': 13.0}, {'sender': 'WalletB', 'recipient': 'WalletA', 'amount': 13.0}]
karakai-blockchain  |
karakai-blockchain  | Mining block with user transactions...
karakai-blockchain  | Mined block #3 | tx_count=3 | reward=199.100000 | hash_end=ff09
karakai-blockchain  |
karakai-blockchain  | Final chain (verbose):
karakai-blockchain  | [{'curr_hash': '6933b778b17bdf47c84b4e01c488d555bebe33eaa6aab02a70af14b01f4d9309',
karakai-blockchain  |   'index': 0,
karakai-blockchain  |   'nonce': 51992,
karakai-blockchain  |   'prev_hash': 'Karakai',
karakai-blockchain  |   'timestamp': 1769599097,
karakai-blockchain  |   'transactions': [{'amount': 1991.0,
karakai-blockchain  |                     'recipient': 'Karakai Oleksandr',
karakai-blockchain  |                     'sender': 'COINBASE'}]},
karakai-blockchain  |  {'curr_hash': '31d1f6c25182f3f7f089cd16722c54e6e845fa4eb374513e535e5a48c6f81e09',
karakai-blockchain  |   'index': 1,
karakai-blockchain  |   'nonce': 5593,
karakai-blockchain  |   'prev_hash': '6933b778b17bdf47c84b4e01c488d555bebe33eaa6aab02a70af14b01f4d9309',
karakai-blockchain  |   'timestamp': 1769599097,
karakai-blockchain  |   'transactions': [{'amount': 1991.0,
karakai-blockchain  |                     'recipient': 'Karakai Oleksandr',
karakai-blockchain  |                     'sender': 'COINBASE'}]},
karakai-blockchain  |  {'curr_hash': 'f7b05c745074b90f516a58d9943c4a4def2b7a8da6206f11c8052638e17e8209',
karakai-blockchain  |   'index': 2,
karakai-blockchain  |   'nonce': 90628,
karakai-blockchain  |   'prev_hash': '31d1f6c25182f3f7f089cd16722c54e6e845fa4eb374513e535e5a48c6f81e09',
karakai-blockchain  |   'timestamp': 1769599097,
karakai-blockchain  |   'transactions': [{'amount': 199.1,
karakai-blockchain  |                     'recipient': 'Karakai Oleksandr',
karakai-blockchain  |                     'sender': 'COINBASE'},
karakai-blockchain  |                    {'amount': 13.0,
karakai-blockchain  |                     'recipient': 'WalletA',
karakai-blockchain  |                     'sender': 'Karakai Oleksandr'},
karakai-blockchain  |                    {'amount': 13.0,
karakai-blockchain  |                     'recipient': 'WalletB',
karakai-blockchain  |                     'sender': 'Karakai Oleksandr'}]},
karakai-blockchain  |  {'curr_hash': 'd4ccda61c53c28a11ba529927252f4c9f54d13cf76cadbfb78d521783aceff09',
karakai-blockchain  |   'index': 3,
karakai-blockchain  |   'nonce': 50001,
karakai-blockchain  |   'prev_hash': 'f7b05c745074b90f516a58d9943c4a4def2b7a8da6206f11c8052638e17e8209',
karakai-blockchain  |   'timestamp': 1769599097,
karakai-blockchain  |   'transactions': [{'amount': 199.1,
karakai-blockchain  |                     'recipient': 'Karakai Oleksandr',
karakai-blockchain  |                     'sender': 'COINBASE'},
karakai-blockchain  |                    {'amount': 13.0,
karakai-blockchain  |                     'recipient': 'WalletB',
karakai-blockchain  |                     'sender': 'WalletA'},
karakai-blockchain  |                    {'amount': 13.0,
karakai-blockchain  |                     'recipient': 'WalletA',
karakai-blockchain  |                     'sender': 'WalletB'}]}]
karakai-blockchain  |
karakai-blockchain  | Final balances:
karakai-blockchain  | {'Karakai Oleksandr': 4354.200000000001, 'WalletA': 13.0, 'WalletB': 13.0}