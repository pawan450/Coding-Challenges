## Project Description

This project is designed to anonymize a large CSV file stored in a distributed storage system (such as HDFS) using Apache Spark. The project pulls a 2GB CSV file from HDFS, anonymizes the `first_name`, `last_name`, and `address` columns by hashing, and measures the execution time for the anonymization process. The Spark job is dynamically configured with partition sizes based on available memory.

### Prerequisites

- Docker and Docker Compose installed on your machine.
- A 2GB CSV file stored in HDFS or a compatible distributed file system.
- Python 3.8 or later installed locally.

### Clone the Repository

Clone the repository to your local machine:

git clone https://github.com/pawan450/Coding-Challenges.git

cd problem2

## Start the Hadoop and Spark services:

docker-compose up -d

## Verify that the services are running:
Hadoop Namenode: http://localhost:9870
Spark Master: http://localhost:8080

## Build the Docker image for the Spark job:

docker build -t spark-anonymization .

## Submit the Spark Job
Run the Spark job to anonymize the CSV data and measure the execution time. Make sure to replace the input_path with the actual path to your 2GB CSV file in HDFS:

## bash command

docker run --network=spark-network problem2 \
    --executor_memory 2G \
    --executor_cores 2 \
    --driver_memory 2G \
    --num_executors 2 \
    --min_executors 2 \
    --max_executors 6 \
    --input_path hdfs://hadoop-namenode:9000/user/pawan/sample_data.csv