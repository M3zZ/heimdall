# -*- coding: utf-8 -*-

from jinja2 import Environment, FileSystemLoader

from templates import __tdir__
from tmp import __tmpdir__
from wikibase import __wikipath__


class JinjaTemplate:
    """ Class used for rendering template with jinja library.

     :param: audit: Audit Object who contains all informations of current audit.
     :param: template: jinja template's name.
     :type: audit: Audit Object
     :type: template: str
     :type: desc: str
     :type: path: list of str
     :type: types: list of Type Object
     :return: Profile object
     :rtype: object

    """

    def __init__(self, audit=None, template=None):
        self.audit = audit
        self.template = template
        self.template_dir = []
        self.template_dir.append(__tdir__)  # directory where template is found
        self.template_dir.append(__wikipath__)
        from os.path import join
        [self.template_dir.append(join(__wikipath__, t.name)) for t in self.audit.profile.types]
        from conf.scripts import __auditdir__, __remeddir__
        self.template_dir.append(__auditdir__)
        self.template_dir.append(__remeddir__)
        self.env = Environment(autoescape=False, loader=FileSystemLoader(self.template_dir), trim_blocks=False)
        # self.env.add_extension('jinja2.ext.with_')

    def render_template(self, context):
        """ Render ing template with context.

        :param context: dict who contains python objects to render.
        :return: path to generated script.
        """
        return self.env.get_template(self.template).render(context)

    def create_audit_template(self):
        """ Create audit script from jinja template.

        :return: path to generated script
        """

        path = __tmpdir__ + '%s.%s' % (self.audit.audit_name, 'py')
        context = {
            'rpickle': self.audit.pickle_name,
            'types': self.audit.profile.types
        }
        with open(path, 'w') as f:
            script = self.render_template(context)
            f.write(script)
            f.close()
        return path

    def create_config_template(self):
        """ Create configuration script from jinja template.

        :return: path to generated script
        """
        with open('/opt/heimdall/.ssh/id_rsa.pub', 'r') as fd:
            ssh_pub = fd.read()
        fd.close()
        path = __tmpdir__ + '%s.%s' % (self.audit.config_name, 'sh')
        context = {
            'scripts': self.audit.scripts_needed,
            'ssh_key': ssh_pub
        }
        with open(path, 'w') as f:
            script = self.render_template(context)
            f.write(script)
            f.close()
        return path

    def create_report_template(self):
        """ Create report from jinja template.

        :return: path to generated script
        """
        from datetime import datetime
        context = {
            'host': self.audit.host,
            'plateform': self.audit.plateform,
            'environment': self.audit.environment,
            'profile': self.audit.profile,
            'rule_output': self.audit.report.rule_output,
            'stats': self.audit.report.stats,
            'pourcent': self.audit.report.pourcent,
            'total': self.audit.report.total,
            'day': datetime.now().strftime("%Y-%m-%d"),
            'hour': datetime.now().strftime("%H:%M:%S"),
        }
        from codecs import open
        with open(self.audit.report_path, 'w', 'utf-8') as f:
            script = self.render_template(context)
            f.write(script)
            f.close()
        return self.audit.report_path
