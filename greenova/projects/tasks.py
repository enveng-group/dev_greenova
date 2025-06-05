"""Background and manual tasks for the projects app.

All functions and classes are decorated with @beartype for runtime type checking.
"""
from beartype import beartype
import logging
from datetime import timedelta
from django.utils import timezone
from .models import Project
from .types import ProjectMetadataDict, ProjectMembershipDict, ProjectObligationDict, ProjectManager, MembershipManager, ObligationRelationshipHandler

logger = logging.getLogger(__name__)

@beartype
def update_project_statuses() -> None:
    """Check for inactive projects and log them.

    Logs projects with no members or not updated in the last 6 months.
    """
    six_months_ago = timezone.now() - timedelta(days=180)
    projects = Project.objects.all()
    count = 0
    for project in projects:
        member_count = project.get_member_count()
        if member_count == 0:
            logger.warning(
                "Project %s (id=%s) has no members!", project.name, project.id
            )
            count += 1
        elif project.updated_at < six_months_ago:
            logger.info(
                "Project %s (id=%s) has not been updated in over 6 months.",
                project.name,
                project.id,
            )
            count += 1
    logger.info("Checked %d inactive or stale projects.", count)
