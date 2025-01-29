---

# j2c

A command-line tool to convert JSON files to CSV with the same filename.

## Installation

1. **Install Python**: Make sure you have Python installed on your system. You can download it from [python.org](https://www.python.org/downloads/).

2. **Clone this Repository**:
    ```bash
    git clone https://github.com/yourusername/j2c.git
    cd j2c
    ```

3. **Build and Install the Package**:
    Run the following commands to build and install the package using pip.
    ```bash
    python setup.py sdist bdist_wheel
    pip install .
    ```

## Usage

### Help Option

To see the help message explaining how to use the script, run:
```bash
python j2c.py --help
```
This will display the help message.

### Convert JSON to CSV

Specify the path to your JSON file using the `--json-file` option.
```bash
python j2c.py --json-file input.json
```

This will convert `input.json` to a CSV output file named `input.csv`.

## Example

1. **Get Help:**
   ```bash
   python j2c.py --help
   ```

2. **Specify JSON File and Run Conversion**:
    ```bash
    python j2c.py --json-file input.json
    ```
    
  This will convert `input.json` to `input.csv`.
