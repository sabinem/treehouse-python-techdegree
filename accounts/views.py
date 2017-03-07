"""
This file contains authentications views, that sign users in and out
"""
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render

from . import forms


def sign_in(request):
    """
    signs users in:
    - superusers are directly signed in into the admin
    - active users are taken to their profiles when they sign in
    """
    form = forms.AuthenticationForm()
    if request.method == 'POST':
        form = forms.AuthenticationForm(data=request.POST)
        if form.is_valid():
            if form.user_cache is not None:
                user = form.user_cache
                if user.is_superuser:
                    login(request, user)
                    return HttpResponseRedirect(reverse('admin:index'))
                elif user.is_active:
                    login(request, user)
                    return HttpResponseRedirect(
                        reverse('profiles:own')
                    )
                else:
                    messages.error(
                        request,
                        "That user account has been disabled."
                    )
            else:
                messages.error(
                    request,
                    "Username or password is incorrect."
                )
    return render(request, 'accounts/sign_in.html', {'form': form})


def sign_up(request):
    """
    sign up for new users
    - they are taken to create their profile after sign up
    """
    form = forms.UserCreationForm()
    if request.method == 'POST':
        form = forms.UserCreationForm(data=request.POST)
        if form.is_valid():
            form.save()
            user = authenticate(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password1']
            )
            login(request, user)
            messages.success(
                request,
                "You're now a user! You've been signed in, too."
            )
            return HttpResponseRedirect(reverse('profiles:create'))
    return render(request, 'accounts/sign_up.html', {'form': form})


@login_required
def sign_out(request):
    """
    logs users out
    - after log out the user is taken to the home page
    """
    logout(request)
    messages.success(request, "You've been signed out. Come back soon!")
    return HttpResponseRedirect(reverse('home'))


@login_required()
def change_password(request):
    """
    change password
    """
    form = forms.PasswordChangeForm(user=request.user)
    if request.method == 'POST':
        form = forms.PasswordChangeForm(data=request.POST, user=request.user)
        if form.is_valid():
            form.save()
            user = authenticate(
                username=request.user.username,
                password=form.cleaned_data['new_password1']
            )
            login(request, user)
            messages.success(
                request,
                "Your password has been changed."
            )
            return HttpResponseRedirect(reverse('profiles:own'))
    return render(request, 'accounts/change_password.html', {'form': form})
