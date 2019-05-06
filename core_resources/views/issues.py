from core_resources.helpers.api_library import APIResponse, APIConverter
from oauth2_provider.decorators import protected_resource
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from core_resources.proto import APIV1_pb2 as API
from core_resources.models import Issue
from django.views import View


@method_decorator(protected_resource(), name='dispatch')
@method_decorator(csrf_exempt, name='dispatch')
class IssuesView(View):

    def get(self, request, *args, **kwargs):
        state = request.GET.get('state', None)

        # Get By Id
        if 'issue_id' in kwargs:
            issue_id = kwargs['issue_id']

            if Issue.objects.filter(pk=issue_id):
                db_issue = Issue.objects.get(pk=issue_id)
                pb_issue = APIConverter.convert_to_pb_issue(db_issue)
                return APIResponse.api_response_get(pb_issue)
            else:
                return APIResponse.api_error_response(404, 'Does Not Exist Issue')
        else:
            if state:
                db_issues = Issue.objects.all()
            else:
                db_issues = Issue.objects.filter(_issue_state=state)

            pb_issue_list = API.IssueList()

            aux_issues = []
            for db_issue in db_issues:
                pb_issue = APIConverter.convert_to_pb_issue(db_issue, all=all)
                aux_issues.append(pb_issue)

            pb_issue_list.issues.extend(aux_issues)

            return APIResponse.api_response_get(pb_issue_list)
