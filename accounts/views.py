"""views for the accounts app
the app uses a custom user model"""
import json

from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, get_object_or_404
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.core.urlresolvers import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.views import generic

from teambuilder import models as teambuilder_models

from . import forms, email


User = get_user_model()


class LoginView(generic.FormView):
    """Login View
    - uses djangos generic FormView"""
    form_class = forms.UserLoginForm
    success_url = reverse_lazy("teambuilder:projects")
    template_name = "accounts/signin.html"

    def form_valid(self, form):
        """the user is logged in,
        when the form is valid"""
        user = authenticate(
            email=form.cleaned_data['email'],
            password=form.cleaned_data['password']
        )
        login(self.request, user)
        return super().form_valid(form)


class LogoutView(generic.RedirectView):
    """Logout View
     - uses djangos generic RedirectView"""
    url = reverse_lazy("teambuilder:projects")

    def get(self, request, *args, **kwargs):
        """log user out"""
        logout(request)
        return super().get(request, *args, **kwargs)


class RegisterView(SuccessMessageMixin, generic.CreateView):
    """register user"""
    form_class = forms.UserCreateForm
    template_name = "accounts/signup.html"

    def form_valid(self, form):
        """authenticate user and log user in
        when form is valid"""
        form.save()
        user = authenticate(
            email=form.cleaned_data['email'],
            password=form.cleaned_data['password1']
        )
        login(self.request, user)
        return HttpResponseRedirect(reverse_lazy("accounts:profile"))


class ProfileView(generic.TemplateView):
    """view user profile
    own profile or that of others"""
    template_name = "accounts/profile.html"

    def get_context_data(self, **kwargs):
        """get context data for template
        - profile user may be the request user
        or an other user"""
        context = super().get_context_data(**kwargs)
        if 'profile_pk' in kwargs:
            profile_user = get_object_or_404(User, pk=kwargs['profile_pk'])
        else:
            profile_user = self.request.user
        context['user'] = profile_user
        context['projects'] = profile_user.get_projects()
        context['jobs'] = profile_user.get_jobs()
        context['skills'] = profile_user.get_skills()
        return context


@login_required
def profile_edit_view(request):
    """
    Allows a user to update his own profile.
    """
    #TODO: save projects

    #TODO: JAVASCRIPT for foto upload
    user = request.user
    skills = request.user.get_skills()
    jobs = request.user.get_jobs()
    projects = request.user.get_projects()

    skills_initial_data = [{'skill': skill}
                    for skill in skills]
    projects_initial_data = [{'title': project.title, 'link': project.link, 'id':project.id}
                  for project in projects]

    if request.method == 'POST':

        profile_form = forms.ProfileForm(request.POST, request.FILES, instance=request.user)
        skills_formset = forms.SkillsFormSet(request.POST, prefix='fs_skills')
        projects_formset = forms.ProjectsFormSet(request.POST, prefix='fs_projects')

        if profile_form.is_valid() and skills_formset.is_valid() and projects_formset.is_valid():
            profile_form.save()
            new_skills = set([skill_form.cleaned_data.get('skill')
                          for skill_form in skills_formset
                          if skill_form.cleaned_data.get('skill')])
            user.skills.clear()
            user.skills.add(*new_skills)

            #TODO: das funktioniert noch nicht! modelformfactory testen und verwenden
            #projects = projects_formset.save(commit=False)
            #for p in projects:
            #    print(p)

            #projects.save()

            return HttpResponseRedirect(reverse_lazy('accounts:profile'))
    else:
        profile_form = forms.ProfileForm(instance=request.user)
        skills_formset = forms.SkillsFormSet(initial=skills_initial_data, prefix='fs_skills')
        projects_formset = forms.ProjectsFormSet(initial=projects_initial_data, prefix='fs_projects')


    return render(request, 'accounts/profile_edit.html', {
        'profile_form': profile_form,
        'skills_formset': skills_formset,
        'projects_formset': projects_formset,
        'jobs': jobs,
    })


class ApplicationsListView(generic.TemplateView):
    """List applications for a users projects"""
    template_name = "accounts/applications.html"

    def get_context_data(self, **kwargs):
        """get context data to fill the template
        - destinguish between request user and other users"""
        if 'profile_pk' in kwargs:
            profile_user = get_object_or_404(User, pk=kwargs['profile_pk'])
        else:
            profile_user = self.request.user
        context = super().get_context_data(**kwargs)
        context['profile_user'] = profile_user
        context['status'] = list(teambuilder_models.ApplicationStatus)
        context['application_status'] = teambuilder_models.ApplicationStatus


        context['projects'] = profile_user.get_projects()
        context['needs'] = profile_user.get_needs()
        context['applications'] = \
            teambuilder_models.Application.objects.applications_for_a_users_projects(profile_user)
        for x in context['applications']:
            print("status", x.status)
        for x in context['application_status']:
            print("enum", x.name, x.value)



        #context['needs'] = models.Skill.objects.needs_for_user(user)
        return context


def search_applications(request):
    """ajax search in applications"""
    searchterm = request.GET.get('searchterm')
    response_data = {}
    response_data['result'] = 'Create post successful!'
    response_data['postpk'] = post.pk
    response_data['text'] = post.text
    response_data['created'] = post.created.strftime('%B %d, %Y %I:%M %p')
    response_data['author'] = post.author.username

    return HttpResponse(
        json.dumps(response_data),
        content_type="application/json"
    )


@login_required
def approve_application(request, application_pk):
    """rejecting or approving an application"""
    application = get_object_or_404(teambuilder_models.Application, pk=application_pk)
    application.reject()
    return HttpResponseRedirect(reverse_lazy(
        'accounts:applications', kwargs={'profile_pk':request.user.id}))


@login_required
def reject_application(request, application_pk):
    """rejecting or approving an application"""
    application = get_object_or_404(teambuilder_models.Application, pk=application_pk)
    application.approve()
    return HttpResponseRedirect(reverse_lazy(
        'accounts:applications', kwargs={'profile_pk':request.user.id}))