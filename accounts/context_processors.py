"""Context processors for accounts app."""


def organization_switcher(request):
    """Add current org and accessible orgs for the header switcher."""
    context = {'current_organization': None, 'accessible_organizations': []}
    if request.user.is_authenticated:
        accessible = getattr(request.user, 'get_accessible_organizations', lambda: [])()
        if accessible:
            current_id = request.session.get('current_organization_id')
            current = next((o for o in accessible if o.id == current_id), None)
            if not current:
                current = getattr(request.user, 'organization', None) or accessible[0]
                if current:
                    request.session['current_organization_id'] = current.id
            context['current_organization'] = current
            context['accessible_organizations'] = accessible
        else:
            context['current_organization'] = getattr(request.user, 'organization', None)
            context['accessible_organizations'] = []
    return context
