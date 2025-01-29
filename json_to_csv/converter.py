import json
import csv
import argparse
import os
from datetime import datetime

def flatten(data, parent_key='', sep='.'):
    items = {}
    if isinstance(data, dict):
        for k, v in data.items():
            new_key = f"{parent_key}{sep}{k}" if parent_key else k
            if isinstance(v, (dict, list)):
                items.update(flatten(v, new_key, sep=sep))
            else:
                items[new_key] = v
    elif isinstance(data, list):
        for i, item in enumerate(data):
            items.update(flatten(item, f"{parent_key}{sep}{i}", sep=sep))
    return items

def ensure_list_of_dicts(data):
    if isinstance(data, dict):
        return [data]
    elif not isinstance(data, list) or not all(isinstance(item, dict) for item in data):
        raise ValueError("JSON data must be an array of objects or a single object.")
    else:
        return data

def json_to_csv(json_file_path, csv_file_path):
    with open(json_file_path, 'r') as json_file:
        data = json.load(json_file)
    data = ensure_list_of_dicts(data)
    if not data:
        raise ValueError("JSON data must contain at least one object.")
    
    # Flatten all dictionaries to identify unique keys
    flattened_data = [flatten(item) for item in data]
    headers = set()
    for item in flattened_data:
        headers.update(item.keys())
    
    with open(csv_file_path, 'w', newline='', encoding='utf-8') as csv_file:
        csv_writer = csv.DictWriter(csv_file, fieldnames=sorted(headers), quoting=csv.QUOTE_MINIMAL)
        csv_writer.writeheader()
        
        for item in flattened_data:
            # Flatten and convert datetime objects to strings
            flat_item = flatten(item)
            for key, value in flat_item.items():
                if isinstance(value, datetime):
                    flat_item[key] = value.isoformat()
            csv_writer.writerow(flat_item)

def main():
    parser = argparse.ArgumentParser(description="Convert JSON to CSV")
    parser.add_argument('--json-file', type=str, required=True,
                        help='Path to the input JSON file')
    args = parser.parse_args()
    json_file_path = args.json_file
    base_name = os.path.splitext(os.path.basename(json_file_path))[0]
    csv_file_path = f"{base_name}.csv"
    try:
        json_to_csv(json_file_path, csv_file_path)
        print(f"JSON data has been successfully converted to {csv_file_path}")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
