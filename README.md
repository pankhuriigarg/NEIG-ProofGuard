> ⚠️ This project was developed for India Innovates 2026 by Team ProofGuard. 
> Original work by Pankhuri Garg, IMS Engineering College, Ghaziabad.
> Submission Date: March 2026.

# NEIG - National Evidence Integrity Grid

A blockchain-based digital evidence integrity verification system 
that ensures tamper-proof evidence management for the Indian judiciary.

## Problem
Digital evidence tampering is a critical issue in India's justice 
system. Existing systems rely on centralized storage with no 
tamper-detection mechanism.

## Solution
NEIG uses SHA-256 cryptographic hashing + Ethereum blockchain + 
Zero Knowledge Proofs to ensure evidence authenticity.

## Tech Stack
- Python + Flask
- SHA-256 (hashlib)
- Ethereum Blockchain (Ganache + Web3.py)
- Solidity Smart Contract
- Circom + snarkjs (ZKP) — in progress
- HTML/CSS

## Features
- Evidence upload + hash generation
- Blockchain storage with transaction hash
- Court verification portal
- Tamper detection — Authentic ✅ or Tampered ❌

## How to Run
1. Start Ganache: `ganache`
2. Deploy contract: `python backend/deploy.py`
3. Run server: `python backend/app.py`
4. Open: `http://127.0.0.1:5000`

## Status
🚧 In Development — India Innovates 2026

## Team
ProofGuard — India Innovates 2026
