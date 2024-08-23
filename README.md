# Fixed Width Parser

This project provides a simple utility to generate a fixed-width file based on a provided specification and parse it back into a CSV file.

## Project Structure

- `main.py`: The main entry point of the application.
- `spec.json`: The specification file that defines the structure of the fixed-width file.
- `data/`: Directory where generated fixed-width files and parsed CSV files are stored.
- `utils/`: Directory containing utility functions for file operations and data generation.
  - `file_operations.py`: Functions for loading specifications, generating fixed-width files, and parsing them into CSV files.
  - `data_generation.py`: Functions for generating sample data using the Faker library.
- `requirements.txt`: List of Python dependencies.
- `README.md`: Project documentation.

## Setup

1. Clone the repository.
2. Install dependencies using:

   ```bash
   pip install -r requirements.txt


## How to create a docker image

docker build -t problem1 .

## give number of records required
docker run --rm -v C:\Users\saiso\OneDrive\Documents\Problem1:/usr/src/app problem1 python main.py --num-records 1000 

