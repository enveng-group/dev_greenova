import logging
from typing import Any

from beartype import beartype
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.core.paginator import Page, Paginator
from django.db.models import Count, Q, QuerySet
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.template.loader import render_to_string
from django.views.decorators.http import require_http_methods
from guardian.shortcuts import assign_perm, get_objects_for_user

from .commons import COMPANY_ROLE_ADMIN, is_company_admin
from .forms import (
    AddUserToCompanyForm,
    CompanyDocumentForm,
    CompanyForm,
    CompanyMembershipForm,
    CompanySearchForm,
)
from .models import Company, CompanyDocument, CompanyMembership
from .serializers import (
    CompanyCollectionProtoSerializer,
    CompanyProtoSerializer,
)

logger = logging.getLogger(__name__)

User = get_user_model()


@beartype
def create_company_with_permissions(user, form):
    """Create a company and assign object-level permissions to the creator.

    Args:
        user: The user creating the company.
        form: The validated CompanyForm instance.

    Returns:
        The created Company instance.

    """
    company = form.save(commit=False)
    company.save()
    form.save_m2m()
    # Assign object-level permissions to creator
    assign_perm("view_company", user, company)
    assign_perm("change_company", user, company)
    assign_perm("delete_company", user, company)
    assign_perm("manage_members", user, company)
    return company


@beartype
@login_required
def company_list(request: HttpRequest) -> HttpResponse:
    """View for listing companies with object-level permission checks."""
    search_form = CompanySearchForm(request.GET)
    # Only show companies the user has view permission for
    companies_query: QuerySet[Company] = get_objects_for_user(
        request.user,
        "company.view_company",
        Company.objects.all(),
    )

    # Apply filters if form is submitted
    if search_form.is_valid():
        search = search_form.cleaned_data.get("search")
        company_type = search_form.cleaned_data.get("company_type")
        industry = search_form.cleaned_data.get("industry")
        is_active = search_form.cleaned_data.get("is_active")

        if search:
            companies_query = companies_query.filter(
                Q(name__icontains=search) | Q(description__icontains=search),
            )

        if company_type:
            companies_query = companies_query.filter(company_type=company_type)

        if industry:
            companies_query = companies_query.filter(industry=industry)

        if is_active is not None:
            companies_query = companies_query.filter(is_active=is_active)

    # Add member count annotation
    companies_query = companies_query.annotate(member_count=Count("members"))

    # Handle pagination
    paginator = Paginator(companies_query, 10)
    page_number = int(request.GET.get("page", 1))
    companies: Page[Company] = paginator.get_page(page_number)

    # Check user permissions for each company using guardian
    user_permissions: dict[int, list[str]] = {}
    if not request.user.is_superuser:
        for company in companies:
            user_permissions[company.id] = request.user.get_all_permissions(company)

    context: dict[str, Any] = {
        "companies": companies,
        "search_form": search_form,
        "user_permissions": user_permissions,
        "page_obj": companies,
        "can_create": is_company_admin(request.user),
    }

    # Always render full template
    return render(request, "company/company_list.html", context)


@beartype
@login_required
def company_detail(request: HttpRequest, company_id: int) -> HttpResponse:
    """View for viewing company details."""
    company = get_object_or_404(Company, id=company_id)

    # Get projects related to this company
    projects = company.projects.all()

    # Get members with their roles
    members = CompanyMembership.objects.filter(company=company).select_related("user")

    # Get documents
    documents = company.documents.all()

    # Check user permissions
    can_edit = False
    can_manage_members = False
    if request.user.is_superuser:
        can_edit = True
        can_manage_members = True
    else:
        try:
            membership = CompanyMembership.objects.get(
                company=company,
                user=request.user,
            )
            if membership.role in {COMPANY_ROLE_ADMIN, "owner"}:
                can_edit = True
                can_manage_members = True
            elif membership.role == "manager":
                can_manage_members = True
        except CompanyMembership.DoesNotExist:
            pass

    context: dict[str, Any] = {
        "company": company,
        "projects": projects,
        "members": members,
        "documents": documents,
        "can_edit": can_edit,
        "can_manage_members": can_manage_members,
    }

    # Always render full template
    return render(request, "company/company_detail.html", context)


@beartype
@login_required
@user_passes_test(is_company_admin)
def company_create(request: HttpRequest) -> HttpResponse:
    """View for creating a new company."""
    if request.method == "POST":
        form = CompanyForm(request.POST, request.FILES)
        if form.is_valid():
            company: Company = create_company_with_permissions(request.user, form)

            # Add the creator as an owner of the company
            CompanyMembership.objects.create(
                company=company,
                user=request.user,
                role="owner",
                is_primary=True,
            )

            messages.success(request, f"Company '{company.name}' created successfully!")
            return redirect("company:detail", company_id=company.id)
    else:
        form = CompanyForm()

    context: dict[str, Any] = {"form": form, "action": "Create"}

    # Always render full template
    return render(request, "company/company_form.html", context)


@beartype
@login_required
def company_edit(request: HttpRequest, company_id: int) -> HttpResponse:
    """View for editing a company."""
    company = get_object_or_404(Company, id=company_id)

    # Check if user has permission to edit this company
    has_permission: bool = request.user.is_superuser
    if not has_permission:
        try:
            membership = CompanyMembership.objects.get(
                company=company,
                user=request.user,
            )
            has_permission = membership.role in {COMPANY_ROLE_ADMIN, "owner"}
        except CompanyMembership.DoesNotExist:
            pass

    if not has_permission:
        messages.error(request, "You don't have permission to edit this company.")
        return redirect("company:detail", company_id=company.id)

    if request.method == "POST":
        form = CompanyForm(request.POST, request.FILES, instance=company)
        if form.is_valid():
            company: Company = form.save()
            messages.success(request, f"Company '{company.name}' updated successfully!")
            return redirect("company:detail", company_id=company.id)
    else:
        form = CompanyForm(instance=company)

    context: dict[str, Any] = {"form": form, "company": company, "action": "Update"}

    # Always render full template
    return render(request, "company/company_form.html", context)


@beartype
@login_required
@user_passes_test(is_company_admin)
def company_delete(request: HttpRequest, company_id: int) -> HttpResponse:
    """View for deleting a company."""
    company = get_object_or_404(Company, id=company_id)

    # Check if user has permission to delete this company
    if not request.user.is_superuser:
        try:
            # Note: We're using the membership value now
            CompanyMembership.objects.get(
                company=company,
                user=request.user,
                role="owner",
            )
            # We could check membership.role here if needed
        except CompanyMembership.DoesNotExist:
            messages.error(request, "Only the owner can delete this company.")
            return redirect("company:detail", company_id=company.id)

    if request.method == "POST":
        company_name = company.name
        company.delete()
        messages.success(request, f"Company '{company_name}' deleted successfully!")
        return redirect("company:list")

    context: dict[str, Any] = {"company": company}

    # Always render full template
    return render(request, "company/company_delete.html", context)


@beartype
@login_required
def manage_members(request: HttpRequest, company_id: int) -> HttpResponse:
    """View for managing company members."""
    company = get_object_or_404(Company, id=company_id)

    # Check if user has permission to manage members
    can_manage = False
    if request.user.is_superuser:
        can_manage = True
    else:
        try:
            membership = CompanyMembership.objects.get(
                company=company,
                user=request.user,
            )
            if membership.role in {"owner", COMPANY_ROLE_ADMIN, "manager"}:
                can_manage = True
        except CompanyMembership.DoesNotExist:
            pass

    if not can_manage:
        messages.error(request, "You don't have permission to manage members.")
        return redirect("company:detail", company_id=company.id)

    # Get all members
    members = CompanyMembership.objects.filter(company=company).select_related("user")

    # Initialize forms
    add_user_form = AddUserToCompanyForm()

    context: dict[str, Any] = {
        "company": company,
        "members": members,
        "add_user_form": add_user_form,
        "can_edit": can_manage,
    }

    # Always render full template
    return render(request, "company/company_members.html", context)


@beartype
@login_required
@require_http_methods(["POST"])
def add_member(request: HttpRequest, company_id: int) -> HttpResponse:
    """View for adding a member to a company."""
    company = get_object_or_404(Company, id=company_id)

    # Check permissions
    can_manage = False
    if request.user.is_superuser:
        can_manage = True
    else:
        try:
            membership = CompanyMembership.objects.get(
                company=company,
                user=request.user,
            )
            if membership.role in {"owner", COMPANY_ROLE_ADMIN, "manager"}:
                can_manage = True
        except CompanyMembership.DoesNotExist:
            pass

    if not can_manage:
        return JsonResponse(
            {"status": "error", "message": "Permission denied"},
            status=403,
        )

    # Process form
    form = AddUserToCompanyForm(request.POST)
    if form.is_valid():
        user = form.cleaned_data["user"]
        role = form.cleaned_data["role"]
        department = form.cleaned_data["department"]
        position = form.cleaned_data["position"]
        is_primary = form.cleaned_data["is_primary"]

        # Check if user is already a member
        if CompanyMembership.objects.filter(company=company, user=user).exists():
            return JsonResponse(
                {
                    "status": "error",
                    "message": "User is already a member of this company",
                },
                status=400,
            )

        # Create membership
        membership = CompanyMembership.objects.create(
            company=company,
            user=user,
            role=role,
            department=department,
            position=position,
            is_primary=is_primary,
        )

        # Return updated member list
        members = CompanyMembership.objects.filter(company=company).select_related(
            "user",
        )
        html = render_to_string(
            "company/partials/member_list.html",
            {
                "members": members,
                "company": company,
                "can_edit": can_manage,
            },
            request=request,
        )

        return HttpResponse(html)

    return JsonResponse({"status": "error", "errors": form.errors}, status=400)


@beartype
@login_required
@require_http_methods(["POST"])
def remove_member(
    request: HttpRequest,
    company_id: int,
    member_id: int,
) -> HttpResponse:
    """View for removing a member from a company."""
    company = get_object_or_404(Company, id=company_id)
    membership = get_object_or_404(CompanyMembership, id=member_id, company=company)

    # Check permissions
    can_manage = False
    if request.user.is_superuser:
        can_manage = True
    else:
        try:
            user_role = CompanyMembership.objects.get(
                company=company,
                user=request.user,
            )

            # Only owner and admin can remove members
            if user_role.role in {"owner", COMPANY_ROLE_ADMIN}:
                can_manage = True
        except CompanyMembership.DoesNotExist:
            pass

    if not can_manage:
        return JsonResponse(
            {"status": "error", "message": "Permission denied"},
            status=403,
        )

    # Can't remove the owner
    if membership.role == "owner" and not request.user.is_superuser:
        return JsonResponse(
            {
                "status": "error",
                "message": "Company owner cannot be removed",
            },
            status=400,
        )

    # Remove membership
    membership.delete()

    # Return updated member list
    members = CompanyMembership.objects.filter(company=company).select_related("user")
    html = render_to_string(
        "company/partials/member_list.html",
        {
            "members": members,
            "company": company,
            "can_edit": can_manage,
        },
        request=request,
    )

    return HttpResponse(html)


@beartype
@login_required
def update_member_role(
    request: HttpRequest,
    company_id: int,
    member_id: int,
) -> HttpResponse:
    """View for updating a member's role in a company."""
    company = get_object_or_404(Company, id=company_id)
    membership = get_object_or_404(CompanyMembership, id=member_id, company=company)

    # Check permissions
    can_manage = False
    if request.user.is_superuser:
        can_manage = True
    else:
        try:
            user_membership = CompanyMembership.objects.get(
                company=company,
                user=request.user,
            )
            # Only owner and admin can update roles
            if user_membership.role in {"owner", COMPANY_ROLE_ADMIN}:
                can_manage = True
        except CompanyMembership.DoesNotExist:
            pass

    if not can_manage:
        return JsonResponse(
            {"status": "error", "message": "Permission denied"},
            status=403,
        )

    if request.method == "POST":
        form = CompanyMembershipForm(request.POST, instance=membership)
        if form.is_valid():
            form.save()
            return JsonResponse({"status": "success"})
        return JsonResponse({"status": "error", "errors": form.errors}, status=400)

    form = CompanyMembershipForm(instance=membership)

    context: dict[str, Any] = {
        "form": form,
        "membership": membership,
        "company": company,
    }

    return render(request, "company/partials/member_role_form.html", context)


@beartype
@login_required
def upload_document(request: HttpRequest, company_id: int) -> HttpResponse:
    """View for uploading a document to a company."""
    company = get_object_or_404(Company, id=company_id)

    # Check permissions
    can_edit = False
    if request.user.is_superuser:
        can_edit = True
    try:
        membership = CompanyMembership.objects.get(
            company=company,
            user=request.user,
        )
        if membership.role in {"owner", COMPANY_ROLE_ADMIN, "manager"}:
            can_edit = True
    except CompanyMembership.DoesNotExist:
        pass

    if not can_edit:
        messages.error(request, "You don't have permission to upload documents.")
        return redirect("company:detail", company_id=company.id)

    if request.method == "POST":
        form = CompanyDocumentForm(request.POST, request.FILES)
        if form.is_valid():
            document = form.save(commit=False)
            document.company = company
            document.uploaded_by = request.user
            document.save()

            messages.success(
                request,
                f"Document '{document.name}' uploaded successfully!",
            )
            return redirect("company:detail", company_id=company.id)
    else:
        form = CompanyDocumentForm()

    context: dict[str, Any] = {
        "form": form,
        "company": company,
    }

    # Always render full template
    return render(request, "company/document_form.html", context)


@beartype
@login_required
def delete_document(
    request: HttpRequest,
    company_id: int,
    document_id: int,
) -> HttpResponse:
    """View for deleting a document from a company."""
    company = get_object_or_404(Company, id=company_id)
    document = get_object_or_404(CompanyDocument, id=document_id, company=company)

    # Check permissions
    can_edit = False
    if request.user.is_superuser:
        can_edit = True
    else:
        try:
            membership = CompanyMembership.objects.get(
                company=company,
                user=request.user,
            )
            if membership.role in {"owner", COMPANY_ROLE_ADMIN}:
                can_edit = True
        except CompanyMembership.DoesNotExist:
            pass

    if not can_edit:
        return JsonResponse(
            {"status": "error", "message": "Permission denied"},
            status=403,
        )

    if request.method == "POST":
        document.delete()
        messages.success(request, f"Document '{document.name}' deleted successfully!")
        return redirect("company:detail", company_id=company.id)

    context: dict[str, Any] = {
        "document": document,
        "company": company,
    }

    # Always render full template
    return render(request, "company/document_delete.html", context)


@beartype
@login_required
def export_company(request, company_id: int) -> HttpResponse:
    """Export a single company as Protocol Buffer binary data."""
    if request.user.is_superuser:
        company = get_object_or_404(Company, id=company_id)
    else:
        company = get_object_or_404(
            Company,
            id=company_id,
            companymembership__user=request.user,
        )
    serializer = CompanyProtoSerializer(instance=company)
    data = serializer.data()
    if not data:
        messages.error(request, "Failed to export company.")
        return redirect("company:company_list")
    response = HttpResponse(data, content_type="application/octet-stream")
    response["Content-Disposition"] = f'attachment; filename="company_{company_id}.pb"'
    return response


@beartype
@login_required
def export_all_companies(request) -> HttpResponse:
    """Export all companies as a Protocol Buffer collection."""
    if request.user.is_superuser:
        companies = list(Company.objects.all())
    else:
        companies = list(Company.objects.filter(companymembership__user=request.user))
    serializer = CompanyCollectionProtoSerializer(instances=companies)
    data = serializer.data()
    if not data:
        messages.error(request, "Failed to export companies.")
        return redirect("company:company_list")
    response = HttpResponse(data, content_type="application/octet-stream")
    response["Content-Disposition"] = 'attachment; filename="companies.pb"'
    return response


@beartype
@login_required
@require_http_methods(["GET", "POST"])
def import_company(request) -> HttpResponse:
    """Import a company from Protocol Buffer binary data."""
    if request.method == "POST":
        if "file" not in request.FILES:
            messages.error(request, "No file was provided.")
            return redirect("company:import_company")
        uploaded_file = request.FILES["file"]
        try:
            data = uploaded_file.read()
            serializer = CompanyProtoSerializer(data=data)
            if not serializer.is_valid():
                messages.error(
                    request,
                    "Could not deserialize the file. Invalid format.",
                )
                return redirect("company:import_company")
            company = serializer.validated_data
            company.id = None  # Ensure a new record is created
            company.save()
            messages.success(request, "Company imported successfully.")
            return redirect("company:company_list")
        except (ValueError, OSError, AttributeError, TypeError) as e:
            logger.exception("Error importing company: %s", str(e))
            messages.error(request, "An error occurred while importing the company.")
            return redirect("company:import_company")
    # GET request - show import form
    return render(
        request,
        "company/import_company.html",
        {
            "page_title": "Import Company",
        },
    )
