# -*- coding: utf-8 -*-


class Host(object):
    """ Class who define an host

        Keyword Args:
            plateform (str): host's plateform (same as plateform yaml file)
            name (str): host's name
            environment (str): plateform's environment
            ip (str): host's ip
            id (int): host's id
            desc (str): host's description
            status (str): host's configuration status
            last_audit (str): host's last audit date
            account (str): host's superuser account used for configuration
            distribution (str): host's distribution
            kernel_version (str): host's kernel_version

        :return: Plateform Object
        :rtype: Plateform Object
    """

    def __init__(self, **kwargs):
        self.plateform = kwargs.get('plateform', '')
        self.name = kwargs.get('name', '')
        self.environment = kwargs.get('environment', '')
        self.ip = kwargs.get('ip', '')
        self.id = kwargs.get('id', '')
        self.desc = kwargs.get('desc', '')
        self.status = kwargs.get('status', 'unconfigured')
        self.last_audit = kwargs.get('last_audit', '')
        self.account = kwargs.get('account', 'root')
        self.distribution = kwargs.get('distribution', '')
        self.kernel_version = kwargs.get('kernel_version', '')

    def __str__(self):
        return super(Host, self).__str__()

    def __repr__(self):
        return super(Host, self).__repr__()

    def __setattr__(self, name, value):
        return super(Host, self).__setattr__(name, value)

    def __getattribute__(self, name):
        return super(Host, self).__getattribute__(name)

    def __iter__(self):
        for k, v in self.__dict__.iteritems():
            yield (k, v)
