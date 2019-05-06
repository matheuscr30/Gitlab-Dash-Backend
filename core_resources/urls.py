from django.views.decorators.csrf import csrf_exempt
from oauth2_provider.views import TokenView
from core_resources import views
from django.urls import path

urlpatterns = [
    path('o/token/', csrf_exempt(TokenView.as_view()), name='token'),

    path('users/', views.UsersView.as_view(), name='users'),
    path('users/<int:user_id>/', views.UsersView.as_view(), name='specific_user'),

    path('groups/', views.GroupsView.as_view(), name='groups'),
    path('groups/<int:group_id>', views.GroupsView.as_view(), name='specific_group'),

    path('issues/', views.IssuesView.as_view(), name='issues'),
    path('issues/<int:issue_id>', views.IssuesView.as_view(), name='specific_issue'),

    path('projects/', views.ProjectsView.as_view(), name='projects'),
    path('projects/<int:project_id>/', views.ProjectsView.as_view(), name='specific_project'),
    path('projects/<int:project_id>/members/', views.ProjectMembersView.as_view(), name='members_specific_project'),
    path('projects/<int:project_id>/issues/', views.ProjectIssuesView.as_view(), name='issues_specific_project'),
    path('projects/<int:project_id>/commits/', views.ProjectCommitsView.as_view(), name='commits_specific_project'),
    path('projects/<int:project_id>/branches/', views.ProjectBranchesView.as_view(), name='commits_specific_branch')
]
