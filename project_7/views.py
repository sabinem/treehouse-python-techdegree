from django.shortcuts import render, reverse
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth import logout

def home(request):
    if request.user.is_superuser:
        logout(request)
        messages.success(request, "You've been signed out. Come back soon!")
    elif request.user.is_authenticated():
        return HttpResponseRedirect(reverse('profiles:own'))
    return render(request, 'home.html')