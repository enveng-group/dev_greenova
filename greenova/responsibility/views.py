from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import ResponsibilityRole, ResponsibilityAssignment


@login_required
def responsibility_home(request):
    """Home view for responsibility app."""
    # Get assignments for current user
    assignments = ResponsibilityAssignment.objects.filter(
        user=request.user
    ).select_related('obligation', 'role')

    context = {
        'assignments': assignments,
    }

    return render(request, 'responsibility/responsibility_home.html', context)


@login_required
def assignment_list(request):
    """List view for responsibility assignments."""
    # Get assignments for current user
    assignments = ResponsibilityAssignment.objects.filter(
        user=request.user
    ).select_related('obligation', 'role')

    context = {
        'assignments': assignments,
    }

    return render(request, 'responsibility/assignment_list.html', context)


@login_required
def role_list(request):
    """List view for responsibility roles."""
    # Get roles for companies the user belongs to
    user_companies = request.user.companies.all()
    roles = ResponsibilityRole.objects.filter(
        company__in=user_companies,
        is_active=True
    ).select_related('company')

    context = {
        'roles': roles,
    }

    return render(request, 'responsibility/role_list.html', context)
