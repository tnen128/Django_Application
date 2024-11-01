# kpi_app/data_sinks.py

from kpi_app.models.models import EvaluationLog
from .interfaces import DataSink

class DatabaseDataSink(DataSink):
    """Data sink that writes processed data to the database."""

    def write_data(self, asset_id, attribute_id, timestamp, result):
        """Writes evaluation results to the EvaluationLog table."""
        EvaluationLog.objects.create(
            asset_id=asset_id,
            attribute_id=attribute_id,
            timestamp=timestamp,
            result=result
        )
