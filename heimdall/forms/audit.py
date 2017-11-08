# -*- coding: utf-8 -*-
from django import forms

from heimdall.models.audits import Audit
from heimdall.models.hostsgroup import Host
from heimdall.models.profiles import Profile

str_max_len = 50


class AuditForm(forms.ModelForm):
    host = forms.ModelChoiceField(queryset=Host.objects.all())
    profile = forms.ModelChoiceField(queryset=Profile.objects.all())

    class Meta:
        model = Audit
        fields = ('host', 'profile')
