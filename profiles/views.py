"""
views for viewing and editing profiles
"""
from PIL import Image

from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.core import exceptions

from . import models
from . import forms


@login_required()
def own_profile(request):
    """
    view own profile
    - if the profile does not exist yet, the user is send to create profile
    """
    try:
        profile = models.Profile.objects.get(user=request.user)
    except exceptions.ObjectDoesNotExist:
        return HttpResponseRedirect(reverse('profiles:create'))
    return render(request, 'profiles/own_profile.html', {'profile': profile})


@login_required()
def other_profile(request, pk):
    """
    - view own profile as others see it
    - view profile of somebody else
    - the user can cycle through the profiles: he can always request to see
    the next one
    """
    profile = get_object_or_404(models.Profile, user_id=pk)
    next_profile = models.Profile.objects.filter(user__username__gt=profile.user.username)\
        .order_by('user__username').first()
    if not next_profile:
        next_profile = models.Profile.objects.all()\
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
    """
    list all profiles
    """
    profiles = models.Profile.objects.all().select_related('user').order_by('user__username')
    return render(request, 'profiles/list_profiles.html', {'profiles': profiles})


@login_required
def edit_profile(request):
    """
    edit profile
    """
    if request.method == 'POST':
        user_form = forms.UserForm(request.POST, instance=request.user)
        profile_form = forms.ProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, ('Your profile was successfully updated!'))
            return HttpResponseRedirect(reverse('profiles:own'))
        else:
            messages.error(request,('Please correct the error below.'))
    else:
        user_form = forms.UserForm(instance=request.user)
        profile_form = forms.ProfileForm(instance=request.user.profile)
    return render(request, 'profiles/edit_profile.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })


@login_required
def create_profile(request):
    """
    create profile
    """
    if request.method == 'POST':
        user_form = forms.UserForm(request.POST, instance=request.user)
        profile_form = forms.ProfileForm(request.POST, request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile = profile_form.save(commit=False)
            profile.user = request.user
            profile.save()
            messages.success(request, ('Your profile was successfully updated!'))
            return HttpResponseRedirect(reverse('profiles:own'))
        else:
            messages.error(request,('Please correct the error below.'))
    else:
        user_form = forms.UserForm(instance=request.user)
        profile_form = forms.ProfileForm()
    return render(request, 'profiles/create_profile.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })


@login_required
def transform_avatar(request):
    if request.method == 'POST':
        form = forms.AvatarForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, ('Your avatar was successfully updated!'))
            return HttpResponseRedirect(reverse('profiles:own'))
        else:
            messages.error(request, ('Please correct the error below.'))
    else:
        form = forms.AvatarForm()
    return render(request, 'profiles/edit_avatar.html', {
        'form': form,
    })


@login_required
def transform_avatar(request):
    profile = get_object_or_404(models.Profile, user_id=request.user.id)
    img = Image.open(profile.avatar)
    if request.method == "POST":
        form = forms.AvatarForm(request.POST)
        if form.is_valid():
            if form.cleaned_data['action'] == form.CROP:
                box = (form.cleaned_data['crop_left'],
                       form.cleaned_data['crop_top'],
                       form.cleaned_data['crop_right'],
                       form.cleaned_data['crop_bottom'])
                img = img.crop(box)
            if form.cleaned_data['action'] == form.FLIP_TOP_BOTTOM:
                img = img.transpose(Image.FLIP_TOP_BOTTOM)
            if form.cleaned_data['action'] == form.FLIP_LEFT_RIGHT:
                img = img.transpose(Image.FLIP_LEFT_RIGHT)
            if form.cleaned_data['action'] == form.ROTATE:
                degree = int(form.cleaned_data['rotate'])
                # converted to have an alpha layer
                im2 = img.convert('RGBA')
                # rotated image: rotation is clockwise -> calculate counter clockwise for PIL
                rot = im2.rotate(360 - degree, expand=1)
                # a white image same size as rotated image
                fff = Image.new('RGBA', rot.size, (255,) * 4)
                # create a composite image using the alpha layer of rot as a mask
                out = Image.composite(rot, fff, rot)
                img = out
            profile.save(new_image=img)
            return HttpResponseRedirect(reverse('profiles:transform_avatar'))
        else:
            messages.error(request, ('Please correct the error below.'))
    else:
        form = forms.AvatarForm()
    context = {'profile': profile, 'form': form}
    return render(
        request,
        'profiles/transform_avatar.html',
        context
    )

