# -*- coding: utf-8 -*-
from django import forms

from heimdall.models.hostsgroup import Host
from heimdall.models.profiles import Profile
from heimdall.models.rulestype import Rule

str_max_len = 50


class ProfileForm(forms.ModelForm):
    name = forms.CharField(max_length=str_max_len)
    description = forms.CharField(max_length=255, widget=forms.Textarea, required=False)
    rules = forms.ModelMultipleChoiceField(queryset=Rule.objects.all(), required=True)
    hosts = forms.ModelMultipleChoiceField(queryset=Host.objects.all(), required=True)

    class Meta:
        model = Profile
        fields = ('name', 'description', 'rules', 'hosts')
