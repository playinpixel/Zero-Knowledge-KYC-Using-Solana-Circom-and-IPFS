import sys
from kyc import convertDataToJSON, pinJSONtoIPFS, initContract, w3
from pprint import pprint
from datetime import datetime
from zkp import ZKProof

kyccontract = initContract()
zkp = ZKProof()

def calculate_age(dob):
    birth_date = datetime.strptime(dob, "%d/%m/%Y")
    today = datetime.today()
    age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
    return age


def createkycReport():
    first_name = input("First Name: ")
    last_name = input("Last Name: ")
    dob = input("Date of birth dd/mm/yyyy: ")
    age = calculate_age(dob)
    email = input("Email: ")
    nationality = input("Nationality: ")
    occupation = input("Occupation: ")

    user_id = input("User ID: ")

    print("Age is ", age)

    zkp_proof = zkp.generate_proof(age)
    print("ZKP Proof:", zkp_proof)
    
    json_data = convertDataToJSON(first_name, last_name, dob, age, email, nationality, occupation, zkp_proof)
    report_uri = pinJSONtoIPFS(json_data)

    return user_id, report_uri, zkp_proof


def kycreport(user_id, report_uri, zkp_proof):
    tx_hash = kyccontract.functions.registerKYC(user_id, report_uri, zkp_proof).transact(
        {"from": user_id}
    )
    receipt = w3.eth.wait_for_transaction_receipt(tx_hash)

    return receipt

def kycupdate(user_id, report_uri):
    tx_hash = kyccontract.functions.updateKYC(user_id, report_uri).transact(
        {"from": user_id}
    )
    receipt = w3.eth.wait_for_transaction_receipt(tx_hash)

    return receipt

         
def main():
    if sys.argv[1] == "report":
        user_id, report_uri, zkp_proof  = createkycReport()

        receipt = kycreport(user_id, report_uri, zkp_proof)

        pprint(receipt)
        print("Report IPFS Hash:", report_uri)
        print("User ID:", user_id)
        print("ZKP Proof:", zkp_proof)


    if sys.argv[1] == "update":
        user_id, report_uri, zkp_proof= createkycReport()

        receipt = kycupdate(user_id, report_uri)

        pprint(receipt)
        print("Report IPFS Hash:", report_uri)
        print("User ID:", user_id)
        print("ZKP Proof:", zkp_proof)

main()