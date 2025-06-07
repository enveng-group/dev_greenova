# Copyright 2025 Enveng Group.
# SPDX-License-Identifier: AGPL-3.0-or-later

"""Company management logic for the company app.

This module provides the Company and CompanyManager classes for managing
company profiles and employee records, with strict type annotations and
runtime type checking.

Features:
    - Strict type annotations and runtime type checking with beartype
    - Google style docstrings throughout
    - Company and CompanyManager classes for profile and employee management

Author:
    Adrian Gallo <agallo@enveng-group.com.au>
"""

from beartype import beartype

from .types import (
    CompanyProfileDict,
    CompanyProfileManager,
    EmployeeManager,
    EmployeeRecordDict,
)


class Company:
    """Represents a company with a profile and employee records."""

    @beartype
    def __init__(
        self,
        profile: CompanyProfileDict,
        employees: list[EmployeeRecordDict],
    ) -> None:
        """Initialize a Company instance.

        Args:
            profile: The company profile dictionary.
            employees: List of employee record dictionaries.

        """
        self.profile: CompanyProfileDict = profile
        self.employees: list[EmployeeRecordDict] = employees

    @beartype
    def get_employee_records(self) -> list[EmployeeRecordDict]:
        """Get the list of employee records.

        Returns:
            List of EmployeeRecordDict.

        """
        return self.employees

    @beartype
    def update_profile(self, new_profile: CompanyProfileDict) -> None:
        """Update the company profile.

        Args:
            new_profile: The new company profile dictionary.

        """
        self.profile = new_profile


class CompanyManager(CompanyProfileManager, EmployeeManager):
    """Manager for company profile and employee operations."""

    @beartype
    def __init__(self, company: Company) -> None:
        """Initialize a CompanyManager.

        Args:
            company: The Company instance to manage.

        """
        self.company: Company = company

    @beartype
    def add_employee(self, employee: EmployeeRecordDict) -> None:
        """Add an employee to the company.

        Args:
            employee: The employee record to add.

        """
        self.company.employees.append(employee)

    @beartype
    def remove_employee(self, employee_id: str) -> None:
        """Remove an employee from the company by ID.

        Args:
            employee_id: The ID of the employee to remove.

        """
        self.company.employees = [
            emp for emp in self.company.employees if emp["id"] != employee_id
        ]

    @beartype
    def update_employee(
        self,
        employee_id: str,
        updated_record: EmployeeRecordDict,
    ) -> None:
        """Update an employee's record by ID.

        Args:
            employee_id: The ID of the employee to update.
            updated_record: The updated employee record.

        """
        for i, emp in enumerate(self.company.employees):
            if emp["id"] == employee_id:
                self.company.employees[i] = updated_record
                break

    @beartype
    def get_company_profile(self) -> CompanyProfileDict:
        """Get the company profile.

        Returns:
            The company profile dictionary.

        """
        return self.company.profile

    @beartype
    def set_company_profile(self, profile: CompanyProfileDict) -> None:
        """Set the company profile.

        Args:
            profile: The new company profile dictionary.

        """
        self.company.update_profile(profile)
