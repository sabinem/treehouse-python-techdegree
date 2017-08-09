"""teambuilder views"""
from django.http import HttpResponseRedirect, HttpResponse
from django import forms
from django.shortcuts import get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.core.urlresolvers import reverse_lazy
from django.views import generic
from django.db.models import ProtectedError
from django.contrib.auth import get_user_model
from django.db import IntegrityError

from accounts import email
from . import models, forms


User = get_user_model()


class ProjectListView(generic.TemplateView):
    """List all projects"""
    template_name = "teambuilder/projects.html"

    def get_context_data(self, **kwargs):
        """gets data for the view"""
        context = super().get_context_data(**kwargs)
        context['skills'] = models.Skill.objects.all()
        print(kwargs)
        if 'need_pk' in kwargs:
            need_pk = int(kwargs['need_pk'])
            context['need_pk'] = int(need_pk)
            context['positions'] = models.Position.objects.get_positons_by_skill(
                skill_pk=need_pk
            )
        elif 'term' in kwargs:
            term = kwargs['term']
            project_ids = models.Project.objects.get_by_searchterm(searchterm=term)
            context['term'] = term
            context['positions'] = models.Position.objects.get_positons_by_project_ids(project_ids=project_ids)
        else:
            context['positions'] = models.Position.objects.all()
        return context


class ProjectDetailView(generic.TemplateView):
    """Detail for one project"""
    template_name = "teambuilder/project.html"

    def get_context_data(self, **kwargs):
        """fetching data for display"""
        context = super().get_context_data(**kwargs)
        project = get_object_or_404(
            models.Project, id=kwargs['project_pk'])
        context['project'] = project
        if self.request.user.is_authenticated:
            context['positions_applied'] =\
                models.Position.objects.get_positions_for_project_where_user_applied(
                    project=project,
                    user=self.request.user)
            context['positions_not_applied'] =\
                models.Position.objects.get_positions_for_project_where_user_did_not_apply(
                    project=project,
                    user=self.request.user)
        else:
            context['positions'] = \
                models.Position.objects.get_positons_by_project(project_pk=project.id)
        context['needs'] = project.get_project_needs()
        return context


@login_required
def project_delete(request, project_pk):
    """deleting a project if it has no positions"""
    project = get_object_or_404(models.Project, pk=project_pk)
    if request.user != project.owner:
        messages.add_message(
            request, messages.ERROR,
            'You are not the owner of this project'
        )
        return HttpResponseRedirect(reverse_lazy(
            'teambuilder:project', kwargs={'project_pk': project_pk}))
    try:
        project.delete()
    except ProtectedError:
        messages.add_message(
            request, messages.ERROR,
            'You cannot delete a project, that has positions.'
            ' First edit the project and delete its postions.'
        )
        return HttpResponseRedirect(reverse_lazy(
            'teambuilder:project', kwargs={'project_pk': project_pk}))
    else:
        messages.add_message(request, messages.INFO, 'The project has been deleted.')
        return HttpResponseRedirect(reverse_lazy(
           'teambuilder:projects'))


@login_required
def position_apply(request, position_pk):
    """handeling the application of the request user
    to a position"""
    position = get_object_or_404(models.Position, pk=position_pk)
    try:
        position.apply(request.user)
    except IntegrityError as e:
        messages.add_message(request, messages.ERROR, e)
        return HttpResponseRedirect(reverse_lazy(
            'teambuilder:project', kwargs={'project_pk': position.project_id}))
    else:
        email.send_email(
            'We received your application!',
            '''Hello {}!
            Thank you for your application to {} as {}, you will hear from the project owner
            {} soon.'''
                .format(request.user.name, position.project, position.skill, position.project.owner),
            [request.user.email],
        )
        messages.add_message(request, messages.INFO,
                             'Thank you for applying. '
                             'We have send you an email confirmation!')
        return HttpResponseRedirect(reverse_lazy(
            'teambuilder:project', kwargs={'project_pk': position.project_id}))


@login_required
def project_edit_view(request, project_pk):
    """Editing a project
    and its positions"""
    project = get_object_or_404(models.Project, pk=project_pk)
    if request.user != project.owner:
        messages.add_message(
            request, messages.ERROR,
            'You are not the owner of this project'
        )
        return HttpResponseRedirect(reverse_lazy(
            'teambuilder:project', kwargs={'project_pk': project_pk}))
    if request.method == 'POST':
        formset = forms.ProjectWithPositionsFormSet(request.POST, instance=project)
        projectform = forms.ProjectForm(request.POST, instance=project)
        if formset.is_valid() and projectform.is_valid():
            projectform.save()
            for form in formset:
            formset.save()
            return HttpResponseRedirect(
                reverse_lazy('teambuilder:project',
                             kwargs={'project_pk': project.id}))
    else:
        formset = forms.ProjectWithPositionsFormSet(instance=project)
        projectform = forms.ProjectForm(instance=project)
    return render(request, 'teambuilder/project_edit.html', {
        'projectform': projectform,
        'formset': formset,
    })


@login_required
def project_create_view(request):
    """Creating a project
    and its positions"""
    user = request.user
    if request.method == 'POST':
        formset = forms.NewPositionsFormset(request.POST)
        projectform = forms.ProjectForm(request.POST)
        if formset.is_valid() and projectform.is_valid():
            project = projectform.save(commit=False)
            project.owner = user
            project.save()
            for form in formset:
                if 'skill' in form.cleaned_data:
                    models.Position.objects.create(
                        project=project,
                        skill=form.cleaned_data['skill'],
                        description=form.cleaned_data['description']
                    )

            return HttpResponseRedirect(
                reverse_lazy('teambuilder:project',
                             kwargs={'project_pk': project.id}))
    else:
        formset = forms.NewPositionsFormset()
        projectform = forms.ProjectForm()

    return render(request, 'teambuilder/project_new.html', {
        'formset': formset,
        'projectform': projectform
    })


