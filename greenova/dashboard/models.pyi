from typing import Any

from django.db import models
from protobuf import greenova_data_pb2

class ProjectSummary(models.Model):
    total_projects: int
    active_projects: int
    completed_projects: int
    recent_projects: Any
    def to_proto(self) -> greenova_data_pb2.ProjectSummary: ...
    @classmethod
    def from_proto(cls, proto: greenova_data_pb2.ProjectSummary) -> ProjectSummary: ...

class ObligationSummary(models.Model):
    status: str
    count: int
    upcoming_obligations: Any
    def to_proto(self) -> greenova_data_pb2.ObligationSummary: ...
    @classmethod
    def from_proto(
        cls, proto: greenova_data_pb2.ObligationSummary
    ) -> ObligationSummary: ...

class ComplianceMetrics(models.Model):
    overall_compliance_rate: float
    overdue_obligations: int
    due_this_week: int
    due_this_month: int
    compliance_by_framework: Any
    def to_proto(self) -> greenova_data_pb2.ComplianceMetrics: ...
    @classmethod
    def from_proto(
        cls, proto: greenova_data_pb2.ComplianceMetrics
    ) -> ComplianceMetrics: ...

class DashboardData(models.Model):
    project_summary: ProjectSummary
    obligation_summaries: Any
    compliance_metrics: ComplianceMetrics
    last_updated: Any
    def to_proto(self) -> greenova_data_pb2.DashboardData: ...
    @classmethod
    def from_proto(cls, proto: greenova_data_pb2.DashboardData) -> DashboardData: ...
