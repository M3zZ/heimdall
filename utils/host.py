# -*- coding: utf-8 -*-


def get_host(**kwargs):
    """ Return Host Objects read from yaml file in heimdall/conf/hosts/plateform.yml

        :return: return all Host Objects
        :rtype: list of Host Objects

        .. seealso:: heimdall.conf.hosts.getAllHostsObjects()
    """
    from conf.hosts import getAllHostsObjects

    if all(v is None for v in kwargs.values()):  # No value set return all host
        return getAllHostsObjects()

    hosts_availables = []
    for h in getAllHostsObjects():
        union_dict = {}
        # We take all arguments's value and we create a set for each
        for keys, values in kwargs.iteritems():
            set_list = []
            if values:  # Only if value exist (mean user choose a value)
                [set_list.append({v}) for v in values] if len(values) > 1 else set_list.append({values[0]})
            if set_list:
                union_dict[keys] = set.union(*set_list)  # Union for all set in set_list
        data_found = 0
        data_total = 0
        for k, v in union_dict.iteritems():
            for s in list(v):
                if type(s) is int or k == 'id':
                    if s == h.id:  # rules id special case
                        data_found += 1
                elif type(s) is float or k == 'kernel_version':
                    if str(s) in h.kernel_version:  # rules kernel special case
                        data_found += 1
                elif s in h.__getattribute__(k):
                    data_found += 1  # we found a correct value
            data_total += len(list(v))
        if data_found == data_total:  # All values have been found
            hosts_availables.append(h)
    return hosts_availables


def add_host(**kwargs):
    """ Create a Host Object from information passed by user, and return a Platform Object who contain the new Host Object.

        Keyword Args:
            plateform (list of one str): host's plateform (same as plateform yaml file)
            environment (list of one str): host's environment
            name (list of one str): host's name passed by user
            desc (list of one str): host's description passed by user
            ip (list of one str): host's ip passed by user
            account (list of one str): host's superuser account used for configuration passed by user
            distribution (list of one str): host's distribution passed by user
            kernel_version (list of one str): host's kernel_version passed by user

        :return: updated Plateform Object with the new Host Object
        :rtype: Plateform Object

        ..seealso: heimdall.core.host.Host, heimdall.core.plateform.Plateform, heimdall.conf.hosts.getPlateformObject()
    """
    from core.host import Host
    from conf.hosts import getPlateformObject
    from core.exceptions import EnvironmentDoesNotExist

    newhost = dict((k, ''.join(v)) for k, v in kwargs.iteritems() if v and len(v) == 1)
    host = Host(**newhost)
    p = getPlateformObject(host.plateform)

    try:
        if not p.check_environment(kwargs.get('environment')[0]):
            raise EnvironmentDoesNotExist(
                'Environment %s in plateform %s does not exists!' % (kwargs.get('environment')[0], p.name), p.name)
    except EnvironmentDoesNotExist as ede:
        print ede
        exit(ede.code)

    host.id = p.get_new_id(host.environment)
    p.add_host(host)

    return p


def remove_host(plateform=None, name=None, environment=None):
    """ Remove Host Object from Platform Object attribute hosts and return updated Platform Object.

        :param: plateform: host's plateform (same as type yaml file) passed by user
        :param: name: host's name passed by user
        :param: name: host's environment passed by user
        :type: plateform: list of one str
        :type: name: list of one str
        :type: environment: list of one str
        :return: Updated Plateform
        :rtype: Plateform Object

        .. seealso:: heimdall.conf.hosts.getPlateformObject(), heimdall.core.plateform.Plateform
    """
    from conf.hosts import getPlateformObject
    from core.exceptions import EnvironmentDoesNotExist

    p = getPlateformObject(plateform[0])
    try:
        if not p.check_environment(environment[0]):
            raise EnvironmentDoesNotExist('Environment %s in plateform %s does not exists!' % (environment[0], p.name),
                                          p.name)
    except EnvironmentDoesNotExist as ede:
        print ede
        exit(ede.code)

    if name[0] == -1:  # remove all
        p.environment[environment[0]] = []
    else:
        [p.remove_host(host) for host in p.environment[environment[0]] for n in name if host.name == n]

    return p


def move_host(oldplateform=None, environment=None, name=None, newplateform=None, newenvironment=None):
    """ Move host from one plateform to another.
        Retrieve old Platform Object and new Platform Object and update both with the Host Object filter by name.

        :param: oldplateform: old host's plateform (same as plateform yaml file).
        :param: name: host's name passed by user.
        :param: newplateform: new host's plateform (same as plateform yaml file).
        :type: oldplateform: list of one str
        :type: name: list of one str
        :type: newplateform: list of one str
        :return: Updated old Platform and new Platform
        :rtype: Old Platform Object, New Platform Object

        .. seealso:: heimdall.conf.hosts.getPlateformObject(), heimdall.core.plateform.Plateform
    """
    from conf.hosts import getPlateformObject
    from utils.plateform import get_new_host_id
    from core.exceptions import EnvironmentDoesNotExist
    old = getPlateformObject(oldplateform[0])
    new = getPlateformObject(newplateform[0])

    # Check if new environment exist
    try:
        if not new.check_environment(environment[0]):
            raise EnvironmentDoesNotExist(
                'Environment %s in plateform %s does not exists!' % (newenvironment[0], new.name), new.name)
    except EnvironmentDoesNotExist as ede:
        print ede
        exit(ede.code)

    for env, hosts in old.environment.iteritems():
        if environment[0] == env:  # found our environment
            for h in hosts:
                if h.name == name[0] or name[0] == -1:
                    old.remove_host(h)
                    h.plateform = new.name  # Setting new plateform name and environement
                    h.environment = newenvironment[0]
                    h.id = get_new_host_id(new.name, newenvironment[0])
                    new.add_host(h)

    return old, new


def update_host(**kwargs):
    """ Create a Host Object from information passed by user, and return a Platform Object who contain the new Host Object.

        Keyword Args:
            plateform (list of one str): host's plateform (same as plateform yaml file)
            name (list of one str): host's name passed by user
            desc (list of one str): host's description passed by user
            ip (list of one str): host's ip passed by user
            account (list of one str): host's superuser account used for configuration passed by user
            distribution (list of one str): host's distribution passed by user
            kernel_version (list of one str): host's kernel_version passed by user

        :return: updated Plateform Object with the new Host Object
        :rtype: Plateform Object

        ..seealso: heimdall.core.host.Host, heimdall.core.plateform.Plateform, heimdall.conf.hosts.getPlateformObject()
    """
    from conf.hosts import getPlateformObject
    from core.exceptions import EnvironmentDoesNotExist
    p = getPlateformObject(kwargs.get('plateform')[0])

    if not p.check_environment(kwargs.get('environment')[0]):
        raise EnvironmentDoesNotExist(
            'Environment %s in plateform %s does not exists!' % (kwargs.get('environment')[0], p.name),
            p.name)
    for host in p.environment[kwargs.get('environment')[0]]:
        if host.name == kwargs.get('name')[0]:
            if kwargs.get('newname'):
                host.name = kwargs.get('newname')[0]
            [host.__setattr__(k, v[0]) for k, v in kwargs.iteritems() if v and k != 'name' and k != 'newname']
    return p


def check_host(plateform=None, name=None, environment=None, check_exist=False):
    """ Check if host exist

        :param: plateform: host's plateform passed by user.
        :param: name: host's name passed by user.
        :param: environment: host's environment passed by user.
        :type: plateform: list of one str
        :type: name: list of one str
        :type: environment: list of one str
        :return: True if rule exist, raise exception otherwise.
        :rtype: bool

        .. seealso:: heimdall.conf.hosts.getPlateformObject()
    """
    from conf.hosts import getPlateformObject
    from core.exceptions import HostDoesNotExist, HostAlreadyExist

    if not plateform and not name:
        return False

    try:
        for plat in plateform:
            p = getPlateformObject(plat)
            if check_exist and p.check_host_exist(name[0], environment[0]):
                raise HostAlreadyExist("Host %s from %s already exist !" % (name[0], plat))
            if not check_exist and not p.check_host_exist(name[0], environment[0]):
                raise HostDoesNotExist("Host %s from %s in env %s doesnt exist !" % (name[0], plat, environment[0]))
        else:
            return True
    except HostDoesNotExist as hde:
        print hde
        exit(hde.code)
    except HostAlreadyExist as hae:
        print hae
        exit(hae.code)
