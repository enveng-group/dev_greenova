from enum import Enum

class ProjectRole(str, Enum):
    PERDAMAN_MANAGEMENT = 'perdaman_management'
    PERDAMAN_ENV_HERITAGE_MANAGER = 'perdaman_env_heritage_manager'
    SCJV_PROJECT_DIRECTOR = 'scjv_project_director'
    SCJV_PROJECT_MANAGER = 'scjv_project_manager'
    SCJV_CONSTRUCTION_MANAGER = 'scjv_construction_manager'
    SCJV_COMMERCIAL_MANAGER = 'scjv_commercial_manager'
    SCJV_ENGINEERING_MANAGER = 'scjv_engineering_manager'
    SCJV_ENVIRONMENTAL_LEAD = 'scjv_environmental_lead'
    SCJV_HSSE_MANAGER = 'scjv_hsse_manager'
    SCJV_HERITAGE_INDIGENOUS_MANAGER = 'scjv_heritage_indigenous_manager'
    SCJV_LEAD_ENV_ADVISOR = 'scjv_lead_env_advisor'
    SCJV_SENIOR_ENV_ADVISOR = 'scjv_senior_env_advisor'
    SCJV_CONSTRUCTION_DIRECTOR = 'scjv_construction_director'
    SCJV_PROJECT_ENV_REPRESENTATIVE = 'scjv_project_env_representative'
    SCJV_CONSTRUCTION_SUPERVISOR = 'scjv_construction_supervisor'
    SCJV_COMMUNITY_STAKEHOLDER = 'scjv_community_stakeholder'
    OWNER = 'owner'
    MANAGER = 'manager'
    MEMBER = 'member'
    VIEWER = 'viewer'

ROLE_DISPLAY_NAMES: dict[str, str]
ROLE_COLORS: dict[str, str]

def get_role_display(role_value: str) -> str: ...
def get_role_color(role_value: str) -> str: ...
def get_role_choices() -> list[tuple[str, str]]: ...
def get_responsibility_choices() -> list[tuple[str, str]]: ...
def get_role_from_responsibility(responsibility: str) -> str | None: ...
def get_responsibility_from_role(role: str) -> str | None: ...
def get_responsibility_display_name(responsibility: str) -> str: ...
