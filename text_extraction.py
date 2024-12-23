import re

def extract_information(file_path):
    # Open the text file and read its contents
    with open(file_path, 'r', encoding='utf-8') as file:
        data = file.read()
    
    # Extract account details using regular expressions
    account_details = {
        "Account Name": re.search(r'Account Name\s+:\s+(.+)', data),
        "Address": re.search(r'Address\s+:\s+(.+)', data),
        "Account Number": re.search(r'Account Number\s+:\s+(\d+)', data),
        "Branch": re.search(r'Branch\s+:\s+(.+)', data),
        "Interest Rate": re.search(r'Interest Rate\(% p.a.\)\s+:\s+([\d.]+)', data),
        "Balance as on": re.search(r'Balance as on\s+([\d\w\s]+):\s+([\d,.]+)', data)
    }
    
    # Process the matches to clean up and format
    account_details = {key: match.group(1).strip() if match else None for key, match in account_details.items()}
    
    # Extract transactions
    transaction_pattern = re.compile(
        r'(\d{1,2} \w{3} \d{4})\s+.*?\s+([\w\s/-]+)\s+([\d,]+\.?\d*)?\s+([\d,]+\.?\d*)?\s+([\d,]+\.?\d*)'
    )
    transactions = []
    
    for match in transaction_pattern.finditer(data):
        transactions.append({
            "Date": match.group(1),
            "Description": match.group(2).strip(),
            "Debit": match.group(3).replace(',', '') if match.group(3) else None,
            "Credit": match.group(4).replace(',', '') if match.group(4) else None,
            "Balance": match.group(5).replace(',', '') if match.group(5) else None
        })
    
    return account_details, transactions

def main():
    file_path = r"C:\Users\sanjay\Downloads\sanjay\iit-medrass\extracted_text.txt"  # Corrected input
    account_details, transactions = extract_information(file_path)
    
    print("Account Details:")
    for key, value in account_details.items():
        print(f"{key}: {value}")
    
    print("\nTransactions:")
    for txn in transactions:
        print(txn)

if __name__ == "__main__":
    main()