# -*- coding: utf-8 -*-
from django import forms

from heimdall.models.rulestype import RulesType, Rule

str_max_len = 50


class RuleForm(forms.ModelForm):
    name = forms.CharField(max_length=str_max_len)
    description = forms.CharField(max_length=1024, widget=forms.Textarea, required=False)
    audit_command = forms.CharField(max_length=str_max_len)
    type = forms.ModelChoiceField(queryset=RulesType.objects.all())
    rationale = forms.CharField(max_length=1024, widget=forms.Textarea, required=False)

    class Meta:
        model = Rule
        fields = ('name', 'description', 'audit_command', 'type', 'rationale')
