# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from heimdall.models.audits import Audit
from heimdall.models.hostsgroup import HostsGroup, Host
from heimdall.models.profiles import Profile
from heimdall.models.results import Result
from heimdall.models.rulestype import RulesType, Rule

# Register your models here.
admin.site.register(Host)
admin.site.register(HostsGroup)
admin.site.register(Profile)
admin.site.register(Rule)
admin.site.register(RulesType)
admin.site.register(Audit)
admin.site.register(Result)
