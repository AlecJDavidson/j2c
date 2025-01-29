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

def format_value(value, formatter=None):
    if formatter and callable(formatter):
        value = formatter(value)
    elif isinstance(value, datetime):
        value = value.isoformat()
    elif isinstance(value, list):
        # Decide whether to join the list into a string or keep it as JSON
        # For now, let's join the list into a string with comma separation
        value = ', '.join(map(str, value))
    return str(value)

def json_to_csv(json_file_path, csv_file_path, delimiter=',', custom_formatters=None):
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
        writer = csv.DictWriter(
            csv_file,
            fieldnames=headers,
            delimiter=delimiter,
            quoting=csv.QUOTE_MINIMAL
        )
        writer.writeheader()
        
        for flat_item in flattened_data:
            formatted_flat_item = {k: format_value(v, custom_formatters.get(k)) for k, v in flat_item.items()}
            writer.writerow(formatted_flat_item)

def main():
    parser = argparse.ArgumentParser(description="Convert JSON to CSV")
    parser.add_argument('--json-file', type=str, required=True,
                        help='Path to the input JSON file')
    parser.add_argument('--csv-file', type=str, default=None,
                        help='Path to the output CSV file (default: same as JSON but with .csv extension)')
    parser.add_argument('--delimiter', type=str, default=',',
                        help='CSV delimiter (default: comma)')
    parser.add_argument('--array-as-string', action='store_true',
                        help='Keep arrays as JSON strings instead of joining them into a string')
    parser.add_argument('--custom-formatter', nargs='+',
                        help='Specify custom formatters for specific fields (e.g., --custom-formatter "field:formatter_function")')

    args = parser.parse_args()

    json_file_path = args.json_file
    csv_file_path = args.csv_file or os.path.splitext(json_file_path)[0] + '.csv'
    delimiter = args.delimiter

    # Decide how to handle arrays based on the --array-as-string flag
    if args.array_as_string:
        custom_formatters = {'list': lambda x: json.dumps(x)}
    else:
        custom_formatters = {}

    # Parse custom formatters from command line arguments
    custom_formatters = {}
    for formatter in args.custom_formatter or []:
        field, func_str = formatter.split(':')
        if field and func_str:
            try:
                custom_formatters[field] = lambda x: eval(func_str)
            except Exception as e:
                print(f"Invalid custom formatter {formatter}: {e}")

    json_to_csv(json_file_path, csv_file_path, delimiter=delimiter, custom_formatters=custom_formatters)

if __name__ == "__main__":
    main()
