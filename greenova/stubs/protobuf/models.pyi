from . import chart_data_pb2, greenova_data_pb2
from _typeshed import Incomplete
from django.db import models

class ProtoBufProject(models.Model):
    name: Incomplete
    description: Incomplete
    created_at: Incomplete
    updated_at: Incomplete
    is_active: Incomplete
    class Meta:
        app_label: str
        db_table: str
    def to_protobuf(self) -> greenova_data_pb2.Project: ...
    @classmethod
    def from_protobuf(cls, proto_project: greenova_data_pb2.Project) -> ProtoBufProject: ...

class ProtoBufObligation(models.Model):
    project: Incomplete
    title: Incomplete
    description: Incomplete
    due_date: Incomplete
    status: Incomplete
    priority: Incomplete
    created_at: Incomplete
    class Meta:
        app_label: str
        db_table: str
    def to_protobuf(self) -> greenova_data_pb2.Obligation: ...

class ChartDataModel(models.Model):
    project: Incomplete
    chart_type: Incomplete
    title: Incomplete
    x_axis_label: Incomplete
    y_axis_label: Incomplete
    created_at: Incomplete
    class Meta:
        app_label: str
        db_table: str
    def to_protobuf(self) -> chart_data_pb2.ChartData: ...

class ChartDataPoint(models.Model):
    chart: Incomplete
    x_value: Incomplete
    y_value: Incomplete
    label: Incomplete
    class Meta:
        app_label: str
        db_table: str
