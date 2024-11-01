# kpi_app/management/commands/process_messages.py

import json
import time
from django.core.management.base import BaseCommand
from kpi_app.models.models import AssetKPI
from kpi_app.core.data_sources import FileDataSource
from kpi_app.core.data_sinks import DatabaseDataSink
from kpi_app.core.interpreter import CustomInterpreter

class Command(BaseCommand):
    help = "Process messages from a text file and evaluate KPIs, with 5-second intervals between each message."

    def add_arguments(self, parser):
        parser.add_argument('file_path', type=str, help="Path to the messages text file")

    def handle(self, *args, **options):
        # Initialize components
        file_path = options['file_path']
        data_source = FileDataSource(file_path)
        data_sink = DatabaseDataSink()
        interpreter = CustomInterpreter()

        # Process each message from the data source with a 5-second delay
        for message in data_source.read_data():
            asset_id = None
            attribute_id = None

            try:
                # Ensure that message is a dictionary with necessary fields
                if not isinstance(message, dict):
                    print("Skipping invalid message format. Expected JSON object.")
                    continue

                # Extract fields with error handling for missing keys
                asset_id = message.get('asset_id')
                attribute_id = message.get('attribute_id')
                timestamp = message.get('timestamp')
                value = message.get('value')

                # Check for null or missing values
                if not asset_id or not attribute_id or not timestamp or value is None:
                    print(f"Skipping message with missing fields: {message}")
                    continue

                # Retrieve the corresponding AssetKPI and KPI
                try:
                    asset_kpi = AssetKPI.objects.get(asset__asset_id=asset_id, attribute_id=attribute_id)
                except AssetKPI.DoesNotExist:
                    print(f"No AssetKPI found for asset_id: {asset_id} and attribute_id: {attribute_id}")
                    continue

                kpi = asset_kpi.kpi

                # Validate and process numeric value for arithmetic expressions
                if isinstance(value, str) and value.replace('.', '', 1).isdigit():
                    value = float(value)  # Convert numeric string to float
                elif not isinstance(value, (int, float)) and not kpi.expression.startswith("Regex("):
                    print(f"Invalid numeric value for KPI calculation: {value}")
                    continue

                # Evaluate the KPI expression using the custom interpreter
                result = interpreter.evaluate_expression(kpi.expression, value)

                # Write the result to the data sink (database)
                data_sink.write_data(asset_id, f"output_{attribute_id}", timestamp, result)
                print(f"Processed message for Asset ID: {asset_id}, Attribute: {attribute_id}, Result: {result}")

            except json.JSONDecodeError:
                print("Skipping invalid JSON format line.")
            except Exception as e:
                print(f"Unexpected error processing message for asset_id: {asset_id}, attribute_id: {attribute_id}: {e}")
            
            # Wait for 5 seconds before processing the next row
            time.sleep(5)
