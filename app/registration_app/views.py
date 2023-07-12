from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm, UpdateUserForm
from django.http import HttpRequest


def register(request: HttpRequest):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account {username} created!')
            return redirect('login')
        else:
            form = UserRegisterForm()
            return render(request=request, template_name='registration/registration.html', context={'form': form})
    else:
        form = UserRegisterForm()
        return render(request=request, template_name='registration/registration.html', context={'form': form})


@login_required
def profile(request: HttpRequest):
    return render(request, template_name='registration/profile.html')


@login_required
def update_profile(request: HttpRequest):
    if request.method == 'POST':
        form = UpdateUserForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, f'Your profile is updated successfully!')
            return redirect(to='profile')
    else:
        form = UpdateUserForm(instance=request.user)

    return render(request=request, template_name='registration/update_profile.html', context={'form': form})
