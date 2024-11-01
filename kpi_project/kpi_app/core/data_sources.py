"""
Data source module for reading messages from files.
"""

import json
from .interfaces import DataSource

class FileDataSource(DataSource):
    """
    Reads data from a specified file.
    """

    def __init__(self, file_path):
        self.file_path = file_path

    def read_data(self):
        """
        Generator function to yield messages from the file.

        Yields:
            dict: Message data as dictionary.
        """
        with open(self.file_path, 'r', encoding='utf-8') as file:  # Specify encoding
            for line in file:
                if line.strip():  # Avoid processing empty lines
                    try:
                        yield json.loads(line.strip())
                    except json.JSONDecodeError:
                        print(f"Error decoding JSON: {line}")
