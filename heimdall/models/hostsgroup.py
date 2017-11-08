# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import datetime

from django.db import models
from django.utils import timezone

str_max_len = 50


class HostsGroup(models.Model):
    id = models.AutoField(primary_key=True, verbose_name='group_id')
    name = models.CharField(max_length=str_max_len)
    description = models.TextField(max_length=255)

    def __str__(self):
        return self.name

    def get_hosts(self):
        return list(
            Host.object.filter(hostsgroup=self))

    def get_fields(self):
        linked_hosts = self.get_hosts()
        fields = {}
        for field in HostsGroup._meta.fields:
            fields[field.name] = str(field.value_to_string(self))
        fields['hosts'] = [lh.name for lh in linked_hosts]
        return fields


class Host(models.Model):
    id = models.AutoField(primary_key=True, verbose_name='host_id')
    name = models.CharField(max_length=str_max_len)
    hostsgroup = models.ManyToManyField(HostsGroup)
    description = models.TextField(max_length=255, blank=True, null=True)
    operating_system = models.CharField(max_length=str_max_len)
    ip_address = models.GenericIPAddressField(blank=False, null=False)
    last_audit = models.DateTimeField(blank=True, null=True)
    account = models.CharField(max_length=str_max_len, default="root")
    password = models.CharField(max_length=str_max_len, default="toor", blank=False, null=False)
    status = models.IntegerField(default=0, blank=False, null=False)

    def __str__(self):
        return self.name

    def was_audited_recently(self):
        return self.last_audit >= timezone.now() - datetime.timedelta(days=1)

    def get_fields(self):
        fields = {}
        for field in Host._meta.fields:
            fields[field.name] = str(field.value_to_string(self))
        return fields
