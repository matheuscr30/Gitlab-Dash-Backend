from core_resources.models import Project
from django.db import models


class Branch(models.Model):
    _project = models.ForeignKey(Project, on_delete=models.CASCADE, null=True)
    _name = models.CharField(max_length=250)
    _can_push = models.BooleanField()

    class Meta:
        verbose_name_plural = 'Branches'

    def __str__(self):
        return self._name

    def __unicode__(self):
        return '/%s/' % self._name

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
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    @property
    def can_push(self):
        return self._can_push

    @can_push.setter
    def can_push(self, value):
        self._can_push = value
    # </editor-fold>
