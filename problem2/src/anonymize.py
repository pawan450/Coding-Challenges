import logging
import time
from pyspark.sql.functions import sha2, col

logger = logging.getLogger(__name__)

class Anonymizer:
    def __init__(self, spark):
        self.spark = spark

    def anonymize_and_measure(self, input_path):
        try:
            logger.info("Reading CSV file from distributed storage...")
            df = self.spark.read.csv(input_path, header=True, inferSchema=True)

            # Start timing
            start_time = time.time()

            # Anonymize the specified columns by hashing
            logger.info("Anonymizing data...")
            df_anonymized = df.withColumn("first_name", sha2(col("first_name"), 256)) \
                              .withColumn("last_name", sha2(col("last_name"), 256)) \
                              .withColumn("address", sha2(col("address"), 256))

            # Trigger the computation by performing a count operation
            logger.info("Counting anonymized data...")
            
            df_anonymized.count()

            # Stop timing
            end_time = time.time()

            return end_time - start_time

        except Exception as e:
            logger.error("An error occurred during anonymization.", exc_info=e)
            raise
