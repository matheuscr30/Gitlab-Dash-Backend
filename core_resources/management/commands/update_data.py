from core_resources.models import User, Project, Commit, Issue, MergeRequest, Group, Branch
from django.core.management.base import BaseCommand
from django.conf import settings
import gitlab

gl = gitlab.Gitlab(settings.GITLAB_BASE_URL, private_token=settings.GITLAB_ACCESS_TOKEN)


class Command(BaseCommand):
    def handle(self, *args, **options):
        projects = gl.projects.list()
        for project in projects:
            if not Project.objects.filter(pk=project.id):
                self.create_db_project(project)

        users = gl.users.list()
        for user in users:
            if not User.objects.filter(pk=user.id):
                self.create_db_user(user)

        groups = gl.groups.list()
        for group in groups:
            if not Group.objects.filter(pk=group.id):
                self.create_db_group(group)

        for project in projects:
            db_project = Project.objects.get(pk=project.id)

            members = project.members.list()
            for member in members:
                if User.objects.filter(pk=member.id):
                    db_user = User.objects.get(pk=member.id)
                    db_user.projects.add(db_project)
                    db_user.save()

            commits = project.commits.list(all=True)
            for commit in commits:
                if not Commit.objects.filter(pk=commit.id):
                    self.create_db_commit(commit, project)

            issues = project.issues.list(all=True, state='closed')
            for issue in issues:
                if not Issue.objects.filter(pk=issue.id):
                    self.create_db_issue(issue)

            merge_requests = project.mergerequests.list(all=True, state='opened')
            for merge_request in merge_requests:
                if not MergeRequest.objects.filter(pk=merge_request.id):
                    self.create_db_merge_request(merge_request)

            branches = project.branches.list()
            for branch in branches:
                if not Branch.objects.filter(_name=branch.name):
                    self.create_db_branch(branch, project)

    def create_db_user(self, user):
        db_user = User()
        db_user.id = user.id
        db_user.username = user.username
        db_user.email = user.email
        db_user.name = user.name
        db_user.user_state = user.state
        db_user.avatar_url = user.avatar_url
        db_user.web_url = user.web_url
        db_user.is_admin = user.is_admin
        db_user.created_at = user.created_at
        db_user.save()

    def create_db_project(self, project):
        db_project = Project()
        db_project.id = project.id
        if project.description is not None:
            db_project.description = project.description
        if project.default_branch is not None:
            db_project.default_branch = project.default_branch
        db_project.visibility = project.visibility
        db_project.web_url = project.web_url
        db_project.name = project.name
        db_project.name_with_namespace = project.name_with_namespace
        db_project.created_at = project.created_at
        db_project.save()

    def create_db_commit(self, commit, project):
        db_commit = Commit()
        db_commit.id = commit.id
        db_commit.title = commit.title
        db_commit.committed_date = commit.committed_date
        db_commit.message = commit.message
        db_commit.created_at = commit.created_at
        db_commit.project = Project.objects.get(pk=project.id)

        if User.objects.filter(_email=commit.committer_email):
            db_commit.committer = User.objects.get(_email=commit.committer_email)

        db_commit.save()

    def create_db_issue(self, issue):
        db_issue = Issue()
        db_issue.id = issue.id
        db_issue.title = issue.title
        db_issue.issue_state = issue.state
        if issue.description is not None:
            db_issue.description = issue.description
        db_issue.web_url = issue.web_url
        db_issue.closed_at = issue.closed_at
        db_issue.created_at = issue.created_at
        db_issue.project = Project.objects.get(pk=issue.project_id)

        if User.objects.filter(pk=issue.author['id']):
            db_issue.author = User.objects.get(pk=issue.author['id'])

        db_issue.save()

    def create_db_merge_request(self, merge_request):
        db_merge_request = MergeRequest()
        db_merge_request.id = merge_request.id
        db_merge_request.title = merge_request.title
        if merge_request.description is not None:
            db_merge_request.description = merge_request.description
        db_merge_request.merge_state = merge_request.state
        db_merge_request.web_url = merge_request.web_url
        db_merge_request.created_at = merge_request.created_at
        db_merge_request.project = Project.objects.get(pk=merge_request.project_id)

        if merge_request.merged_at:
            db_merge_request.merged_at = merge_request.merged_at

        if User.objects.filter(pk=merge_request.author['id']):
            db_merge_request.author = User.objects.get(pk=merge_request.author['id'])

        db_merge_request.save()

    def create_db_group(self, group):
        db_group = Group()
        db_group.id = group.id
        db_group.name = group.name
        if group.description is not None:
            db_group.description = group.description
        db_group.visibility = group.visibility
        db_group.web_url = group.web_url
        db_group.save()

    def create_db_branch(self, branch, project):
        db_branch = Branch()
        db_branch.name = branch.name
        db_branch.can_push = branch.can_push
        db_branch.project = Project.objects.get(pk=project.id)
        db_branch.save()
