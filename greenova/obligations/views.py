from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.utils import timezone
from datetime import timedelta
from django.db.models import Q
from .models import Obligation
from .forms import ObligationForm, ObligationFilterForm

@login_required
def obligation_list(request):
    """Display list of obligations with filtering."""
    form = ObligationFilterForm(request.GET)
    obligations = Obligation.objects.all()

    if form.is_valid():
        filters = {}
        
        if form.cleaned_data.get('status'):
            filters['status'] = form.cleaned_data['status']
            
        if form.cleaned_data.get('project'):
            filters['project_name'] = form.cleaned_data['project']
            
        if form.cleaned_data.get('due_range'):
            today = timezone.now().date()
            if form.cleaned_data['due_range'] == 'overdue':
                obligations = obligations.filter(
                    action_due_date__lt=today,
                    status__in=['not_started', 'in_progress']
                )
            elif form.cleaned_data['due_range'] == '7days':
                obligations = obligations.filter(
                    action_due_date__range=[today, today + timedelta(days=7)]
                )
            elif form.cleaned_data['due_range'] == '14days':
                obligations = obligations.filter(
                    action_due_date__range=[today, today + timedelta(days=14)]
                )
            elif form.cleaned_data['due_range'] == 'month':
                obligations = obligations.filter(
                    action_due_date__range=[today, today + timedelta(days=30)]
                )
        
        obligations = obligations.filter(**filters)

    context = {
        'form': form,
        'obligations': obligations,
        'stats': {
            'overdue': Obligation.objects.filter(
                action_due_date__lt=timezone.now().date(),
                status__in=['not_started', 'in_progress']
            ).count(),
            'week': Obligation.objects.filter(
                action_due_date__range=[
                    timezone.now().date(),
                    timezone.now().date() + timedelta(days=7)
                ]
            ).count(),
            'fortnight': Obligation.objects.filter(
                action_due_date__range=[
                    timezone.now().date(),
                    timezone.now().date() + timedelta(days=14)
                ]
            ).count(),
            'month': Obligation.objects.filter(
                action_due_date__range=[
                    timezone.now().date(),
                    timezone.now().date() + timedelta(days=30)
                ]
            ).count(),
        }
    }
    return render(request, 'obligations.html', context)

@login_required
def obligation_detail(request, pk):
    """Display single obligation details."""
    obligation = get_object_or_404(Obligation, obligation_number=pk)
    return render(request, 'obligation_register/obligations_view.html', {
        'obligation': obligation
    })

@login_required
def obligation_create(request):
    """Create new obligation."""
    if request.method == 'POST':
        form = ObligationForm(request.POST)
        if form.is_valid():
            obligation = form.save(commit=False)
            obligation.created_by = request.user
            obligation.save()
            messages.success(request, 'Obligation created successfully.')
            return redirect('obligation_detail', pk=obligation.pk)
    else:
        form = ObligationForm()
    
    return render(request, 'obligation_register/obligations_crud.html', {
        'form': form,
        'title': 'Create Obligation'
    })

@login_required
def obligation_update(request, pk):
    """Update existing obligation."""
    obligation = get_object_or_404(Obligation, obligation_number=pk)
    if request.method == 'POST':
        form = ObligationForm(request.POST, instance=obligation)
        if form.is_valid():
            obligation = form.save(commit=False)
            obligation.updated_by = request.user
            obligation.save()
            messages.success(request, 'Obligation updated successfully.')
            return redirect('obligations:detail', pk=obligation.obligation_number)
    else:
        form = ObligationForm(instance=obligation)
    
    return render(request, 'obligation_register/obligations_crud.html', {
        'form': form,
        'title': 'Update Obligation'
    })

@login_required
def obligation_delete(request, pk):
    """Delete obligation."""
    obligation = get_object_or_404(Obligation, pk=pk)
    if request.method == 'POST':
        obligation.delete()
        messages.success(request, 'Obligation deleted successfully.')
        return redirect('obligation_list')
    return render(request, 'obligation_register/obligation_confirm_delete.html', {
        'obligation': obligation
    })