# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

str_max_len = 50


class RulesType(models.Model):
    id = models.AutoField(primary_key=True, verbose_name='type_id')
    name = models.CharField(max_length=str_max_len)
    description = models.TextField(max_length=255)

    def __str__(self):
        return self.name

    def get_rules(self):
        from heimdall.models.profiles import Rule
        return list(Rule.objects.filter(type=self))

    def get_fields(self):
        linked_rules = self.get_rules()
        fields = {}
        for field in RulesType._meta.fields:
            fields[field.name] = str(field.value_to_string(self))
        fields['rules'] = [lr.name for lr in linked_rules]
        return fields


class Rule(models.Model):
    id = models.AutoField(primary_key=True, verbose_name='rule_id')
    name = models.CharField(max_length=str_max_len)
    audit_command = models.TextField(max_length=str_max_len)
    type = models.ForeignKey(RulesType, on_delete=models.CASCADE)
    description = models.TextField(max_length=255)
    rationale = models.TextField(max_length=255)

    def __str__(self):
        return self.name

    def get_type(self):
        from heimdall.models.rulestype import RulesType
        return list(RulesType.objects.filter(id=self.type).name)

    def get_fields(self):
        fields = {}
        print(Rule._meta.fields)
        for field in Rule._meta.fields:
            if field == 'type':
                fields[field.name] = self.get_type()
            else:
                fields[field.name] = str(field.value_to_string(self))
        return fields
