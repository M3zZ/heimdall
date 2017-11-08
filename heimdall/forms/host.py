# -*- coding: utf-8 -*-
from django import forms

from heimdall.models.hostsgroup import HostsGroup, Host

str_max_len = 50


class HostForm(forms.ModelForm):
    name = forms.CharField(max_length=str_max_len)
    hostsgroup = forms.ModelMultipleChoiceField(queryset=HostsGroup.objects.all())
    description = forms.CharField(max_length=255, widget=forms.Textarea, required=False)
    operating_system = forms.ChoiceField((('CentOS7', 'CentOS7'), ('CentOS6', 'CentOS6'), ('Debian', 'Debian')))
    ip_address = forms.GenericIPAddressField()
    account = forms.CharField(max_length=str_max_len)
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = Host
        fields = ('name', 'hostsgroup', 'description', 'operating_system', 'ip_address', 'account', 'password')
