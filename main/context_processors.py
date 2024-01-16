from django.http import HttpRequest
from typing import Any

from django.contrib.auth.models import User
from .models import Vehicle, Company
from user.models import Profile


def load_navbar_context(request: HttpRequest) -> dict[str, Any]:
    context = {}
    if request.user.is_authenticated:
        if request.user.profile.position_type in ('D', 'M'):
            context = {
                'base_vehicles': sorted(list(set(Vehicle.objects.filter(question_templates__position_type=request.user.profile.position_type).all())), key=lambda v: v.id) # TODO: make this more efficient
            }
        elif request.user.profile.position_type in ('A', 'S'):
            context = {
                'base_vehicles': Vehicle.objects.all(),
                'base_companies': Company.objects.all(),
                #'base_worker_types': #User.objects.filter(profile__position_type__lte=2).all()
            }
    return context