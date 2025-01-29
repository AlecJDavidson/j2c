import os
import tempfile
import json
import csv

from json_to_csv.converter import json_to_csv, ensure_list_of_dicts

def test_json_to_csv():
    # Create a temporary JSON file with sample data
    temp_dir = tempfile.mkdtemp()
    temp_json_file = os.path.join(temp_dir, 'test.json')
    
    sample_data = {
      "model_name": "Gundam RX-78-2",
      "series": "Mobile Suit Gundam",
      "manufacturer": "Universal Century Federation",
      "pilot": "Amuro Ray",
      "era": "UC 0079"
    },
    
    with open(temp_json_file, 'w') as f:
        json.dump([sample_data], f)
    
    # Create a temporary CSV file path
    temp_csv_file = os.path.join(temp_dir, 'test.csv')
    
    # Call the function to convert JSON to CSV
    json_to_csv(temp_json_file, csv_file_path=temp_csv_file)
    
    # Verify that the CSV file was created and contains the correct data
    assert os.path.exists(temp_csv_file), "CSV file not created"
    
    with open(temp_csv_file, 'r') as f:
        reader = csv.DictReader(f)
        rows = list(reader)
        
        assert len(rows) == 1, "One row should be present in CSV"
        assert rows[0] == sample_data, "Data in CSV is incorrect"

# Run the test
if __name__ == "__main__":
    import unittest
    unittest.main()
