"""
views for anonymous users
- superusers are logged out when they arrive at the general site
- logged in users are send to their profile page
"""
from django.shortcuts import render, reverse
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth import logout


def home(request):
    """
    home page
    - page is only seen before or after login
    """
    if request.user.is_superuser:
        logout(request)
        messages.success(request, "You've been signed out. Come back soon!")
    elif request.user.is_authenticated():
        return HttpResponseRedirect(reverse('profiles:own'))
    return render(request, 'home.html')
