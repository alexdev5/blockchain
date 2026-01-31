# src/lab_2/server.py
from __future__ import annotations

from uuid import uuid4
from flask import Flask, jsonify, request

from blockchain import KarakaiOleksandrBlockchain
from config import MINER_ADDRESS

app = Flask(__name__)

# Унікальний ідентифікатор вузла
node_identifier = str(uuid4()).replace("-", "")

# Екземпляр блокчейну для цього вузла
blockchain = KarakaiOleksandrBlockchain()

@app.route("/transactions/new", methods=["POST"])
def new_transaction():
    values = request.get_json(silent=True) or {}

    required = ["sender", "recipient", "amount"]
    if not all(k in values for k in required):
        return jsonify({"error": "Missing values. Required: sender, recipient, amount"}), 400

    sender = str(values["sender"])
    recipient = str(values["recipient"])

    try:
        amount = float(values["amount"])
    except (TypeError, ValueError):
        return jsonify({"error": "amount must be a number"}), 400

    try:
        index = blockchain.KarakaiOleksandr_new_transaction(sender, recipient, amount)
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

    response = {
        "message": f"Transaction will be added to Block {index}",
        "sender": sender,
        "recipient": recipient,
        "amount": amount,
    }
    return jsonify(response), 201

@app.route("/mine", methods=["GET"])
def mine():
    meta = blockchain.KarakaiOleksandr_mine_block()

    # Дістанемо останній блок у “verbose” вигляді
    last_block_verbose = blockchain.KarakaiOleksandr_dump_chain_verbose()[-1]

    response = {
        "message": "New Block Forged",
        "node_id": node_identifier,
        "miner_address": MINER_ADDRESS,
        "meta": meta,
        "block": last_block_verbose,
        "balances": blockchain.KarakaiOleksandr_dump_balances(),
        "mempool": blockchain.KarakaiOleksandr_dump_mempool(),
    }
    return jsonify(response), 200

@app.route("/chain", methods=["GET"])
def full_chain():
    chain = blockchain.KarakaiOleksandr_dump_chain_verbose()
    response = {
        "chain": chain,
        "length": len(chain),
    }
    return jsonify(response), 200

def run_server() -> None:
    app.run(host="0.0.0.0", port=5000, debug=False)
