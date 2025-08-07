from flask import Flask, render_template, request, flash, redirect, url_for, jsonify
import requests
# MODIFIED: Added initContract for blockchain interaction and Web3
from kyc import convertDataToJSON, add_json_to_local_ipfs, initContract
from web3 import Web3
from datetime import datetime, timedelta
from zkp import ZKProof
import json
import os

# Initialize Flask app
app = Flask(__name__)
app.secret_key = 'your_secret_key'

# MODIFIED: Initialize Web3 to connect to Ganache
w3 = Web3(Web3.HTTPProvider('http://127.0.0.1:7545'))

zkp = ZKProof()

# REMOVED: These are no longer needed as we are using the blockchain

# Helper function to calculate age
def calculate_age(dob):
    birth_date = datetime.strptime(dob, "%d/%m/%Y")
    today = datetime.today()
    age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
    return age

# Landing page
@app.route("/landing", methods=["GET"])
def landing():
    return render_template("landing_page.html")

# Route for KYC Registration
@app.route("/register", methods=["POST"])
def kyc_register():
    first_name = request.form.get("first_name")
    last_name = request.form.get("last_name")
    dob = request.form.get("dob")
    email = request.form.get("email")
    nationality = request.form.get("nationality")
    occupation = request.form.get("occupation")
    user_id = request.form.get("user_id")

    age = calculate_age(dob)
    zkp_proof = zkp.generate_proof(age)
    expiry_date = datetime.now() + timedelta(days=365)
    end_date_timestamp = int(expiry_date.timestamp())
    json_data = convertDataToJSON(first_name, last_name, dob, age, email, nationality, occupation, zkp_proof, end_date_timestamp)
    report_uri = add_json_to_local_ipfs(json_data)
    
    try:
        kyc_contract = initContract()
        contract_owner = w3.eth.accounts[0]
        user_id_checksum = w3.to_checksum_address(user_id)

        tx_hash = kyc_contract.functions.storeKYC(
            user_id_checksum,
            report_uri,
            age
        ).transact({'from': contract_owner, 'gas': 500000})
        
        w3.eth.wait_for_transaction_receipt(tx_hash)
        flash("KYC Report Registered Successfully on the Blockchain", "success")
    except Exception as e:
        flash(f"Error interacting with blockchain: {e}", "danger")

    return render_template("kyc_result.html", receipt=None, report_uri=report_uri, user_id=user_id, zkp_proof=zkp_proof)

# Route for KYC Update
@app.route("/update", methods=["POST"])
def kyc_update():
    first_name = request.form.get("first_name")
    last_name = request.form.get("last_name")
    dob = request.form.get("dob")
    email = request.form.get("email")
    nationality = request.form.get("nationality")
    occupation = request.form.get("occupation")
    user_id = request.form.get("user_id")

    age = calculate_age(dob)
    zkp_proof = zkp.generate_proof(age)
    expiry_date = datetime.now() + timedelta(days=365)
    end_date_timestamp = int(expiry_date.timestamp())
    json_data = convertDataToJSON(first_name, last_name, dob, age, email, nationality, occupation, zkp_proof, end_date_timestamp)
    report_uri = add_json_to_local_ipfs(json_data)

    try:
        kyc_contract = initContract()
        contract_owner = w3.eth.accounts[0]
        user_id_checksum = w3.to_checksum_address(user_id)

        tx_hash = kyc_contract.functions.storeKYC(
            user_id_checksum,
            report_uri,
            age
        ).transact({'from': contract_owner, 'gas': 500000})

        w3.eth.wait_for_transaction_receipt(tx_hash)
        flash("KYC Report Updated Successfully on the Blockchain", "success")
    except Exception as e:
        flash(f"Error interacting with blockchain: {e}", "danger")
        
    return render_template("kyc_updation_result.html", receipt=None, report_uri=report_uri, user_id=user_id, zkp_proof=zkp_proof)

# Main form
@app.route("/", methods=["GET"])
def form():
    return render_template("kyc_form.html")

# Admin login routing
@app.route("/admin_login", methods=["POST"])
def admin_login():
    password = request.form.get("password")
    role = request.form.get("role")

    if role == "admin" and password == "admin123":
        return redirect(url_for("admin_page"))
    elif role == "bank" and password == "bank_page":
        return redirect(url_for("bank_page"))

    flash("Incorrect password. Please try again.", "danger")
    return redirect(url_for("form"))

# Admin dashboard
@app.route("/admin_page")
def admin_page():
    return render_template("admin_page.html")

# Admin functionality - AJAX
@app.route("/admin", methods=["POST"])
def admin():
    try:
        data = request.form or request.get_json(force=True)
        user_id = data.get("user_id")
        
        if data.get("get_client_info") or data.get("check_validity"):
            kyc_contract = initContract()
            user_id_checksum = w3.to_checksum_address(user_id)
            user_data = kyc_contract.functions.users(user_id_checksum).call()
            report_uri = user_data[0]

            if not report_uri:
                return jsonify({"error": "No record found for this User ID."})
            
            gateway_url = f"http://127.0.0.1:8080/ipfs/{report_uri}"
            try:
                response = requests.get(gateway_url, timeout=10)
                response.raise_for_status()
                kyc_data = response.json()
            except Exception as e:
                kyc_data = {}
            
            return jsonify({
                "user_id": user_id,
                "report_uri": report_uri,
                "used": kyc_data.get("used", False),
                "end_date": kyc_data.get("end_date", 0),
                "zkp_proof": kyc_data.get("zkp_proof", "")
            })
            
        elif data.get("get_client_count"):
            return jsonify({"client_count": "N/A on-chain"})
            
        else:
            return jsonify({"error": "Invalid request."})
            
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Bank page
@app.route("/bank_page")
def bank_page():
    return render_template("bank_page.html")

# Bank verify-age handler
@app.route("/bank", methods=["POST"])
def bank():
    try:
        data = request.get_json(force=True)
        user_id = data.get("user_id")

        kyc_contract = initContract()
        user_id_checksum = w3.to_checksum_address(user_id)
        user_data = kyc_contract.functions.users(user_id_checksum).call()
        report_uri = user_data[0]

        if not report_uri:
            return jsonify({"error": "No record found for this User ID."})
        
        # Fetching the full document from IPFS to get the ZKP
        gateway_url = f"http://127.0.0.1:8080/ipfs/{report_uri}"
        response = requests.get(gateway_url, timeout=10)
        response.raise_for_status()
        kyc_data = response.json()
        
        # --- MODIFIED: Verify the ZKP instead of checking age directly ---
        zkp_proof_data = kyc_data.get("zkp_proof")
        age_verification = zkp.verify_proof(zkp_proof_data)
        # -----------------------------------------------------------------
            
        return jsonify({"age_verification": age_verification, "kyc_data": kyc_data})
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/get_kyc_document/<ipfs_hash>", methods=["GET"])
def get_kyc_document(ipfs_hash):
    try:
        gateway_url = f"http://127.0.0.1:8080/ipfs/{ipfs_hash}"
        response = requests.get(gateway_url, timeout=10)
        response.raise_for_status()
        return jsonify(response.json())
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Run the app
if __name__ == "__main__":
    app.run(debug=True)