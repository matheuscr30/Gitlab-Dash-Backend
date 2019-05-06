from core_resources.models import User, Project
from django.db import models
from dateutil import parser


class Issue(models.Model):
    _project = models.ForeignKey(Project, on_delete=models.CASCADE, null=True)
    _title = models.CharField(max_length=250)
    _issue_state = models.CharField(max_length=250)
    _description = models.TextField(blank=True, default='')
    _author = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    _web_url = models.CharField(max_length=250)
    _closed_at = models.DateTimeField()
    _created_at = models.DateTimeField()

    def __str__(self):
        return self._title

    def __unicode__(self):
        return '/%s/' % self._title

    # <editor-fold desc="Setter and Getter">
    @property
    def project(self):
        return self._project

    @project.setter
    def project(self, value):
        self._project = value

    @property
    def project_id(self):
        return self._project_id

    @project_id.setter
    def project_id(self, value):
        self._project_id = value

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, value):
        self._title = value

    @property
    def issue_state(self):
        return self._issue_state

    @issue_state.setter
    def issue_state(self, value):
        self._issue_state = value

    @property
    def description(self):
        return self._description

    @description.setter
    def description(self, value):
        self._description = value

    @property
    def author(self):
        return self._author

    @author.setter
    def author(self, value):
        self._author = value

    @property
    def author_id(self):
        return self._author_id

    @author_id.setter
    def author_id(self, value):
        self._author_id = value

    @property
    def web_url(self):
        return self._web_url

    @web_url.setter
    def web_url(self, value):
        self._web_url = value

    @property
    def closed_at(self):
        return int(self._closed_at.timestamp())

    @closed_at.setter
    def closed_at(self, value):
        self._closed_at = parser.parse(value)

    @property
    def created_at(self):
        return int(self._created_at.timestamp())

    @created_at.setter
    def created_at(self, value):
        self._created_at = parser.parse(value)
    # </editor-fold>
