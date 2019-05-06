from core_resources.helpers.api_library import APIResponse, APIConverter
from core_resources.models import Project, User, Commit, Issue, Branch
from oauth2_provider.decorators import protected_resource
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from core_resources.proto import APIV1_pb2 as API
from django.views import View


@method_decorator(protected_resource(), name='dispatch')
@method_decorator(csrf_exempt, name='dispatch')
class ProjectsView(View):

    def get(self, request, *args, **kwargs):
        # Get By Id
        if 'project_id' in kwargs:
            project_id = kwargs['project_id']

            if Project.objects.filter(pk=project_id):
                db_project = Project.objects.get(pk=project_id)
                pb_project = APIConverter.convert_to_pb_project(db_project)
                return APIResponse.api_response_get(pb_project)
            else:
                return APIResponse.api_error_response(404, 'Does Not Exist Project')
        else:
            db_projects = Project.objects.all()
            pb_project_list = API.ProjectList()

            aux_projects = []
            for db_project in db_projects:
                pb_project = APIConverter.convert_to_pb_project(db_project, all=all)
                aux_projects.append(pb_project)

            pb_project_list.projects.extend(aux_projects)

            return APIResponse.api_response_get(pb_project_list)


@method_decorator(protected_resource(), name='dispatch')
@method_decorator(csrf_exempt, name='dispatch')
class ProjectMembersView(View):

    def get(self, request, *args, **kwargs):
        if not 'project_id' in kwargs:
            return APIResponse.api_error_response(400, 'Invalid Parameters')

        project_id = kwargs['project_id']

        if Project.objects.filter(pk=project_id):
            pb_user_list = API.UserList()

            db_users = User.objects.filter(_projects__pk=project_id)
            if len(db_users) > 0:
                aux_users = []
                for db_user in db_users:
                    pb_user = APIConverter.convert_to_pb_user(db_user)
                    aux_users.append(pb_user)

                pb_user_list.users.extend(aux_users)

            return APIResponse.api_response_get(pb_user_list)
        else:
            return APIResponse.api_error_response(404, 'Does Not Exist Project')


@method_decorator(protected_resource(), name='dispatch')
@method_decorator(csrf_exempt, name='dispatch')
class ProjectIssuesView(View):

    def get(self, request, *args, **kwargs):
        state = request.GET.get('state', None)

        if not 'project_id' in kwargs:
            return APIResponse.api_error_response(400, 'Invalid Parameters')

        project_id = kwargs['project_id']

        if Project.objects.filter(pk=project_id):
            pb_issue_list = API.IssueList()

            if state:
                db_issues = Issue.objects.filter(_project__pk=project_id, _issue_state=state)
            else:
                db_issues = Issue.objects.filter(_project__pk=project_id)

            if len(db_issues) > 0:
                aux_issues = []
                for db_issue in db_issues:
                    pb_issue = APIConverter.convert_to_pb_issue(db_issue)
                    aux_issues.append(pb_issue)

                pb_issue_list.issues.extend(aux_issues)

            return APIResponse.api_response_get(pb_issue_list)
        else:
            return APIResponse.api_error_response(404, 'Does Not Exist Project')


@method_decorator(protected_resource(), name='dispatch')
@method_decorator(csrf_exempt, name='dispatch')
class ProjectCommitsView(View):

    def get(self, request, *args, **kwargs):
        if not 'project_id' in kwargs:
            return APIResponse.api_error_response(400, 'Invalid Parameters')

        project_id = kwargs['project_id']

        if Project.objects.filter(pk=project_id):
            pb_commit_list = API.CommitList()

            db_commits = Commit.objects.filter(_project__pk=project_id)
            if len(db_commits) > 0:
                aux_commits = []
                for db_commit in db_commits:
                    pb_commit = APIConverter.convert_to_pb_commit(db_commit)
                    aux_commits.append(pb_commit)

                pb_commit_list.commits.extend(aux_commits)

            return APIResponse.api_response_get(pb_commit_list)
        else:
            return APIResponse.api_error_response(404, 'Does Not Exist Project')


@method_decorator(protected_resource(), name='dispatch')
@method_decorator(csrf_exempt, name='dispatch')
class ProjectBranchesView(View):

    def get(self, request, *args, **kwargs):
        if not 'project_id' in kwargs:
            return APIResponse.api_error_response(400, 'Invalid Parameters')

        project_id = kwargs['project_id']

        if Project.objects.filter(pk=project_id):
            pb_branch_list = API.BranchList()

            db_branches = Branch.objects.filter(_project__pk=project_id)
            if len(db_branches) > 0:
                aux_branches = []
                for db_branch in db_branches:
                    pb_branch = APIConverter.convert_to_pb_branch(db_branch)
                    aux_branches.append(pb_branch)

                pb_branch_list.branches.extend(aux_branches)

            return APIResponse.api_response_get(pb_branch_list)
        else:
            return APIResponse.api_error_response(404, 'Does Not Exist Project')
