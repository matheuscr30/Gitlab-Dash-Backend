from core_resources.models import User, Project
from django.db import models
from dateutil import parser


class Commit(models.Model):
    id = models.CharField(max_length=250, primary_key=True)
    _project = models.ForeignKey(Project, on_delete=models.CASCADE, null=True)
    _title = models.CharField(max_length=250)
    _committer = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    _committed_date = models.DateTimeField()
    _message = models.TextField(blank=True, default='')
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
    def committer(self):
        return self._committer

    @committer.setter
    def committer(self, value):
        self._committer = value

    @property
    def committer_id(self):
        return self._committer_id

    @committer_id.setter
    def committer_id(self, value):
        self._committer_id = value

    @property
    def committed_date(self):
        return int(self._committed_date.timestamp())

    @committed_date.setter
    def committed_date(self, value):
        self._committed_date = parser.parse(value)

    @property
    def message(self):
        return self._message

    @message.setter
    def message(self, value):
        self._message = value

    @property
    def created_at(self):
        return int(self._created_at.timestamp())

    @created_at.setter
    def created_at(self, value):
        self._created_at = parser.parse(value)
    # </editor-fold>
