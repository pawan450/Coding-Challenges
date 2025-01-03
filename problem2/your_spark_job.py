import time
import argparse
import logging
from pyspark.sql import SparkSession
from pyspark.sql.functions import sha2, col

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def calculate_dynamic_partition_size(executor_memory, num_executors, fraction=0.1):
    # Convert executor_memory to bytes
    memory_unit = executor_memory[-1].lower()
    memory_value = int(executor_memory[:-1])

    if memory_unit == 'g':
        total_memory_bytes = memory_value * 1024 * 1024 * 1024  # Convert GB to bytes
    elif memory_unit == 'm':
        total_memory_bytes = memory_value * 1024 * 1024  # Convert MB to bytes
    else:
        raise ValueError("Unsupported memory unit. Use 'g' for GB or 'm' for MB.")

    # Calculate total available memory across all executors
    total_memory = total_memory_bytes * num_executors

    # Calculate partition size as a fraction of total memory
    partition_size_bytes = total_memory * fraction

    # Convert partition size to MB or GB as needed
    if partition_size_bytes >= 1024 * 1024 * 1024:
        partition_size = partition_size_bytes / (1024 * 1024 * 1024)
        return f"{int(partition_size)}GB"
    else:
        partition_size = partition_size_bytes / (1024 * 1024)
        return f"{int(partition_size)}MB"

def anonymize_csv_and_measure_time(executor_memory, executor_cores, driver_memory, num_executors, min_executors, max_executors, input_path):
    spark = None
    try:
        logger.info("Initializing SparkSession...")
        # Dynamically calculate max_partition_bytes
        max_partition_bytes = calculate_dynamic_partition_size(executor_memory, num_executors)

        # Initialize Spark Session
        spark = SparkSession.builder \
            .appName("Anonymize CSV with Dynamic Partition Size") \
            .config("spark.ui.port", "4050") \
            .config("spark.executor.memory", executor_memory) \
            .config("spark.executor.cores", executor_cores) \
            .config("spark.driver.memory", driver_memory) \
            .config("spark.sql.adaptive.enabled", "true") \
            .config("spark.executor.instances", num_executors) \
            .config("spark.sql.files.maxPartitionBytes", max_partition_bytes) \
            .config("spark.dynamicAllocation.enabled", "true") \
            .config("spark.dynamicAllocation.minExecutors", min_executors) \
            .config("spark.dynamicAllocation.maxExecutors", max_executors) \
            .getOrCreate()

        logger.info("SparkSession initialized successfully.")

        # Read CSV
        logger.info("Reading CSV file from distributed storage...")
        df = spark.read.csv(input_path, header=True, inferSchema=True)

        # Start timing
        start_time = time.time()

        # Anonymize the specified columns by hashing without caching
        logger.info("Anonymizing data...")
        df_anonymized = df.withColumn("first_name", sha2(col("first_name"), 256)) \
                          .withColumn("last_name", sha2(col("last_name"), 256)) \
                          .withColumn("address", sha2(col("address"), 256))

        # Trigger the computation by performing a count operation
        logger.info("Counting anonymized data...")
        df_anonymized.count()

        # Stop timing
        end_time = time.time()

        logger.info("Anonymization completed successfully.")
        return end_time - start_time
    except Exception as e:
        logger.error("An error occurred during Spark job execution.", exc_info=e)
        raise
    finally:
        if spark:
            logger.info("Stopping SparkSession...")
            spark.stop()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Anonymize CSV data with Spark and measure execution time.')
    parser.add_argument('--executor_memory', type=str, required=True, help='Memory per executor (e.g., 1G)')
    parser.add_argument('--executor_cores', type=int, required=True, help='Number of cores per executor')
    parser.add_argument('--driver_memory', type=str, required=True, help='Memory for driver (e.g., 1G)')
    parser.add_argument('--num_executors', type=int, required=True, help='Number of executors')
    parser.add_argument('--min_executors', type=int, required=True, help='Minimum number of executors')
    parser.add_argument('--max_executors', type=int, required=True, help='Maximum number of executors')
    parser.add_argument('--input_path', type=str, required=True, help='Path to the input CSV file in distributed storage (e.g., HDFS, S3)')

    args = parser.parse_args()

    # Measure execution time for the given configuration
    time_taken = anonymize_csv_and_measure_time(args.executor_memory, args.executor_cores, args.driver_memory, args.num_executors, args.min_executors, args.max_executors, args.input_path)
    print(f"Time taken for anonymization: {time_taken} seconds")
