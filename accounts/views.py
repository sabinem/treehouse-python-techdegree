
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.core.urlresolvers import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.views import generic
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model

from teambuilder import models as teambuilder_models

from . import forms


User = get_user_model()

class LoginView(generic.FormView):
    form_class = forms.UserLoginForm
    success_url = reverse_lazy("teambuilder:projects")
    template_name = "accounts/signin.html"

    def form_valid(self, form):
        user = authenticate(
            email=form.cleaned_data['email'],
            password=form.cleaned_data['password']
        )
        login(self.request, user)
        return super().form_valid(form)


class LogoutView(generic.RedirectView):
    url = reverse_lazy("teambuilder:projects")

    def get(self, request, *args, **kwargs):
        logout(request)
        return super().get(request, *args, **kwargs)


class RegisterView(SuccessMessageMixin, generic.CreateView):
    form_class = forms.UserCreateForm
    template_name = "accounts/signup.html"

    def form_valid(self, form):
        form.save()
        user = authenticate(
            email=form.cleaned_data['email'],
            password=form.cleaned_data['password1']
        )
        login(self.request, user)
        return HttpResponseRedirect(reverse_lazy("accounts:profile"))


class ProfileView(generic.TemplateView):
    template_name = "accounts/profile.html"

    def get_context_data(self, **kwargs):
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
    Allows a user to update their own profile.
    """
    user = request.user
    skills = request.user.get_skills()
    jobs = request.user.get_jobs()
    projects = request.user.get_projects()

    # This is used as initial data.
    skills_initial_data = [{'skill': skill}
                    for skill in skills]
    projects_initial_data = [{'title': project.title, 'link': project.link, 'id':project.id}
                  for project in projects]
    print(projects_initial_data)

    if request.method == 'POST':

        profile_form = forms.ProfileForm(request.POST, request.FILES, instance=request.user)
        skills_formset = forms.SkillsFormSet(request.POST, prefix='fs_skills')
        projects_formset = forms.ProjectsFormSet(request.POST, prefix='fs_projects')

        if profile_form.is_valid() and skills_formset.is_valid() and projects_formset.is_valid():
            # Save user info
            profile_form.save()
            # Now save the data for each form in the formset
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
    template_name = "accounts/applications.html"

    def get_context_data(self, **kwargs):
        print("HELLO")
        if 'profile_pk' in kwargs:
            profile_user = get_object_or_404(User, pk=kwargs['profile_pk'])
        else:
            profile_user = self.request.user

        context = super().get_context_data(**kwargs)

        context['profile_user'] = profile_user
        context['status'] = list(teambuilder_models.ApplicationStatus)
        context['projects'] = profile_user.get_projects()
        context['applications'] = teambuilder_models.Application.objects.applications_for_user(profile_user)
        #context['needs'] = models.Skill.objects.needs_for_user(user)
        return context
