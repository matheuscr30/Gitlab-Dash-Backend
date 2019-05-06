from django.db import models
from dateutil import parser


class Project(models.Model):
    _description = models.CharField(max_length=250)
    _default_branch = models.CharField(max_length=250, blank=True, default='')
    _visibility = models.CharField(max_length=250)
    _web_url = models.CharField(max_length=250)
    _avatar_url = models.CharField(max_length=250, blank=True, default='')
    _name = models.CharField(max_length=250)
    _name_with_namespace = models.CharField(max_length=250)
    _created_at = models.DateTimeField()

    def __str__(self):
        return self._name

    def __unicode__(self):
        return '/%s/' % self._name

    # <editor-fold desc="Setter and Getter">
    @property
    def description(self):
        return self._description

    @description.setter
    def description(self, value):
        self._description = value

    @property
    def default_branch(self):
        return self._default_branch

    @default_branch.setter
    def default_branch(self, value):
        self._default_branch = value

    @property
    def visibility(self):
        return self._visibility

    @visibility.setter
    def visibility(self, value):
        self._visibility = value

    @property
    def web_url(self):
        return self._web_url

    @web_url.setter
    def web_url(self, value):
        self._web_url = value

    @property
    def avatar_url(self):
        return self._avatar_url

    @avatar_url.setter
    def avatar_url(self, value):
        self._avatar_url = value

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    @property
    def name_with_namespace(self):
        return self._name_with_namespace

    @name_with_namespace.setter
    def name_with_namespace(self, value):
        self._name_with_namespace = value

    @property
    def created_at(self):
        return int(self._created_at.timestamp())

    @created_at.setter
    def created_at(self, value):
        self._created_at = parser.parse(value)
    # </editor-fold>
