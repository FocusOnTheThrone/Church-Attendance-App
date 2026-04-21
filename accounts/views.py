from django.contrib.auth import logout
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.contrib import messages
from .forms import CustomUserCreationForm


@login_required
def switch_organization_view(request):
    """Switch the current organization (church) context. POST with org_id."""
    if request.method != 'POST':
        return redirect(request.META.get('HTTP_REFERER', 'events'))
    try:
        org_id = int(request.POST.get('organization_id', 0))
    except (ValueError, TypeError):
        messages.error(request, 'Invalid organization.')
        return redirect(request.META.get('HTTP_REFERER', 'events'))
    accessible = request.user.get_accessible_organizations()
    org = next((o for o in accessible if o.id == org_id), None)
    if org:
        request.session['current_organization_id'] = org.id
        messages.success(request, f'Switched to {org.name}.')
    else:
        messages.error(request, 'You do not have access to that organization.')
    return redirect(request.META.get('HTTP_REFERER', 'events'))


@login_required
def custom_logout_view(request):
    """Custom logout view to ensure proper functionality."""
    logout(request)
    return redirect('accounts:login')


def signup_view(request):
    """User registration view. Creates a new Organization for each church."""
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            from .models import Organization
            church_name = form.cleaned_data.pop('church_name')
            org = Organization.objects.create(name=church_name)
            user = form.save(commit=False)
            user.organization = org
            user.save()
            form.save_m2m()  # for many-to-many if any
            messages.success(request, 'Account created successfully! You can now sign in.')
            return redirect('accounts:login')
    else:
        form = CustomUserCreationForm()
    
    return render(request, 'registration/signup.html', {'form': form})
