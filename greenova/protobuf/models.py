"""Django models with Protobuf integration for Greenova.

This module provides Django models that can serialize to/from Protocol Buffers
for efficient data transfer between backend and frontend.
"""

from django.db import models

from . import chart_data_pb2, greenova_data_pb2


class ProtoBufProject(models.Model):
    """Project model with Protobuf serialization support.

    This model can be serialized to protobuf format for efficient
    data transfer to frontend components.
    """

    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        app_label = "protobuf"
        db_table = "protobuf_project"

    def to_protobuf(self) -> greenova_data_pb2.Project:
        """Convert Django model to protobuf message."""
        proto_project = greenova_data_pb2.Project()
        proto_project.id = self.id
        proto_project.name = self.name
        proto_project.description = self.description
        proto_project.created_at = int(self.created_at.timestamp())
        proto_project.updated_at = int(self.updated_at.timestamp())
        proto_project.is_active = self.is_active
        return proto_project

    @classmethod
    def from_protobuf(
        cls, proto_project: greenova_data_pb2.Project
    ) -> "ProtoBufProject":
        """Create Django model from protobuf message."""
        from datetime import datetime

        return cls(
            id=proto_project.id,
            name=proto_project.name,
            description=proto_project.description,
            created_at=datetime.fromtimestamp(proto_project.created_at),
            updated_at=datetime.fromtimestamp(proto_project.updated_at),
            is_active=proto_project.is_active,
        )


class ProtoBufObligation(models.Model):
    """Obligation model with Protobuf serialization support.

    Environmental obligations that can be efficiently serialized
    for frontend display and API responses.
    """

    project = models.ForeignKey(
        ProtoBufProject, on_delete=models.CASCADE, related_name="obligations"
    )
    title = models.CharField(max_length=300)
    description = models.TextField()
    due_date = models.DateField()
    status = models.CharField(
        max_length=50,
        choices=[
            ("pending", "Pending"),
            ("in_progress", "In Progress"),
            ("completed", "Completed"),
            ("overdue", "Overdue"),
        ],
    )
    priority = models.CharField(
        max_length=20,
        choices=[
            ("low", "Low"),
            ("medium", "Medium"),
            ("high", "High"),
            ("critical", "Critical"),
        ],
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        app_label = "protobuf"
        db_table = "protobuf_obligation"

    def to_protobuf(self) -> greenova_data_pb2.Obligation:
        """Convert Django model to protobuf message."""
        proto_obligation = greenova_data_pb2.Obligation()
        proto_obligation.id = self.id
        proto_obligation.project_id = self.project_id
        proto_obligation.title = self.title
        proto_obligation.description = self.description
        proto_obligation.due_date = self.due_date.isoformat()
        proto_obligation.status = self.status
        proto_obligation.priority = self.priority
        proto_obligation.created_at = int(self.created_at.timestamp())
        return proto_obligation


class ChartDataModel(models.Model):
    """Model for storing chart data that can be serialized to protobuf.

    This model stores chart configuration and data points for
    environmental compliance visualizations.
    """

    project = models.ForeignKey(
        ProtoBufProject, on_delete=models.CASCADE, related_name="charts"
    )
    chart_type = models.CharField(
        max_length=50,
        choices=[
            ("line", "Line Chart"),
            ("bar", "Bar Chart"),
            ("pie", "Pie Chart"),
            ("scatter", "Scatter Plot"),
        ],
    )
    title = models.CharField(max_length=200)
    x_axis_label = models.CharField(max_length=100)
    y_axis_label = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        app_label = "protobuf"
        db_table = "protobuf_chart_data"

    def to_protobuf(self) -> chart_data_pb2.ChartData:
        """Convert chart model to protobuf message."""
        proto_chart = chart_data_pb2.ChartData()
        proto_chart.chart_type = self.chart_type
        proto_chart.title = self.title
        proto_chart.x_axis_label = self.x_axis_label
        proto_chart.y_axis_label = self.y_axis_label

        # Add data points from related ChartDataPoint models
        for point in self.data_points.all():
            proto_point = proto_chart.data_points.add()
            proto_point.x_value = point.x_value
            proto_point.y_value = point.y_value
            proto_point.label = point.label

        return proto_chart


class ChartDataPoint(models.Model):
    """Individual data points for charts."""

    chart = models.ForeignKey(
        ChartDataModel, on_delete=models.CASCADE, related_name="data_points"
    )
    x_value = models.FloatField()
    y_value = models.FloatField()
    label = models.CharField(max_length=100, blank=True)

    class Meta:
        app_label = "protobuf"
        db_table = "protobuf_chart_data_point"
