# -*- coding: utf-8 -*-
from __future__ import unicode_literals


# Create your views here.
# def mainpage(request):
#     latest_audited_hosts_list = Host.objects.order_by('-host_last_audit')[:5]
#     critical_host = {}
#     for host in Host.objects.order_by('-host_id'):
#         if host.host_status == 'Critical':
#             critical_host[host.id] = host.host_name
#     context = {
#         'latest_audited_hosts_list': latest_audited_hosts_list,
#         'critical_host': critical_host,
#     }
#     return render(request, 'main.html', context)
#
# def hosts(request, action='overview'):
#     print action
#     if action=='add':
#         return render(request, 'host.html', { 'action': 'add' })
#     elif action == 'overview':
#         return render(request, 'host.html', { 'action': '' })
#
# def test(request):
#     return render(request, 'object_detail.html')
#
# def hosts_overview(request):
#     return render(request, 'host.html')
#
# def rules_overview(request):
#     return render(request, 'rules.html')
#
# def profiles_overview(request):
#     return render(request, 'profiles.html')
#
# def audits_overview(request):
#     return render(request, 'audits.html')
