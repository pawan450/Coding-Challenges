import argparse
from utils.file_operations import load_spec, generate_fixed_width_file, parse_fixed_width_file
from utils.data_generation import generate_sample_data
import os

def main(num_records):
    # Use default values for spec file and output directory
    spec_file = 'spec.json'
    output_dir = 'data'
    
    # Load specification from spec.json
    spec = load_spec(spec_file)
    
    # Generate sample data using Faker
    data = generate_sample_data(spec, num_records=num_records)
    
    # Ensure the output directory exists
    os.makedirs(output_dir, exist_ok=True)
    
    # File paths
    fixed_width_file = os.path.join(output_dir, 'output_fixed_width.txt')
    parsed_csv_file = os.path.join(output_dir, 'output_parsed.csv')
    
    # Generate fixed width file
    generate_fixed_width_file(spec, data, fixed_width_file)
    
    # Parse fixed width file to CSV
    parse_fixed_width_file(spec, fixed_width_file, parsed_csv_file)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate and parse fixed-width files.")
    parser.add_argument('--num-records', type=int, default=10, help="Number of records to generate")
    
    args = parser.parse_args()
    main(args.num_records)
