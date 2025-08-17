# Blockchain-Based KYC with Zero-Knowledge Proofs (ZKP) and IPFS

This project leverages blockchain technology and Zero-Knowledge Proofs (ZKPs) to improve KYC (Know Your Customer) processes. It provides enhanced security, lowers costs, and maintains data privacy by allowing identity verification without exposing sensitive personal details. IPFS (InterPlanetary File System) is used for secure and decentralized data storage.

---

## Features

- **Privacy-Preserving KYC**: Identity verification using ZKPs.
- **Decentralized Storage**: Using IPFS for secure file management.
- **Cost-Effective**: Blockchain reduces the cost of KYC operations.

---

## Prerequisites

Ensure you have the following installed:

- **Ganache**: For local Ethereum blockchain simulation.
- **Truffle**: To compile, deploy, and manage smart contracts.
- **Python**: To run the Flask backend.
- **Node.js and npm**: Required for Truffle and Ganache.

---

## Setup Guide

### Step 1: Create a `.env` File

1. Navigate to the `FrontEnd` directory.
2. Create a `.env` file and add the following content:

   ```plaintext
   PINATA_API_KEY='your_pinata_key'
   PINATA_SECRET_API_KEY='your_pinata_secret_key'
   KYC_ADDRESS='address_of_the_deployed_smart_contract_in_ganache'
   JWT='your_pinata_jwt_token'

Or use IPFS Desktop application, which is what was used here.


### Step 2: Start your local Ganache Application

1. Launch `Ganache` and click on `QuickStart` (Ethereum).
2. A local blockchain will be initialized for testing purposes.
3. Use the `Settings` menu to make adjustments if necessary.


### Step 3: Deploying the Smart Contract

1. Open your terminal or command prompt.
2. Navigate to the FrontEnd directory and run the following commands:

```bash
   truffle init
   truffle compile
   truffle migrate --network development
```


3. Once deployed, you will see the contract address in the output. Update the `KYC_ADDRESS` field in your .`env` file with this address.


### Step 4: Run the Flask Application

1. Navigate to the FrontEnd directory using the terminal.
2. Run the Flask app with the command:

```bash 
python app.py
```

3. Your Flask application should now be running. You can test the KYC functionalities from here.



