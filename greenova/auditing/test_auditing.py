from django.test import TestCase
from obligations.models import Obligation
from auditing.models import ComplianceComment, NonConformanceComment
class AuditingModelTests(TestCase):
    def setUp(self):
        self.obligation = Obligation.objects.create(name="Test Obligation")

# Check if the ComplianceComment can be created successfully
    def test_create_compliance_comment(self):
        comment = ComplianceComment.objects.create(
            obligation=self.obligation,
            comment="All good here"
        )
        self.assertEqual(comment.comment, "All good here")
        self.assertEqual(comment.obligation, self.obligation)

# Check if the reverse query is available for ComplianceComment
def test_reverse_lookup_compliance(self):
    ComplianceComment.objects.create(
        obligation=self.obligation,
        comment="Test compliance"
    )
    self.assertEqual(self.obligation.compliance_comments.count(), 1)
    self.assertEqual(self.obligation.compliance_comments.first().comment, "Test compliance")

# Check if the NonConformanceComment can be created successfully
    def test_create_non_conformance_comment(self):
        comment = NonConformanceComment.objects.create(
            obligation=self.obligation,
            comment="Issue with safety procedure"
        )
        self.assertEqual(comment.comment, "Issue with safety procedure")
        self.assertEqual(comment.obligation, self.obligation)   

# Check if the reverse query is available for NonConformanceComment
    def test_reverse_lookup_non_conformance(self):
        NonConformanceComment.objects.create(
            obligation=self.obligation,
            comment="Issue with safety procedure"
        )
        self.assertEqual(self.obligation.non_conformance_comments.count(), 1)
