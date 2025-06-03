from auditing.models import ComplianceComment, NonConformanceComment
from django.test import TestCase
from obligations.models import Obligation


class AuditingModelTests(TestCase):
    def setUp(self) -> None:
        self.obligation = Obligation.objects.create(name="Test Obligation")

# Check if the ComplianceComment can be created successfully
    def test_create_compliance_comment(self) -> None:
        comment = ComplianceComment.objects.create(
            obligation=self.obligation,
            comment="All good here",
        )
        assert comment.comment == "All good here"
        assert comment.obligation == self.obligation


# Check if the reverse query is available for ComplianceComment
def test_reverse_lookup_compliance(self) -> None:
    ComplianceComment.objects.create(
        obligation=self.obligation,
        comment="Test compliance",
    )
    assert self.obligation.compliance_comments.count() == 1
    assert self.obligation.compliance_comments.first().comment == "Test compliance"

# Check if the NonConformanceComment can be created successfully
    def test_create_non_conformance_comment(self) -> None:
        comment = NonConformanceComment.objects.create(
            obligation=self.obligation,
            comment="Issue with safety procedure",
        )
        assert comment.comment == "Issue with safety procedure"
        assert comment.obligation == self.obligation

# Check if the reverse query is available for NonConformanceComment
    def test_reverse_lookup_non_conformance(self) -> None:
        NonConformanceComment.objects.create(
            obligation=self.obligation,
            comment="Issue with safety procedure",
        )
        assert self.obligation.non_conformance_comments.count() == 1
