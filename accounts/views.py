"""views for the accounts app
the app uses a custom user model"""

from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.contrib.auth import (authenticate,
                                 login, logout, get_user_model)
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
        context['projects'] = profile_user.get_user_projects()
        context['jobs'] = profile_user.get_user_jobs()
        context['skills'] = profile_user.get_user_skills()
        return context


class ApplicationsListView(generic.TemplateView):
    """List applications for a users projects
    this view can be called from several urls filtering the
    applications according to the url parameters
    - by project
    - by status
    - by project need
    """
    template_name = "accounts/applications.html"

    def get_context_data(self, **kwargs):
        """get context data to fill the template
        - distinguish between request user and other users
        - consider url parameters
        """
        context = super().get_context_data(**kwargs)
        profile_user = self.request.user
        context['profile_user'] = profile_user

        if 'status' in kwargs:
            applications = \
                teambuilder_models.Application.objects.applications_for_a_users_projects_per_status(
                    profile_user,
                    status=kwargs['status']
                )
        elif 'need_pk' in kwargs:
            need_pk = int(kwargs['need_pk'])
            context['need_pk'] = need_pk
            applications = \
                teambuilder_models.Application.objects.applications_for_a_users_projects_per_need(
                    profile_user,
                    need_pk=need_pk
                )
        elif 'project_pk' in kwargs:
            project_pk = int(kwargs['project_pk'])
            context['project_pk'] = project_pk
            applications = \
                teambuilder_models.Application.objects.applications_for_a_users_projects_per_project(
                    profile_user,
                    project_pk=project_pk
                )
        else:
            applications = \
                teambuilder_models.Application.objects.applications_for_a_users_projects(
                    profile_user
                )
        context['applications'] = applications

        context['status'] = list(teambuilder_models.ApplicationStatus)

        # enum type do not work in Django templates
        context['application_status_undecided'] \
            = teambuilder_models.ApplicationStatus.Undecided.value

        context['projects'] = profile_user.get_user_projects()
        context['needs'] = profile_user.get_user_projects_needs()

        return context


@login_required
def approve_application(request, application_pk):
    """approving a users application
    - the applicant receives an email notification"""
    application = get_object_or_404(teambuilder_models.Application, pk=application_pk)
    developer = application.applicant
    application.approve()
    email.send_email(
        'Your application was approved!',
        '''Hello {}!
        Thank you for your application to {} as {}.
        We are happy to inform you that your application has been
        accepted. We will soon get in touch with you regarding
        the details of this job. With regards, {}'''
            .format(developer, application.position.project,
                    application.position.skill, application.position.project.owner),
        [developer.email],
    )
    return HttpResponseRedirect(reverse_lazy(
        'accounts:applications'))


@login_required
def reject_application(request, application_pk):
    """rejecting a users application
    - the applicant receives an email notification
    """
    application = get_object_or_404(teambuilder_models.Application, pk=application_pk)
    developer = application.applicant
    application.reject()
    email.send_email(
        'Your application was rejected!',
        '''Hello {}!
        Thank you for your application to {} as {}.
        Unfortunately we could not consider your application.
        The position has been filled. With regards, {}'''
            .format(developer,
                    application.position.project,
                    application.position.skill,
                    application.position.project.owner),
        [developer.email],
    )
    return HttpResponseRedirect(reverse_lazy(
        'accounts:applications'))


@login_required
def profile_edit_view(request):
    """
    Allows a user to update his own profile.
    """
    user = request.user
    skills = request.user.get_user_skills()
    jobs = request.user.get_user_jobs()
    projects = request.user.get_user_projects()

    skills_initial_data = [{'skill': skill}
                    for skill in skills]

    if request.method == 'POST':

        profile_form = forms.ProfileForm(request.POST, request.FILES, instance=request.user)
        skills_formset = forms.SkillsFormSet(request.POST, prefix='fs_skills')

        if profile_form.is_valid() and skills_formset.is_valid():
            # save profile form
            profile_form.save()

            # skills: save set of skills
            new_skills = [skill_form.cleaned_data.get('skill')
                              for skill_form in skills_formset
                              if not skill_form.cleaned_data.get('DELETE')
                              and skill_form.cleaned_data.get('skill')]
            user.skills.clear()
            if new_skills:
                new_skills_set = set(new_skills)
                user.skills.add(*new_skills)
            user.save()

            return HttpResponseRedirect(reverse_lazy('accounts:profile'))
    else:
        profile_form = forms.ProfileForm(instance=request.user)
        skills_formset = forms.SkillsFormSet(
            initial=skills_initial_data,
            prefix='fs_skills')

    return render(request, 'accounts/profile_edit.html', {
        'profile_form': profile_form,
        'skills_formset': skills_formset,
        'jobs': jobs,
        'projects': projects
    })