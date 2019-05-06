from django.db import models


class Group(models.Model):
    _name = models.CharField(max_length=250)
    _description = models.TextField(blank=True, default='')
    _visibility = models.CharField(max_length=250)
    _web_url = models.CharField(max_length=250)

    def __str__(self):
        return self._name

    def __unicode__(self):
        return '/%s/' % self._name

    # <editor-fold desc="Setter and Getter">
    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    @property
    def description(self):
        return self._description

    @description.setter
    def description(self, value):
        self._description = value

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
    # </editor-fold>
