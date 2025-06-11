import logging
from typing import Any

from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count, Q
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.views.decorators.http import require_http_methods
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from .forms import (
    AddUserToCompanyForm,
    CompanyDocumentForm,
    CompanyForm,
    CompanyMembershipForm,
    CompanySearchForm,
)
from .mixins import CompanyAccessMixin
from .models import Company, CompanyDocument, CompanyMembership

logger = logging.getLogger(__name__)

User = get_user_model()


def is_company_admin(user: User) -> bool:
    """Check if user is a company admin or superuser."""
    if not user.is_authenticated:
        return False

    # Superusers can manage all companies
    if user.is_superuser:
        return True

    # Check if user is an admin in any company
    return CompanyMembership.objects.filter(
        user=user, role__in=["owner", "admin"]
    ).exists()


class CompanyListView(LoginRequiredMixin, CompanyAccessMixin, ListView):
    """
    View for listing companies the user has access to.

    Users can only see companies they are members of.
    This view handles both regular requests and HTMX requests.
    """

    model = Company
    template_name = "company/company_list.html"
    context_object_name = "companies"
    paginate_by = 10

    def get_queryset(self):
        """Return filtered companies the user has access to."""
        # Start with the base queryset of companies the user has access to
        queryset = self.request.user.companies.all()

        # Get filter parameters from GET
        form = CompanySearchForm(self.request.GET)
        if form.is_valid():
            search = form.cleaned_data.get("search")
            company_type = form.cleaned_data.get("company_type")
            industry = form.cleaned_data.get("industry")
            is_active = form.cleaned_data.get("is_active")

            # Apply filters
            if search:
                queryset = queryset.filter(
                    Q(name__icontains=search) | Q(description__icontains=search)
                )

            if company_type:
                queryset = queryset.filter(company_type=company_type)

            if industry:
                queryset = queryset.filter(industry=industry)

            if is_active:
                queryset = queryset.filter(is_active=True)

        # Add member count annotation
        return queryset.annotate(member_count=Count("users"))

    def get_context_data(self, **kwargs):
        """Add search form and can_create flag to context."""
        context = super().get_context_data(**kwargs)
        context["search_form"] = CompanySearchForm(self.request.GET)
        context["can_create"] = is_company_admin(self.request.user)
        return context

    def get(self, request, *args, **kwargs):
        """Handle GET requests, including HTMX requests."""
        self.object_list = self.get_queryset()
        context = self.get_context_data()

        # For HTMX requests, return only the partial list
        if hasattr(request, "htmx") and request.htmx:
            return render(request, "company/partials/company_list.html", context)

        return super().get(request, *args, **kwargs)


class CompanyCreateView(LoginRequiredMixin, CreateView):
    """
    View for creating a new company.

    Only users with company admin privileges can create companies.
    """

    model = Company
    form_class = CompanyForm
    template_name = "company/company_form.html"
    success_url = reverse_lazy("company:list")

    def dispatch(self, request, *args, **kwargs):
        """Check if user has permission to create a company."""
        if not is_company_admin(self.request.user):
            messages.error(request, "You don't have permission to create companies.")
            return redirect("company:list")
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        """Add action to context."""
        context = super().get_context_data(**kwargs)
        context["action"] = "Create"
        context["button_text"] = "Create"
        context["legend"] = "Company Information"
        return context

    def form_valid(self, form):
        """Save form and add the user as an owner."""
        logger.info("Form validation successful")
        response = super().form_valid(form)
        self.object.users.add(self.request.user)

        # Also create a membership record
        CompanyMembership.objects.create(
            company=self.object, user=self.request.user, role="owner", is_primary=True
        )

        messages.success(
            self.request, f"Company '{self.object.name}' created successfully!"
        )
        return response

    def form_invalid(self, form):
        """Log form validation errors."""
        logger.error("Form validation failed: %s", form.errors)
        return super().form_invalid(form)


class CompanyUpdateView(LoginRequiredMixin, CompanyAccessMixin, UpdateView):
    """
    View for updating a company.

    Only users with appropriate permissions can update companies.
    """

    model = Company
    form_class = CompanyForm
    template_name = "company/company_update.html"
    context_object_name = "company"
    pk_url_kwarg = "company_id"

    def get_success_url(self):
        """Return URL to redirect after successful update."""
        return reverse_lazy("company:detail", kwargs={"company_id": self.object.id})

    def get_context_data(self, **kwargs):
        """Add action to context."""
        context = super().get_context_data(**kwargs)
        context["action"] = "Update"
        context["button_text"] = "Update"
        context["legend"] = "Edit Company Information"
        return context

    def form_valid(self, form):
        """Save form with success message."""
        logger.info("Form validation successful for company update")
        response = super().form_valid(form)
        messages.success(
            self.request, f"Company '{self.object.name}' updated successfully!"
        )
        return response

    def form_invalid(self, form):
        """Log form validation errors."""
        logger.error("Company update form validation failed: %s", form.errors)
        return super().form_invalid(form)


class CompanyDeleteView(LoginRequiredMixin, CompanyAccessMixin, DeleteView):
    """
    View for deleting a company.

    Only owners or superusers can delete companies.
    """

    model = Company
    template_name = "company/company_delete.html"
    context_object_name = "company"
    success_url = reverse_lazy("company:list")
    pk_url_kwarg = "company_id"

    def dispatch(self, request, *args, **kwargs):
        """Check if user has permission to delete the company."""
        company = self.get_object()

        # Superusers can delete any company
        if request.user.is_superuser:
            return super().dispatch(request, *args, **kwargs)

        # Check if user is owner
        try:
            membership = CompanyMembership.objects.get(
                company=company, user=request.user
            )
            if membership.role != "owner":
                messages.error(request, "Only the owner can delete this company.")
                return redirect("company:detail", company_id=company.id)
        except CompanyMembership.DoesNotExist:
            messages.error(request, "You don't have permission to delete this company.")
            return redirect("company:list")

        return super().dispatch(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        """Delete object and provide success message."""
        company = self.get_object()
        company_name = company.name
        response = super().delete(request, *args, **kwargs)
        messages.success(request, f"Company '{company_name}' deleted successfully!")
        return response


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
                company=company, user=request.user
            )
            if membership.role in ["owner", "admin"]:
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

    if hasattr(request, "htmx") and request.htmx:
        return render(request, "company/partials/company_detail.html", context)
    return render(request, "company/company_detail.html", context)


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
                company=company, user=request.user
            )
            if membership.role in ["owner", "admin", "manager"]:
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

    if hasattr(request, "htmx") and request.htmx:
        return render(request, "company/partials/company_members.html", context)
    return render(request, "company/company_members.html", context)


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
                company=company, user=request.user
            )
            if membership.role in ["owner", "admin", "manager"]:
                can_manage = True
        except CompanyMembership.DoesNotExist:
            pass

    if not can_manage:
        return JsonResponse(
            {"status": "error", "message": "Permission denied"}, status=403
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
            "user"
        )
        html = render_to_string(
            "company/partials/member_list.html",
            {"members": members, "company": company, "can_edit": can_manage},
            request=request,
        )

        return HttpResponse(html)

    return JsonResponse({"status": "error", "errors": form.errors}, status=400)


@login_required
@require_http_methods(["POST"])
def remove_member(
    request: HttpRequest, company_id: int, member_id: int
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
                company=company, user=request.user
            )

            # Only owner and admin can remove members
            if user_role.role in ["owner", "admin"]:
                can_manage = True
        except CompanyMembership.DoesNotExist:
            pass

    if not can_manage:
        return JsonResponse(
            {"status": "error", "message": "Permission denied"}, status=403
        )

    # Can't remove the owner
    if membership.role == "owner" and not request.user.is_superuser:
        return JsonResponse(
            {"status": "error", "message": "Company owner cannot be removed"},
            status=400,
        )

    # Remove membership
    membership.delete()

    # Return updated member list
    members = CompanyMembership.objects.filter(company=company).select_related("user")
    html = render_to_string(
        "company/partials/member_list.html",
        {"members": members, "company": company, "can_edit": can_manage},
        request=request,
    )

    return HttpResponse(html)


@login_required
def update_member_role(
    request: HttpRequest, company_id: int, member_id: int
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
                company=company, user=request.user
            )
            # Only owner and admin can update roles
            if user_membership.role in ["owner", "admin"]:
                can_manage = True
        except CompanyMembership.DoesNotExist:
            pass

    if not can_manage:
        return JsonResponse(
            {"status": "error", "message": "Permission denied"}, status=403
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


@login_required
def upload_document(request: HttpRequest, company_id: int) -> HttpResponse:
    """View for uploading a document to a company."""
    company = get_object_or_404(Company, id=company_id)

    # Check permissions
    can_edit = False
    if request.user.is_superuser:
        can_edit = True
    try:
        membership = CompanyMembership.objects.get(company=company, user=request.user)
        if membership.role in ["owner", "admin", "manager"]:
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
                request, f"Document '{document.name}' uploaded successfully!"
            )

            if hasattr(request, "htmx") and request.htmx:
                documents = company.documents.all()
                html = render_to_string(
                    "company/partials/document_list.html",
                    {"documents": documents, "company": company, "can_edit": can_edit},
                    request=request,
                )
                return HttpResponse(html)
            return redirect("company:detail", company_id=company.id)
    else:
        form = CompanyDocumentForm()

    context: dict[str, Any] = {
        "form": form,
        "company": company,
    }

    if hasattr(request, "htmx") and request.htmx:
        return render(request, "company/partials/document_form.html", context)
    return render(request, "company/document_form.html", context)


@login_required
def delete_document(
    request: HttpRequest, company_id: int, document_id: int
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
                company=company, user=request.user
            )
            if membership.role in ["owner", "admin"]:
                can_edit = True
        except CompanyMembership.DoesNotExist:
            pass

    if not can_edit:
        return JsonResponse(
            {"status": "error", "message": "Permission denied"}, status=403
        )

    if request.method == "POST":
        document.delete()
        messages.success(request, f"Document '{document.name}' deleted successfully!")

        if hasattr(request, "htmx") and request.htmx:
            documents = company.documents.all()
            html = render_to_string(
                "company/partials/document_list.html",
                {"documents": documents, "company": company, "can_edit": can_edit},
                request=request,
            )
            return HttpResponse(html)
        return redirect("company:detail", company_id=company.id)

    context: dict[str, Any] = {
        "document": document,
        "company": company,
    }

    if hasattr(request, "htmx") and request.htmx:
        return render(request, "company/partials/document_delete_confirm.html", context)
    return render(request, "company/document_delete.html", context)
