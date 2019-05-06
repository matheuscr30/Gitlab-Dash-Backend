from .models import User, Project, Commit, MergeRequest, Issue, Group, Branch
from django.contrib import admin


class UserAdmin(admin.ModelAdmin):
    list_display = ('id', '_username', '_email', '_name', '_user_state')
    search_fields = ('_username', '_email', '_name', '_user_state')


class ProjectAdmin(admin.ModelAdmin):
    list_display = ('id', '_description', '_name', '_name_with_namespace')
    search_fields = ('_description', '_name', '_name_with_namespace')


class CommitAdmin(admin.ModelAdmin):
    list_display = ('id', '_title', '_message', '_committer')
    search_fields = ('_title', '_message', '_committer__username', '_committer__email', '_project__name')


class MergeRequestAdmin(admin.ModelAdmin):
    list_display = ('id', '_title', '_description', '_merge_state', '_author', '_project')
    search_fields = ('_title', '_description', '_author__username', '_author__email', '_project__name')


class IssueAdmin(admin.ModelAdmin):
    list_display = ('id', '_title', '_description', '_issue_state', '_author', '_project')
    search_fields = ('_title', '_description', '_author__username', '_author__email', '_project__name')


class GroupAdmin(admin.ModelAdmin):
    list_display = ('id', '_name', '_description', '_visibility', '_web_url')
    search_fields = ('_name', '_description', '_visibility')


class BranchAdmin(admin.ModelAdmin):
    list_display = ('id', '_name', '_can_push')
    search_fields = ('_name', '_can_push')


admin.site.register(User, UserAdmin)
admin.site.register(Project, ProjectAdmin)
admin.site.register(Commit, CommitAdmin)
admin.site.register(MergeRequest, MergeRequestAdmin)
admin.site.register(Issue, IssueAdmin)
admin.site.register(Group, GroupAdmin)
admin.site.register(Branch, BranchAdmin)
