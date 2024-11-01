# kpi_app/interfaces.py

from abc import ABC, abstractmethod

class DataSource(ABC):
    """Abstract base class for data sources."""
    
    @abstractmethod
    def read_data(self):
        """Reads data from the source."""
        pass

class DataSink(ABC):
    """Abstract base class for data sinks."""

    @abstractmethod
    def write_data(self, asset_id, attribute_id, timestamp, result):
        """Writes data to the sink."""
        pass

class ExpressionEvaluator(ABC):
    """Abstract base class for expression evaluators."""

    @abstractmethod
    def evaluate_expression(self, expression, attr_value):
        """Evaluates an expression with the given attribute value."""
        pass
