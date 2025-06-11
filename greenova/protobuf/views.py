"""Views for Protobuf-based API endpoints.

These views demonstrate how to use protobuf serialization
for efficient data transfer in API responses.
"""

from django.http import HttpResponse, JsonResponse
from django.views import View

from . import greenova_data_pb2
from .models import ChartDataModel, ProtoBufProject


class ProtobufProjectAPIView(View):
    """API view that returns project data in protobuf format.

    This demonstrates efficient serialization for frontend consumption.
    """

    def get(self, request, project_id: int | None = None) -> HttpResponse:
        """Get project data serialized as protobuf."""
        if project_id:
            try:
                project = ProtoBufProject.objects.get(id=project_id)
                proto_data = project.to_protobuf()

                response = HttpResponse(
                    proto_data.SerializeToString(),
                    content_type="application/x-protobuf",
                )
                response["Content-Disposition"] = (
                    f'attachment; filename="project_{project_id}.pb"'
                )
                return response

            except ProtoBufProject.DoesNotExist:
                return JsonResponse({"error": "Project not found"}, status=404)
        else:
            # Return list of all projects
            projects = ProtoBufProject.objects.all()
            project_list = greenova_data_pb2.ProjectList()

            for project in projects:
                proto_project = project_list.projects.add()
                proto_project.CopyFrom(project.to_protobuf())

            response = HttpResponse(
                project_list.SerializeToString(),
                content_type="application/x-protobuf",
            )
            response["Content-Disposition"] = 'attachment; filename="projects.pb"'
            return response


class ProtobufObligationAPIView(View):
    """API view for obligation data in protobuf format."""

    def get(self, request, project_id: int) -> HttpResponse:
        """Get obligations for a project serialized as protobuf."""
        try:
            project = ProtoBufProject.objects.get(id=project_id)
            obligations = project.obligations.all()

            obligation_list = greenova_data_pb2.ObligationList()
            for obligation in obligations:
                proto_obligation = obligation_list.obligations.add()
                proto_obligation.CopyFrom(obligation.to_protobuf())

            response = HttpResponse(
                obligation_list.SerializeToString(),
                content_type="application/x-protobuf",
            )
            response["Content-Disposition"] = (
                f'attachment; filename="obligations_{project_id}.pb"'
            )
            return response

        except ProtoBufProject.DoesNotExist:
            return JsonResponse({"error": "Project not found"}, status=404)


class ProtobufChartDataAPIView(View):
    """API view for chart data in protobuf format."""

    def get(self, request, chart_id: int) -> HttpResponse:
        """Get chart data serialized as protobuf."""
        try:
            chart = ChartDataModel.objects.get(id=chart_id)
            proto_data = chart.to_protobuf()

            response = HttpResponse(
                proto_data.SerializeToString(),
                content_type="application/x-protobuf",
            )
            response["Content-Disposition"] = (
                f'attachment; filename="chart_{chart_id}.pb"'
            )
            return response

        except ChartDataModel.DoesNotExist:
            return JsonResponse({"error": "Chart not found"}, status=404)


class ProtobufJSONAPIView(View):
    """API view that returns protobuf data as JSON for debugging.

    This is useful for development and testing protobuf serialization.
    """

    def get(
        self, request, model_type: str, object_id: int | None = None
    ) -> JsonResponse:
        """Get protobuf data as JSON for debugging."""
        try:
            if model_type == "project":
                if object_id:
                    project = ProtoBufProject.objects.get(id=object_id)
                    proto_data = project.to_protobuf()
                else:
                    projects = ProtoBufProject.objects.all()
                    project_list = greenova_data_pb2.ProjectList()
                    for project in projects:
                        proto_project = project_list.projects.add()
                        proto_project.CopyFrom(project.to_protobuf())
                    proto_data = project_list

            elif model_type == "obligation":
                if object_id:
                    project = ProtoBufProject.objects.get(id=object_id)
                    obligations = project.obligations.all()
                    obligation_list = greenova_data_pb2.ObligationList()
                    for obligation in obligations:
                        proto_obligation = obligation_list.obligations.add()
                        proto_obligation.CopyFrom(obligation.to_protobuf())
                    proto_data = obligation_list
                else:
                    return JsonResponse(
                        {"error": "Project ID required for obligations"}, status=400
                    )

            elif model_type == "chart":
                if object_id:
                    chart = ChartDataModel.objects.get(id=object_id)
                    proto_data = chart.to_protobuf()
                else:
                    return JsonResponse({"error": "Chart ID required"}, status=400)
            else:
                return JsonResponse({"error": "Invalid model type"}, status=400)

            # Convert protobuf to dict for JSON response
            from google.protobuf.json_format import MessageToDict

            data_dict = MessageToDict(proto_data)

            return JsonResponse(
                {
                    "model_type": model_type,
                    "data": data_dict,
                }
            )

        except (ProtoBufProject.DoesNotExist, ChartDataModel.DoesNotExist):
            return JsonResponse({"error": "Object not found"}, status=404)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
