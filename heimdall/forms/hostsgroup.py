# -*- coding: utf-8 -*-
from django import forms

from heimdall.models.hostsgroup import HostsGroup, Host

str_max_len = 50


class HostsGroupForm(forms.ModelForm):
    name = forms.CharField(max_length=str_max_len)
    description = forms.CharField(max_length=255, widget=forms.Textarea, required=False)
    host = forms.ModelMultipleChoiceField(queryset=Host.objects.all(), required=False)

    class Meta:
        model = HostsGroup
        fields = ('name', 'description', 'host')
