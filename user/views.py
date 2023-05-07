from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpRequest
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm

# message.debug
# message.info
# message.success
# message.warning
# message.error

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
def profile(request: HttpRequest):
    return render(request, 'user/profile.html', context=context)