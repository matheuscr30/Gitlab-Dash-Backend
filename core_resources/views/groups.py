from core_resources.helpers.api_library import APIResponse, APIConverter
from oauth2_provider.decorators import protected_resource
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from core_resources.proto import APIV1_pb2 as API
from core_resources.models import Group
from django.views import View


@method_decorator(protected_resource(), name='dispatch')
@method_decorator(csrf_exempt, name='dispatch')
class GroupsView(View):

    def get(self, request, *args, **kwargs):
        # Get By Id
        if 'group_id' in kwargs:
            group_id = kwargs['group_id']

            if Group.objects.filter(pk=group_id):
                db_group = Group.objects.get(pk=group_id)
                pb_group = APIConverter.convert_to_pb_group(db_group)
                return APIResponse.api_response_get(pb_group)
            else:
                return APIResponse.api_error_response(404, 'Does Not Exist Group')
        else:
            db_groups = Group.objects.all()
            pb_group_list = API.GroupList()

            aux_groups = []
            for db_group in db_groups:
                pb_group = APIConverter.convert_to_pb_group(db_group)
                aux_groups.append(pb_group)

            pb_group_list.groups.extend(aux_groups)

            return APIResponse.api_response_get(pb_group_list)
