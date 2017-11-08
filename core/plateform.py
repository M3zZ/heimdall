# -*- coding: utf-8 -*-


class Plateform(object):
    """ Class who define a plateform.
         yml files are read from heimdall/conf/hosts/plateform.yml and used for Plateform Object instantiation

        Keyword Args:
            :param: name: plateform's name.
            :param: desc: plateform's description.
            :param: id: plateform's id.
            :param: path: plateform's path to yaml file.
            :param: environment: plateform's environments.
            :type: name: str
            :type: desc: str
            :type: id: int
            :type: path: str
            :type: environment: list of Host Object
            :return: Plateform object
            :rtype: object
    """

    def __init__(self, **kwargs):
        self.name = kwargs.get('name', '')
        self.desc = kwargs.get('desc', '')
        self.id = kwargs.get('id', 1)
        self.path = kwargs.get('path', '')
        self.environment = kwargs.get('environment', '')

    def __str__(self):
        return super(Plateform, self).__str__()

    def __repr__(self):
        return super(Plateform, self).__repr__()

    def __setattr__(self, name, value):
        return object.__setattr__(self, name, value)

    def __getattribute__(self, name):
        return object.__getattribute__(self, name)

    def __iter__(self):
        for k, v in self.__dict__.iteritems():
            if k == 'environment':
                v = {}
                for env, hosts in self.environment.iteritems():
                    v[env] = []
                    [v[env].append(dict(h)) for h in hosts]
            yield (k, v)

    def get_new_id(self, environment):
        """ Return a new id available for a rule.

            :return: Length of list of all Host Objects in hosts attribute.
            :rtype: int
        """
        return len(self.environment[environment]) + 1

    def check_host_exist(self, hostname, environment):
        """ Check if name exist in list of all Host Objects.

            :param hostname: Host's name that must be checked
            :param environment: Host's environment
            :type: hostname: str
            :type: environment: str
            :return: If name exist return name, return False otherwise.
            :rtype: bool or str
        """

        exist = False
        try:
            self.environment[environment]  # Environment doesnt exist
        except KeyError:
            return exist

        for hosts in self.environment[environment]:
            if hosts.name == hostname:
                exist = True
        return exist

    def check_environment(self, environment):
        if environment not in self.environment.keys():
            return False
        else:
            return True

    def remove_host(self, host):
        """ Remove a Host Object from Plateform.

            :param: host: Host Object that must be removed.
            :type: host: Host Object
            :return: Updated Plateform Object
            :rtype: Plateform Object
        """
        if host == -1:
            self.environment[host.environment] = []
        else:
            [self.environment[h.environment].remove(h) for h in host] if isinstance(host, list) else self.environment[
                host.environment].remove(host)
        return self

    def add_host(self, host):
        """ Add a Host Object to Plateform.

            :param: host: Host Object that must be added.
            :type: host: Host Object
            :return: Updated Plateform Object
            :rtype: Plateform Object
        """
        self.environment[host.environment].append(host)
        return self
