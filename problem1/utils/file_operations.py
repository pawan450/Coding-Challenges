import json
import csv

def load_spec(spec_file):
    """
    Load the specification from a JSON file.

    Parameters:
    spec_file (str): Path to the JSON file containing the specification.

    Returns:
    dict: The specification loaded from the JSON file.
    """
    with open(spec_file, 'r') as file:
        spec = json.load(file)
    return spec

def generate_fixed_width_file(spec, data, output_file):
    """
    Generate a fixed-width file based on the specification and provided data.

    Parameters:
    spec (dict): The specification dictionary defining column widths and encoding.
    data (list of lists): The data to write into the fixed-width file.
    output_file (str): The path to the output fixed-width file.
    """
    with open(output_file, 'w', encoding=spec['FixedWidthEncoding']) as fw_file:
        # Write the header row if specified in the spec
        if spec['IncludeHeader'] == 'True':
            header = ''.join([col.ljust(int(width)) for col, width in zip(spec['ColumnNames'], spec['Offsets'])])
            fw_file.write(header + '\n')
        
        # Write each row of data in fixed-width format
        for row in data:
            fixed_width_row = ''.join([str(value).ljust(int(width)) for value, width in zip(row, spec['Offsets'])])
            fw_file.write(fixed_width_row + '\n')

def parse_fixed_width_file(spec, input_file, output_file):
    """
    Parse a fixed-width file and convert it into a CSV file.

    Parameters:
    spec (dict): The specification dictionary defining column widths and encoding.
    input_file (str): The path to the input fixed-width file.
    output_file (str): The path to the output CSV file.
    """
    offsets = list(map(int, spec['Offsets']))  # Convert string offsets to integers
    with open(input_file, 'r', encoding=spec['FixedWidthEncoding']) as fw_file, open(output_file, 'w', newline='', encoding=spec['DelimitedEncoding']) as csv_file:
        csv_writer = csv.writer(csv_file)
        
        # Read and write the header row if specified in the spec
        if spec['IncludeHeader'] == 'True':
            header = fw_file.readline()  # Read the first line as the header
            header_values = [header[sum(offsets[:i]):sum(offsets[:i + 1])].strip() for i in range(len(offsets))]
            csv_writer.writerow(header_values)
        
        # Read each line of the fixed-width file, parse it according to offsets, and write to CSV
        for line in fw_file:
            row = [line[sum(offsets[:i]):sum(offsets[:i + 1])].strip() for i in range(len(offsets))]
            csv_writer.writerow(row)
