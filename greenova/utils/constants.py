from typing import Final, List

# Status Constants
STATUS_NOT_STARTED: Final[str] = 'not started'
STATUS_IN_PROGRESS: Final[str] = 'in progress'
STATUS_COMPLETED: Final[str] = 'completed'

STATUS_CHOICES: Final[List[tuple[str, str]]] = [
    (STATUS_NOT_STARTED, 'Not Started'),
    (STATUS_IN_PROGRESS, 'In Progress'),
    (STATUS_COMPLETED, 'Completed')
]

# System Status
SYSTEM_STATUS_OPERATIONAL: Final[str] = 'operational'
SYSTEM_STATUS_MAINTENANCE: Final[str] = 'maintenance'
SYSTEM_STATUS_ERROR: Final[str] = 'error'

SYSTEM_STATUS_CHOICES: Final[List[tuple[str, str]]] = [
    (SYSTEM_STATUS_OPERATIONAL, 'Operational'),
    (SYSTEM_STATUS_MAINTENANCE, 'Maintenance'),
    (SYSTEM_STATUS_ERROR, 'Error')
]