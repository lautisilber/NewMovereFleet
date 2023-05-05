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
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}! Now you can log in')
            return redirect('user-login')
    else:
        form = UserRegisterForm()
    context = {
        'form': form
    }
    return render(request, 'user/register.html', context=context)


@login_required
def profile(request: HttpRequest):
    context = load_navbar_context(request)
    return render(request, 'user/profile.html', context=context)