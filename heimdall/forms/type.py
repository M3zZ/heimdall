# -*- coding: utf-8 -*-
from django import forms

from heimdall.models.profiles import Rule
from heimdall.models.rulestype import RulesType

str_max_len = 50


class TypeForm(forms.ModelForm):
    name = forms.CharField(max_length=str_max_len)
    description = forms.CharField(max_length=255, widget=forms.Textarea, required=False)
    rule = forms.ModelMultipleChoiceField(queryset=Rule.objects.all(), required=False)

    class Meta:
        model = RulesType
        fields = ('name', 'description', 'rule')
