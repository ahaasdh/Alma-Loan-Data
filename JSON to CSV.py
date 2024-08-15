import pandas as pd
import json
import os

input_folder = 'input'
output_folder = 'output'

# Load JSON data from the completed loan file
completed_json_file = os.path.join(output_folder, 'all_completed_loan_data.json')
with open(completed_json_file, 'r') as file:
    completed_data = json.load(file)

# Load JSON data from the active loan file
active_json_file = os.path.join(output_folder, 'all_active_loan_data.json')
with open(active_json_file, 'r') as file:
    active_data = json.load(file)

# Function to extract loan data from JSON and return a list of dictionaries
def extract_loan_data(data):
    loan_list = []
    for item in data:
        mms_id = item['mms_id']
        loan_data = item['loan_data']
        for loan_item in loan_data:
            loan_list.append({
                'mms_id': mms_id,
                'loan_id': loan_item['loan_id'],
                'loan_date': pd.to_datetime(loan_item['loan_date']),
                'due_date': pd.to_datetime(loan_item['due_date'])
            })
    return loan_list

# Extract loan data from completed and active JSON files
completed_loan_data = extract_loan_data(completed_data)
active_loan_data = extract_loan_data(active_data)

# Combine the loan data from both files into a single list
all_loan_data = completed_loan_data + active_loan_data

# Create a DataFrame from the combined loan data
df = pd.DataFrame(all_loan_data)

# Sort the DataFrame by 'loan_date' if needed
df.sort_values(by='loan_date', inplace=True)

# Save the combined data to a CSV file
output_csv = os.path.join(output_folder, 'combined_loan_data.csv')
df.to_csv(output_csv, index=False)

print(f"Combined loan data exported to {output_csv}")