# -*- coding: utf-8 -*-
from datetime import datetime

from reports import __reportdir__


class Audit(object):
    """ Class who define an audit.

        :param: host: audit's host.
        :param: profile: audit's profile.
        :param: report: result data after auditing.
        :param: audit_name: temporary generate audit script name.
        :param: pickle_name: pickle name created by audit script.
        :param: config_name: list of script needed for audit.
        :param: scripts_needed: temporary generate configuration script name.
        :param: audit_script_path: path to audit script.
        :param: config_script_path: path to configuration script.
        :param: report_path: path to audit report.
        :type: host: Plateform host
        :type: profile: Profile Object
        :type: report: dict
        :type: audit_name: str
        :type: pickle_name: str
        :type: config_name: list of script needed for audit.
        :type: scripts_needed: list of str
        :type: audit_script_path: str
        :type: config_script_path: str
        :type: report_path: str
        :return: Audit Object
        :rtype: object
    """

    def __init__(self, host=None, profile=None, plateform=None, environment=None):
        self.host = host
        self.profile = profile
        self.plateform = plateform
        self.environment = environment
        self.report = ''
        self.audit_name, self.pickle_name, self.config_name = self.generate_name()
        self.scripts_needed = self.get_script_needed
        self.audit_script_path = ''
        self.config_script_path = ''
        self.report_path = __reportdir__ + '/%s.%s' % (
            host.name + '_' + datetime.now().strftime("%Y-%m-%d_%H-%M-%S"), 'html')

    def __str__(self):
        return super(Audit, self).__str__()

    def __repr__(self):
        return super(Audit, self).__repr__()

    def __setattr__(self, name, value):
        return object.__setattr__(self, name, value)

    def __getattribute__(self, name):
        return object.__getattribute__(self, name)

    def __iter__(self):
        for k, v in self.__dict__.iteritems():
            if k == 'host':
                v = dict(self.hosts)
            if k == 'profile':
                v = []
                for pr in self.profile:
                    v.append(dict(pr))
            yield (k, v)

    @property
    def get_script_needed(self):
        list_scripts = []
        from conf.scripts import __auditdir__
        for t in self.profile.types:
            for r in t.rules:
                [list_scripts.append(__auditdir__ + '/' + au) for au in r.audit if '.sh' == au[-3:]]
                # [list_scripts.append(__remeddir__ + '/' + re) for re in r.remed if '.sh' == re[-3:]]
        return list_scripts

    @staticmethod
    def generate_name():
        """ Generate 3 random name for temporary files

        :return: names of temporary files
        :rtype: str
        """
        from hashlib import md5
        import random
        noncename = md5(str(random.random())).hexdigest()
        audit_name = noncename[:10]
        pickle_name = noncename[10:20]
        config_name = noncename[20:30]
        return audit_name, pickle_name, config_name

    def generate_scripts(self):
        """ Generate script from Jinja template.

        :return: Updated Audit Object
        :rtype: Audit Object
        """
        from core.jinja import JinjaTemplate
        from templates import __audittemplate__, __configtemplate__

        audit_template = JinjaTemplate(audit=self, template=__audittemplate__)
        self.audit_script_path = audit_template.create_audit_template()

        audit_template.template = __configtemplate__
        self.config_script_path = audit_template.create_config_template()

        return self

    def generate_report(self):
        """ Generate report from result data. Generated file is a html file based on a JinjaTemplate.

        :return: Updated Audit Object
        :rtype: Audit Object
        """
        from core.exceptions import AuditError
        try:
            if not self.report:
                raise AuditError("Can't generate report from empty data")
        except AuditError as ae:
            print ae
            exit(255)

        from core.jinja import JinjaTemplate
        from templates import __reporttemplate__

        report_template = JinjaTemplate(audit=self, template=__reporttemplate__)
        self.report_path = report_template.create_report_template()

        return self
