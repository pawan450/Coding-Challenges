import argparse
import logging
import time
from anonymize import Anonymizer
from partition_size_calculator import PartitionSizeCalculator
from pyspark.sql import SparkSession

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def run_anonymization(executor_memory, executor_cores, driver_memory, num_executors, min_executors, max_executors, input_path):
    spark = None
    try:
        logger.info("Initializing SparkSession...")

        # Calculate dynamic partition size
        partition_calculator = PartitionSizeCalculator(executor_memory, num_executors)
        max_partition_bytes = partition_calculator.calculate()

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

        # Anonymize the data and measure the time taken
        anonymizer = Anonymizer(spark)
        execution_time = anonymizer.anonymize_and_measure(input_path)

        logger.info(f"Anonymization completed successfully. Time taken: {execution_time:.2f} seconds")
        return execution_time

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

    # Run anonymization with the provided configuration
    run_anonymization(args.executor_memory, args.executor_cores, args.driver_memory, args.num_executors, args.min_executors, args.max_executors, args.input_path)
