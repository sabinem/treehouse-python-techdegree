import os
from PIL import Image

from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login
#rom django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.core import exceptions

from .models import Profile
from .forms import UserForm, ProfileForm, PasswordChangeForm


@login_required()
def own_profile(request):
    try:
        profile = Profile.objects.get(user=request.user)
    except exceptions.ObjectDoesNotExist:
        return HttpResponseRedirect(reverse('profiles:create'))
    return render(request, 'profiles/own_profile.html', {'profile': profile})



@login_required()
def other_profile(request, pk):
    profile = get_object_or_404(Profile, user_id=pk)
    next_profile = Profile.objects.filter(user__username__gt=profile.user.username)\
        .order_by('user__username').first()
    if not next_profile:
        next_profile = Profile.objects.all()\
            .order_by('user__username').first()
    if profile.user == request.user:
        messages.success(
            request,
           "This is your profile! Go to it <a href='{}'>here</a> if you like"
           .format(reverse('profiles:own')),
            extra_tags='safe'
        )
    return render(request, 'profiles/other_profile.html',
                  {'profile': profile,
                   'next_profile': next_profile})



@login_required
def list_profiles(request):
    profiles = Profile.objects.all().select_related('user').order_by('user__username')
    return render(request, 'profiles/list_profiles.html', {'profiles': profiles})


@login_required()
def change_password(request):
    form = PasswordChangeForm(user=request.user)
    print(form)
    if request.method == 'POST':
        form = PasswordChangeForm(data=request.POST, user=request.user)
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
    return render(request, 'profiles/change_password.html', {'form': form})


@login_required
def edit_profile(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)

        profile_form = ProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, ('Your profile was successfully updated!'))
            return HttpResponseRedirect(reverse('profiles:own'))
        else:
            messages.error(request,('Please correct the error below.'))
    else:
        user_form = UserForm(instance=request.user)
        profile_form = ProfileForm(instance=request.user.profile)
    return render(request, 'profiles/edit_profile.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })


@login_required
def create_profile(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile = profile_form.save(commit=False)
            profile.user = request.user
            profile.save()
            messages.success(request, ('Your profile was successfully updated!'))
            return HttpResponseRedirect(reverse('profiles:view'))
        else:
            messages.error(request,('Please correct the error below.'))
    else:
        user_form = UserForm(instance=request.user)
        profile_form = ProfileForm()
    return render(request, 'profiles/create_profile.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })


@login_required
def edit_avatar(request):
    profile = Profile.objects.get(user= request.user)
    print(profile.avatar.url)
    avatar_img = Image.open('/Users/sabinemaennel/PycharmProjects/userprofile/profile_project/media/pic_folder/51679728_s_ydF0Ni0.jpg')

    return render(request, 'profiles/edit_avatar.html', {'profile': profile, 'avatar_img': avatar_img})



from django.http import HttpResponse
from PIL import Image

import random
INK = "red", "blue", "green", "yellow"

def image(request):

    # ... create/load image here ...
    image = Image.new("RGB", (800, 600), random.choice(INK))

    # serialize to HTTP response
    response = HttpResponse(content_type="image/png")
    image.save(response, "PNG")
    return response



def pil_image(request):
    ''' A View that Returns a PNG Image generated using PIL'''

    from PIL import Image, ImageDraw

    size = (400,500)             # size of the image to create
    im = Image.new('RGB', size) # create the image
    draw = ImageDraw.Draw(im)   # create a drawing object that is
                                # used to draw on the new image
    red = (255,0,0)    # color of our text
    text_pos = (10,10) # top-left position of our text
    text = "Hello World!" # text to draw
    # Now, we'll do the drawing:
    draw.text(text_pos, text, fill=red)

    del draw # I'm done drawing so I don't need this anymore

    # We need an HttpResponse object with the correct mimetype
    response = HttpResponse(content_type="image/png")
    # now, we tell the image to save as a PNG to the
    # provided file-like object
    im.save(response, 'PNG')

    return response # and we're done!