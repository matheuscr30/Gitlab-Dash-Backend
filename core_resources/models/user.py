from core_resources.models import Project
from django.db import models
from dateutil import parser


class User(models.Model):
    _username = models.CharField(max_length=250, unique=True)
    _email = models.CharField(max_length=250, unique=True)
    _name = models.CharField(max_length=250)
    _user_state = models.CharField(max_length=250)
    _avatar_url = models.CharField(max_length=250)
    _web_url = models.CharField(max_length=250)
    _is_admin = models.BooleanField()
    _projects = models.ManyToManyField(Project)
    _created_at = models.DateTimeField()

    def __str__(self):
        return self._name

    def __unicode__(self):
        return '/%s/' % self._name

    # <editor-fold desc="Setter and Getter">
    @property
    def username(self):
        return self._username

    @username.setter
    def username(self, value):
        self._username = value

    @property
    def email(self):
        return self._email

    @email.setter
    def email(self, value):
        self._email = value

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    @property
    def user_state(self):
        return self._user_state

    @user_state.setter
    def user_state(self, value):
        self._user_state = value

    @property
    def avatar_url(self):
        return self._avatar_url

    @avatar_url.setter
    def avatar_url(self, value):
        self._avatar_url = value

    @property
    def web_url(self):
        return self._web_url

    @web_url.setter
    def web_url(self, value):
        self._web_url = value

    @property
    def is_admin(self):
        return self._is_admin

    @is_admin.setter
    def is_admin(self, value):
        self._is_admin = value

    @property
    def projects(self):
        return self._projects

    @projects.setter
    def projects(self, value):
        self._projects = value

    @property
    def created_at(self):
        return int(self._created_at.timestamp())

    @created_at.setter
    def created_at(self, value):
        self._created_at = parser.parse(value)
    # </editor-fold>
