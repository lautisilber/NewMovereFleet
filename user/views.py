from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpRequest, HttpResponseForbidden, HttpResponseNotFound
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.views.decorators.http import require_http_methods
from .forms import UserRegisterForm, UserAdminUpdateForm
from main.utils import model_view_update

from .models import Profile
from django.contrib.auth.models import User

# message.debug
# message.info
# message.success
# message.warning
# message.error

@require_http_methods(['GET', 'POST'])
def register(request: HttpRequest):
    profile = False
    if request.user.is_authenticated:
        profile = request.user.profile.position_type >= 3
    if request.method == 'POST':
        form = UserRegisterForm(request.POST, profile=profile)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}! Now you can log in')
            return redirect(request.GET.get('next', 'user-login'))
    else:
        form = UserRegisterForm(profile=profile)
    context = {
        'form': form
    }
    return render(request, 'user/register.html', context=context)


@login_required
@require_http_methods(['GET', 'POST'])
def profile(request: HttpRequest):
    return render(request, 'user/profile.html')


@login_required
@require_http_methods(['GET'])
def admin_update_list(request: HttpRequest, position_type: int):
    if request.user.profile.position_type < 3:
        return HttpResponseForbidden("You haven't got the rank to view this page")
    if position_type not in [t.value for t in Profile.PositionType]:
        return HttpResponseForbidden(f'PositionType {position_type} does not exist')
    context = {
        'users': User.objects.filter(profile__position_type=position_type).all(),
        'title': str(Profile.PositionType.names[Profile.PositionType.values.index(position_type)]).capitalize() + ' Users'
    }
    return render(request, 'user/admin_update_list.html', context=context)



@login_required
@require_http_methods(['GET', 'POST'])
def admin_update(request: HttpRequest, user_id: int):
    if not User.objects.filter(id=user_id).exists():
        return HttpResponseNotFound(f'The User with id {user_id} was not found')
    user = User.objects.get(id=user_id)
    res = model_view_update(request, UserAdminUpdateForm, user_id, default_redirect=reverse('user-admin_update_list', kwargs={'position_type': user.profile.position_type}))
    # if request.user.profile.position_type < 3:
    #     return HttpResponseForbidden("You haven't got the rank to view this page")
    # if request.method == 'POST':
    #     form = UserAdminUpdateForm(request.POST, instance=request.user)
    #     if form.is_valid():
    #         form.save()
    #         return redirect(request.GET.get('next', 'main-home'))
    # else:
    #     form = UserAdminUpdateForm(instance=request.user)
    # context = {
    #     'form': form
    # }
    if isinstance(res, HttpResponse):
        return res

    context = {
        'model': res.instance,
        'form': res
    }
    return render(request, 'user/admin_update.html', context=context)