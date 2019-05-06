from core_resources.models import User, Project, MergeRequest, Commit, Issue
from core_resources.proto import APIV1_pb2 as API
from django.http import HttpResponse
from django.conf import settings


class APIResponse:

    @staticmethod
    def api_response_get(data):
        return HttpResponse(data.SerializeToString())

    @staticmethod
    def api_response_post(data):
        return HttpResponse(data.SerializeToString(), content_type="application/octet-stream")

    @staticmethod
    def api_error_response(status_code, message):
        error = API.Error()
        error.status_code = status_code
        error.message = message
        return HttpResponse(error.SerializeToString(), status=status_code, content_type="application/octet-stream")


class APIConverter:

    @staticmethod
    def convert_to_pb_user(db_user, **kwargs):
        pb_user = API.User()
        pb_user.id = db_user.id
        pb_user.name = db_user.name
        pb_user.username = db_user.username
        pb_user.email = db_user.email
        pb_user.state = db_user.user_state
        pb_user.avatar_url = db_user.avatar_url
        pb_user.web_url = db_user.web_url
        pb_user.is_admin = db_user.is_admin
        pb_user.created_at.FromSeconds(db_user.created_at)

        # Projects
        aux_projects = []
        db_projects = db_user.projects.all()

        for db_project in db_projects:
            pb_project = APIConverter.convert_to_pb_project(db_project)
            aux_projects.append(pb_project)

        pb_user.projects.extend(aux_projects)

        if 'extra' in kwargs and kwargs['extra']:
            # Issues
            aux_issues = []

            if 'all' in kwargs and kwargs['all']:
                db_issues = Issue.objects.filter(_author=db_user).order_by('-_closed_at')
            else:
                db_issues = Issue.objects.filter(_author=db_user).order_by('-_closed_at')[:5]

            for db_issue in db_issues:
                pb_issue = APIConverter.convert_to_pb_issue(db_issue)
                aux_issues.append(pb_issue)

            pb_user.issues.extend(aux_issues)

            # Commits
            aux_commits = []

            if 'all' in kwargs and kwargs['all']:
                db_commits = Commit.objects.filter(_author=db_user).order_by('-_authored_date')
            else:
                db_commits = Commit.objects.filter(_author=db_user).order_by('-_authored_date')[:5]

            for db_commit in db_commits:
                pb_commit = APIConverter.convert_to_pb_commit(db_commit)
                aux_commits.append(pb_commit)

            pb_user.commits.extend(aux_commits)

            # Merge Requests
            aux_merge_requests = []

            if 'all' in kwargs and kwargs['all']:
                db_merge_requests = MergeRequest.objects.filter(_author=db_user).order_by('-_created_at')
            else:
                db_merge_requests = MergeRequest.objects.filter(_author=db_user).order_by('-_created_at')[:5]

            for db_merge_request in db_merge_requests:
                pb_merge_request = APIConverter.convert_to_pb_merge_request(db_merge_request)
                aux_merge_requests.append(pb_merge_request)

            pb_user.merge_requests.extend(aux_merge_requests)

        return pb_user

    @staticmethod
    def convert_to_pb_project(db_project, **kwargs):
        pb_project = API.Project()
        pb_project.id = db_project.id
        pb_project.name = db_project.name
        pb_project.name_with_namespace = db_project.name_with_namespace
        pb_project.description = db_project.description
        pb_project.default_branch = db_project.default_branch
        pb_project.visibility = db_project.visibility
        pb_project.web_url = db_project.web_url
        pb_project.avatar_url = db_project.avatar_url
        pb_project.created_at.FromSeconds(db_project.created_at)

        return pb_project

    @staticmethod
    def convert_to_pb_commit(db_commit, **kwargs):
        pb_commit = API.Commit()
        pb_commit.id = db_commit.id
        pb_commit.project_id = db_commit.project_id
        pb_commit.title = db_commit.title
        if db_commit.committer_id:
            pb_commit.committer_id = db_commit.committer_id
        pb_commit.committed_date.FromSeconds(db_commit.committed_date)
        pb_commit.message = db_commit.message
        pb_commit.created_at.FromSeconds(db_commit.created_at)

        return pb_commit

    @staticmethod
    def convert_to_pb_issue(db_issue, **kwargs):
        pb_issue = API.Issue()
        pb_issue.id = db_issue.id
        pb_issue.project_id = db_issue.project_id
        pb_issue.title = db_issue.title
        pb_issue.state = db_issue.issue_state
        pb_issue.description = db_issue.description
        if db_issue.author_id:
            pb_issue.author_id = db_issue.author_id
        pb_issue.web_url = db_issue.web_url
        pb_issue.closed_at.FromSeconds(db_issue.closed_at)
        pb_issue.created_at.FromSeconds(db_issue.created_at)

        return pb_issue

    @staticmethod
    def convert_to_pb_merge_request(db_merge_request, **kwargs):
        pb_merge_request = API.MergeRequest()
        pb_merge_request.id = db_merge_request.id
        pb_merge_request.project_id = db_merge_request.project_id
        pb_merge_request.title = db_merge_request.title
        pb_merge_request.description = db_merge_request.description
        pb_merge_request.state = db_merge_request.merge_state
        if db_merge_request.author_id:
            pb_merge_request.author_id = db_merge_request.author_id
        pb_merge_request.web_url = db_merge_request.web_url
        pb_merge_request.created_at.FromSeconds(db_merge_request.created_at)

        if db_merge_request.merged_at:
            pb_merge_request.merged_at.FromSeconds(db_merge_request.merged_at)

        return pb_merge_request

    @staticmethod
    def convert_to_pb_group(db_group, **kwargs):
        pb_group = API.Group()
        pb_group.id = db_group.id
        pb_group.name = db_group.name
        pb_group.description = db_group.description
        pb_group.visibility = db_group.visibility
        pb_group.web_url = db_group.web_url

        return pb_group

    @staticmethod
    def convert_to_pb_branch(db_branch, **kwargs):
        pb_branch = API.Branch()
        pb_branch.id = db_branch.id
        pb_branch.name = db_branch.name
        pb_branch.can_push = db_branch.can_push

        return pb_branch

