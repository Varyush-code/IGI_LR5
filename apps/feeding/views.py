from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.shortcuts import render
from .models import Feeding

@login_required
def feeding_list(request):
    role = request.user.profile.role

    if role == 'admin':
        feedings = Feeding.objects.all()

    elif role == 'employee':
        employee = request.user.profile.employee_data
        feedings = Feeding.objects.filter(employee=employee)

    else:
        raise PermissionDenied

    return render(
        request,
        'feeding.html',
        {'feedings': feedings}
    )