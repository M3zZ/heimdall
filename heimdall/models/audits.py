# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

from heimdall.models.hostsgroup import Host
from heimdall.models.profiles import Profile

str_max_len = 50


class Audit(models.Model):
    id = models.AutoField(primary_key=True, verbose_name='audit_id')
    date = models.DateTimeField('audit_date', blank=True, null=True, default=None)
    host = models.ForeignKey(Host)
    profile = models.ForeignKey(Profile)
    audit_status = models.IntegerField(default=255, blank=False)

    def __str__(self):
        return str("Audit # %d " % self.id)

    def get_host(self, name=None):
        from heimdall.models.hostsgroup import Host
        return list(Host.objects.filter(id=self.host.id))

    def get_profile(self, name=None):
        from heimdall.models.profiles import Profile
        return list(Profile.objects.filter(id=self.profile.id))

    def get_fields(self):
        fields = {}
        for field in Audit._meta.fields:
            fields[field.name] = str(field.value_to_string(self))
        fields['host'] = self.get_host()
        fields['profile'] = self.get_profile()
        return fields
