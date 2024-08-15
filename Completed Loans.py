import requests
import json
import csv
import os

# Set your base URL for the Alma API, define input and output folders, and define CSV file
base_url = 'https://api-na.hosted.exlibrisgroup.com/almaws/v1'
input_folder = 'input'
csv_file = os.path.join(input_folder, "titles.csv")
output_folder = 'output'
os.makedirs(output_folder, exist_ok=True)

def get_api_key():
    api_key_file = os.path.join(input_folder, 'api_key.txt')
    with open(api_key_file, 'r') as file:
        return file.read().strip()  # Return the API key

def get_loan_data(api_key, mms_id):
    # Resource URL for loans endpoint
    resource_url = f"{base_url}/bibs/{mms_id}/loans"
    
    # Set parameters for the API call
    params = {
        'apikey': api_key,
        'format': 'json',
        'loan_status': 'Complete',
        'order_by': 'due_date'
        }
    
    try:
        # Make the API call
        response = requests.get(resource_url, params=params)
        response.raise_for_status()  # Check for any HTTP errors
        
        # Parse the response as JSON
        data = response.json()
        
        # Check if 'item_loan' key is present in the response
        if 'item_loan' in data:
            # Return the loan data
            return data['item_loan']
        else:
            print(f"No loan data found for book with MMS ID {mms_id}.")
            return None
    
    except requests.exceptions.RequestException as e:
        print(f"Error making API request: {e}")
        return None

all_loan_data = []

# Get the API key before processing the CSV
api_key = get_api_key()

# Read MMS IDs from the CSV file
with open(csv_file, 'r', encoding='utf-8-sig', newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    print(f"CSV file column names: {reader.fieldnames}")  # Debug print statement
    
    # Verify if the specified column name exists in the CSV header
    mms_id_column = 'MMS Id'  # Replace 'MMS_ID_COLUMN_NAME' with the actual column name
    if mms_id_column not in reader.fieldnames:
        print(f"Error: Column '{mms_id_column}' not found in CSV header.")
    else:
        for row in reader:
            mms_id = row[mms_id_column]
            loan_data = get_loan_data(api_key, mms_id)
            
            if loan_data:
                # Process the loan data for each book as needed
                print(f"Loan data for book with MMS ID {mms_id}:")
                print(loan_data)
                
                all_loan_data.append({
                    'mms_id': mms_id,
                    'loan_data': loan_data
                })
            else:
                print(f"Failed to retrieve loan data for book with MMS ID {mms_id}.")

if all_loan_data:
    output_file = os.path.join(output_folder, 'all_completed_loan_data.json')
    with open(output_file, 'w', encoding='utf-8') as jsonfile:
        json.dump(all_loan_data, jsonfile, indent=2)

    print(f"All loan data exported to {output_file}")
else:
    print("No loan data found or retrieval failed for all books.")
