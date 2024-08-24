class PartitionSizeCalculator:
    def __init__(self, executor_memory, num_executors, fraction=0.1):
        self.executor_memory = executor_memory
        self.num_executors = num_executors
        self.fraction = fraction

    def calculate(self):
        # Convert executor_memory to bytes
        memory_unit = self.executor_memory[-1].lower()
        memory_value = int(self.executor_memory[:-1])

        if memory_unit == 'g':
            total_memory_bytes = memory_value * 1024 * 1024 * 1024  # Convert GB to bytes
        elif memory_unit == 'm':
            total_memory_bytes = memory_value * 1024 * 1024  # Convert MB to bytes
        else:
            raise ValueError("Unsupported memory unit. Use 'g' for GB or 'm' for MB.")

        # Calculate total available memory across all executors
        total_memory = total_memory_bytes * self.num_executors

        # Calculate partition size as a fraction of total memory
        partition_size_bytes = total_memory * self.fraction

        # Convert partition size to MB or GB as needed
        if partition_size_bytes >= 1024 * 1024 * 1024:
            partition_size = partition_size_bytes / (1024 * 1024 * 1024)
            return f"{int(partition_size)}GB"
        else:
            partition_size = partition_size_bytes / (1024 * 1024)
            return f"{int(partition_size)}MB"
