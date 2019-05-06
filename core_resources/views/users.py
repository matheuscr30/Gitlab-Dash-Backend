from core_resources.helpers.api_library import APIResponse, APIConverter
from oauth2_provider.decorators import protected_resource
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from core_resources.proto import APIV1_pb2 as API
from core_resources.models import User
from django.views import View


@method_decorator(protected_resource(), name='dispatch')
@method_decorator(csrf_exempt, name='dispatch')
class UsersView(View):

    def get(self, request, *args, **kwargs):
        all = request.GET.get('all', None)

        # Get By Id
        if 'user_id' in kwargs:
            user_id = kwargs['user_id']

            if User.objects.filter(pk=user_id):
                db_user = User.objects.get(pk=user_id)
                pb_user = APIConverter.convert_to_pb_user(db_user, all=all, extra=True)
                return APIResponse.api_response_get(pb_user)
            else:
                return APIResponse.api_error_response(404, 'Does Not Exist User')
        else:
            db_users = User.objects.all()
            pb_user_list = API.UserList()

            aux_users = []
            for db_user in db_users:
                pb_user = APIConverter.convert_to_pb_user(db_user, all=all, extra=True)
                aux_users.append(pb_user)

            pb_user_list.users.extend(aux_users)

            return APIResponse.api_response_get(pb_user_list)
