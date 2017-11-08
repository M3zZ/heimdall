# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

from heimdall.models.hostsgroup import Host
from heimdall.models.rulestype import Rule

str_max_len = 50


class Profile(models.Model):
    id = models.AutoField(primary_key=True, verbose_name='profile_id')
    name = models.CharField(max_length=str_max_len)
    description = models.TextField(max_length=255)
    rules = models.ManyToManyField(Rule)
    hosts = models.ManyToManyField(Host)

    def __str__(self):
        return self.name

    def get_rules(self):
        return self.rules.all()

    def get_hosts(self):
        return self.hosts.all()

    def get_fields(self):
        fields = {}
        for f in Profile._meta.fields:
            print f
            if f == 'rules':
                fields[f.name] = self.get_rules()
            elif f == 'hosts':
                fields[f.name] = self.get_hosts()
            else:
                fields[f.name] = str(f.value_to_string(self))
        print fields
        return fields
