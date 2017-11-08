# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

from heimdall.models.audits import Audit
from heimdall.models.profiles import Rule

str_max_len = 50


class Result(models.Model):
    id = models.AutoField(primary_key=True, verbose_name='results_id')
    audit = models.ForeignKey(Audit, on_delete=models.CASCADE)
    rule = models.ForeignKey(Rule, on_delete=models.CASCADE)
    output = models.TextField(max_length=255, blank=True, null=True)
    exit_code = models.IntegerField(default=0, blank=True, null=True)

    def __str__(self):
        return self.id

    def get_fields(self):
        fields = [(field.name, [str(field.value_to_string(self))]) for field in Result._meta.fields]
        return fields
