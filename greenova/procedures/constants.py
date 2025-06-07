"""constants.py.

Centralized constants for the procedures app.
"""

# Status choices for Procedure model
STATUS_DRAFT = "draft"
STATUS_REVIEW = "review"
STATUS_ACTIVE = "active"
STATUS_OBSOLETE = "obsolete"
STATUS_ARCHIVED = "archived"

STATUS_CHOICES = [
    (STATUS_DRAFT, "Draft"),
    (STATUS_REVIEW, "In Review"),
    (STATUS_ACTIVE, "Active"),
    (STATUS_OBSOLETE, "Obsolete"),
    (STATUS_ARCHIVED, "Archived"),
]

# Compliance status choices
COMPLIANT = "compliant"
NON_COMPLIANT = "non_compliant"
PARTIALLY_COMPLIANT = "partially_compliant"
NOT_ASSESSED = "not_assessed"

COMPLIANCE_STATUSES = [
    (COMPLIANT, "Compliant"),
    (NON_COMPLIANT, "Non-Compliant"),
    (PARTIALLY_COMPLIANT, "Partially Compliant"),
    (NOT_ASSESSED, "Not Assessed"),
]

# Procedure type choices
PROCEDURE_TYPE_INSPECTION = "inspection"
PROCEDURE_TYPE_MAINTENANCE = "maintenance"
PROCEDURE_TYPE_REPORTING = "reporting"
PROCEDURE_TYPE_TRAINING = "training"

PROCEDURE_TYPE_CHOICES = [
    (PROCEDURE_TYPE_INSPECTION, "Inspection"),
    (PROCEDURE_TYPE_MAINTENANCE, "Maintenance"),
    (PROCEDURE_TYPE_REPORTING, "Reporting"),
    (PROCEDURE_TYPE_TRAINING, "Training"),
]
