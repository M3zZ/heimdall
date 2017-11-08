# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.http import HttpResponseRedirect
from django.shortcuts import render, reverse

from heimdall.forms.audit import AuditForm
from heimdall.forms.host import HostForm
from heimdall.forms.hostsgroup import HostsGroupForm
from heimdall.forms.profile import ProfileForm
from heimdall.forms.rule import RuleForm
from heimdall.forms.type import TypeForm
from heimdall.models.audits import Audit
from heimdall.models.hostsgroup import HostsGroup, Host
from heimdall.models.profiles import Profile
from heimdall.models.rulestype import RulesType, Rule

item_class = {
    'host': {
        'form': HostForm,
        'model': Host
    },
    'hostsgroup': {
        'form': HostsGroupForm,
        'model': HostsGroup
    },
    'profile': {
        'form': ProfileForm,
        'model': Profile
    },
    'rule': {
        'form': RuleForm,
        'model': Rule
    },
    'type': {
        'form': TypeForm,
        'model': RulesType
    },
    'audit': {
        'form': AuditForm,
        'model': Audit
    },

}


def overview(request, item='overview'):
    last_audited = ''
    if item == 'overview':  # overview page need critical hosts and last audited hosts
        data = item_class['host']['model'].objects.all()
        last_audited = data.order_by('-last_audit').exclude(last_audit__isnull=True)[:5]
    else:
        data = item_class[item]['model'].objects.all()
        if item == 'audit':
            last_audited = data.order_by('-date').exclude(date__isnull=True)[:5]
    context = {'item': item, 'action': 'overview', 'data': data, "last_audited": last_audited}
    return render(request, 'main.html', context)


def list(request, item):
    data = item_class[item]['model'].objects.all()
    context = {'item': item, 'action': 'list', 'data': data}
    return render(request, 'main.html', context)


def add(request, item):
    context = {'item': item, 'action': 'add', 'form': item_class[item]['form']}
    return render(request, 'main.html', context)


def update(request, item, id):
    if id:
        filtered_item = item_class[item]['model'].objects.get(id=id)
        form = item_class[item]['form'](initial=filtered_item.get_fields())
        context = {'item': item, 'action': 'update', 'form': form}
    else:
        data = item_class[item]['model'].objects.all()
        context = {'item': item, 'action': 'update', 'form': '', 'data': data}
    return render(request, 'main.html', context)


def remove(request, item, id):
    data = item_class[item]['model'].objects.all()
    for i in id.split(','):
        data.filter(id=int(i)).delete()
    context = {'item': item, 'action': 'list', 'data': item_class[item]['model'].objects.all()}
    return render(request, 'main.html', context)


def save(request, item):
    if request.method == 'POST':
        form = item_class[item]['form'](request.POST)
        if form.is_valid():
            print 'Saving Model !'
            f = form.save(commit=False)
            f.save()
            form.save_m2m()
            return HttpResponseRedirect(reverse(overview))
        else:
            print 'not valid model'
            context = {'item': item, 'action': 'overview'}
            return render(request, 'main.html', context)


def detail(request, item, id):
    # filtered_item = item_class[item]['model'].objects.filter(id=id)[0]
    filtered_item = item_class[item]['model'].objects.get(id=id)
    context = {'item': item, 'action': 'detail', 'data': filtered_item}
    return render(request, 'main.html', context)
