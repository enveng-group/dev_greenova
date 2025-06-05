"""
Custom type definitions and type aliases for the company app.

Centralizes reusable type hints and aliases for company, organization, and
employee data structures, and provides Protocols for company profile managers,
employee managers, and org chart handlers to enable strict type-safety across
modules.

Features:
    - Strict type annotations and runtime type checking with beartype
    - Google style docstrings throughout
    - Protocols for company profile managers, employee managers, and org chart handlers

Author: Adrian Gallo <agallo@enveng-group.com.au>
License: AGPL-3.0
"""

from typing import List, Protocol, TypedDict, runtime_checkable
from beartype import beartype

class CompanyProfileDict(TypedDict):
    """TypedDict for company profile data."""
    id: str
    name: str
    abn: str
    address: str
    contact_email: str
    created_at: str
    updated_at: str

class EmployeeRecordDict(TypedDict):
    """TypedDict for employee record data."""
    id: str
    company_id: str
    name: str
    email: str
    role: str
    is_active: bool
    joined_at: str

class OrgChartNodeDict(TypedDict):
    """TypedDict for an org chart node."""
    id: str
    name: str
    role: str
    children: List["OrgChartNodeDict"]

OrgChart = List[OrgChartNodeDict]

@runtime_checkable
class CompanyProfileManager(Protocol):
    """Protocol for managing company profiles."""

    @beartype
    def get_profile(self, company_id: str) -> CompanyProfileDict:
        """Retrieve a company profile by company ID.

        Args:
            company_id: The unique identifier for the company.

        Returns:
            CompanyProfileDict: The company profile dictionary.
        """
        ...

    @beartype
    def update_profile(self, company_id: str, data: CompanyProfileDict) -> None:
        """Update a company profile.

        Args:
            company_id: The unique identifier for the company.
            data: The updated company profile dictionary.
        """
        ...

@runtime_checkable
class EmployeeManager(Protocol):
    """Protocol for managing employees."""

    @beartype
    def get_employee(self, employee_id: str) -> EmployeeRecordDict:
        """Retrieve an employee record by employee ID.

        Args:
            employee_id: The unique identifier for the employee.

        Returns:
            EmployeeRecordDict: The employee record dictionary.
        """
        ...

    @beartype
    def list_employees(self, company_id: str) -> List[EmployeeRecordDict]:
        """List all employees for a company.

        Args:
            company_id: The unique identifier for the company.

        Returns:
            List[EmployeeRecordDict]: List of employee record dictionaries.
        """
        ...

@runtime_checkable
class OrgChartHandler(Protocol):
    """Protocol for building organization charts."""

    @beartype
    def build_org_chart(self, company_id: str) -> OrgChart:
        """Build an organization chart for a company.

        Args:
            company_id: The unique identifier for the company.

        Returns:
            OrgChart: The organization chart as a list of nodes.
        """
        ...
