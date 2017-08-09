"""
models for the teambuilder app
"""
from enum import Enum

from django.db import models
from django.db.models import Q
from django.conf import settings
from django.db import IntegrityError


class ApplicationStatus(Enum):
    Undecided = '0'
    Approved = 'a'
    Rejected = 'r'


def get_choices(cls):
    """gets the choices from an Enum as lists of tuples with name and value:
    [('m', male), ('f', 'female)]
    """
    return [(x.value, x.name) for x in cls]


class SkillManager(models.Manager):
    """Skill manager"""
    def get_project_needs(self, project_pk):
        """get all skills needed in a project"""
        positions = Position.objects.get_positons_by_project(project_pk=project_pk)
        return self.filter(id__in=positions.values('skill_id'))

    def get_project_needs_for_users_projects(self, user):
        project_ids = user.get_user_project_ids()
        positions = Position.objects.get_positons_by_project_ids(project_ids=project_ids)
        return \
            self.filter(id__in=positions.values('skill_id'))


class Skill(models.Model):
    skill = models.CharField('Skill', max_length=255)
    need = models.CharField('Need', max_length=255, blank=True)

    objects = SkillManager()

    def __str__(self):
        return self.skill

    def get_openings(self):
        return self.positions.all()


class ProjectManager(models.Manager):
    def get_by_searchterm(self, searchterm=None):
        if searchterm:
            return self.filter(
                Q(title__icontains=searchterm) | Q(description__icontains=searchterm)).values_list('id', flat=True)

    def get_projects_by_skill(self, skill_pk):
        positions = Position.objects.get_positons_by_skill(skill_pk=skill_pk)
        return self.filter(id__in=positions.values('project_id'))

    def get_projects_needs(self, projects):
        positions = Position.objects.filter(project__in=projects)
        return set([position.skill for position in positions])


class Project(models.Model):
    """Projects are owned by a user"""
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="projects")
    title = models.CharField('Title', max_length=255)
    description = models.TextField()
    project_timeline = models.TextField()
    applicant_requirements = models.TextField()
    link = models.URLField(blank=True)
    objects = ProjectManager()

    def __str__(self):
        return self.title

    def get_positions(self):
        return self.positions.all()

    def get_project_needs(self):
        return set([position.skill for position in self.get_positions()])


class PositionManager(models.Manager):
    def get_positions_by_developer(self, user):
        return self.select_related('project')\
            .filter(developer=user, open=False)

    def get_positons_by_skill(self, skill_pk):
        return self.select_related('project')\
            .filter(skill_id=skill_pk)

    def get_positons_by_project(self, project_pk):
        return self.select_related('skill')\
            .filter(project_id=project_pk)

    def get_positons_by_project_ids(self, project_ids):
        return self.select_related('skill')\
            .filter(project_id__in=project_ids)

    def get_open_positons_by_skill(self, skill):
        return self.select_related('project')\
            .filter(skill=skill, open=False)

    def get_open_positons_by_skill_set(self, skills):
        return self.select_related('project')\
            .filter(skill__in=skills, open=False)

    def positions_for_user(self, user):
        return self.filter(project__owner=user).select_related('Project')

    def get_positions_for_project_where_user_applied(self, project, user):
        position_ids_for_user = Application.objects.position_ids_where_user_applied(user)
        return self.filter(project=project, id__in=position_ids_for_user)

    def get_positions_for_project_where_user_did_not_apply(self, project, user):
        position_ids_for_user = Application.objects.position_ids_where_user_applied(user)
        return self.filter(project=project).exclude(id__in=position_ids_for_user)


class Position(models.Model):
    """Projects offer positions that require a skill
    they demand an involvement of hours per week"""
    project = models.ForeignKey(
        Project,
        related_name='positions',
        on_delete=models.PROTECT)
    developer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        blank=True,
        null=True,
        related_name='jobs')
    description = models.TextField()
    skill = models.ForeignKey(
        Skill, related_name='demands',
        on_delete=models.PROTECT)
    open = models.BooleanField(default=True)
    objects = PositionManager()

    def __str__(self):
        return "{} {}".format(self.project, self.skill)

    def apply(self, applicant):
        if self.project.owner == applicant:
            raise IntegrityError("You can not apply to your own project!")
        if self.skill not in applicant.get_skills():
            raise IntegrityError(
                "You can not apply to a position when you do not have "
                "the required skill! For this position you need to be a {}".format(self.skill))
        application, created = Application.objects.get_or_create(
            applicant=applicant, position=self)
        application.save()
        return application

    def fill(self, applicant):
        self.open = False
        self.developer = applicant
        self.save()

    def get_candidates(self):
        return self.candidates

    def test_candidate(self, user):
        return user in self.get_candidates()

    def has_applications(self):
        return self.candidates.count() != 0


class ApplicationManager(models.Manager):
    def get_applicants_for_position(self, position_pk, status=None):
        qs = self.select_related('applicant', 'position__project__owner', 'position').filter(position_id=position_pk)
        if status:
            qs.filter(status=status)
        return qs

    def application_for_user_and_position(self, user, position):
        return self.filter(applicant=user, position=position).exists()

    def application_for_user_and_skill_exists(self, user, skill_pk):
        return self.filter(applicant=user, position__skill_id=skill_pk).exists()

    def get_applicants_by_status(self, status):
        return self.select_related('applicant').filter(status=status)

    def applications_for_a_users_projects(self, user):
        applications = self.filter(position__project__owner=user)\
            .select_related('position', 'applicant', 'position__project', 'position__skill')
        return applications

    def applications_for_a_users_projects_per_status(self, user, status):
        applications = self.filter(position__project__owner=user, status=status)\
            .select_related('position', 'applicant', 'position__project', 'position__skill')
        return applications

    def applications_for_a_users_projects_per_need(self, user, need_pk):
        applications = self.filter(position__project__owner=user, position__skill_id=need_pk)\
            .select_related('position', 'applicant', 'position__project', 'position__skill')
        return applications

    def applications_for_a_users_projects_per_project(self, user, project_pk):
        applications = self.filter(position__project__owner=user, position__project_id=project_pk)\
            .select_related('position', 'applicant', 'position__project', 'position__skill')
        return applications

    def applications_for_a_project(self, user):
        applications = self.filter(position__project__owner=user).select_related('position', 'applicant')
        return applications

    def position_ids_where_user_applied(self, user):
        return self.filter(applicant=user).values_list('position_id', flat=True)


class Application(models.Model):
    """Users can apply for Positions"""
    applicant = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="applications")
    position = models.ForeignKey(Position, related_name="candidates")
    status = models.CharField(
        choices=get_choices(ApplicationStatus),
        max_length=1,
        default=ApplicationStatus.Undecided.value)
    objects = ApplicationManager()

    def __str__(self):
        return "{} for {}".format(self.applicant, self.position)

    def approve(self):
        self.status = ApplicationStatus.Approved.value
        self.position.fill(applicant=self.applicant)
        self.save()

    def reject(self):
        self.status = ApplicationStatus.Rejected.value
        self.save()
