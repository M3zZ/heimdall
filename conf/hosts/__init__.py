# -*- coding: utf-8 -*-
from os import path, listdir

__pdir__ = path.dirname(__file__)
__plateformsfiles__ = [path.join(__pdir__, hf) for hf in listdir(__pdir__) if
                       (path.isfile(path.join(__pdir__, hf)) and 'yml' in path.basename(path.join(__pdir__, hf)))]


def getAllPlateformObjects():
    """ Open and read data from heimdall/conf/host/plateform.yaml, then create Plateform Objects from data.
        Host Objects are also created and added to Plateform Objects.

        :return: list of all Plateform Objects available.
        :rtype: list of Plateform Objects

        ..seealso:: heimdall.core.plateform.Plateform, heimdall.core.host.Host
    """
    from core.plateform import Plateform
    from core.host import Host
    from core.yml import open_yml

    plateform_availables = []
    for plateform in __plateformsfiles__:
        filepath = path.join(__pdir__, plateform)
        plateform_data = open_yml(path=filepath)
        if plateform_data:
            plateform_data['path'] = filepath
            for env, hosts in plateform_data['environment'].iteritems():
                environment = []
                for h in hosts:
                    h['environment'] = env
                    environment.append(Host(**h))
                plateform_data['environment'][env] = environment
            plateform = Plateform(**plateform_data)
            plateform_availables.append(plateform)
    return plateform_availables


def getPlateformObject(name=None):
    from core.plateform import Plateform
    from core.host import Host
    from core.yml import open_yml

    filepath = path.join(__pdir__, name + '.yml')
    plateform_data = open_yml(path=filepath)
    plateform = []
    if plateform_data:
        plateform_data['path'] = filepath
        plateform = Plateform(**plateform_data)
        for env, hosts in plateform.environment.iteritems():
            environment = []
            for h in hosts:
                h['environment'] = env
                environment.append(Host(**h))
            plateform.environment[env] = environment
    return plateform


def getAllHostsObjects():
    """ Open and read data from heimdall/conf/hosts/plateform.yaml, then create Host Objects from data.

        :return: list of all Host Objects available.
        :rtype: list of Host Objects

        ..seealso:: heimdall.core.host.Host
    """
    from core.host import Host
    from core.yml import open_yml

    hosts_availables = []
    for plateform in __plateformsfiles__:
        filepath = path.join(__pdir__, plateform)
        hosts_data = open_yml(path=filepath)
        if hosts_data:
            for env, hosts in hosts_data['environment'].iteritems():
                for h in hosts:
                    h['environment'] = env
                    h['plateform'] = hosts_data['name']
                    hosts_availables.append(Host(**h))
    return hosts_availables


def getHostObject(plateform=None, name=None):
    """ Open and read data from plateform name passed by user, then create Host Object from data filtered by name.

        :return: Host Object created from data read in heimdall/conf/host/plateform.yml.
        :rtype: Host Object

        ..seealso:: heimdall.core.host.Host
    """
    from core.host import Host
    from core.yml import open_yml
    from core.exceptions import HostDoesNotExist

    filepath = path.join(__pdir__, plateform + '.yml')
    plateform_data = open_yml(path=filepath)
    try:
        if plateform_data:
            for e in plateform_data['environment']:
                for h in plateform_data['environment'][e]:
                    if name == h.get('name'):
                        h['plateform'] = plateform_data['name']
                        h['environment'] = e
                        return Host(**h)
                else:
                    raise HostDoesNotExist("Host %s in plateform %s doesnt exists" % (name, plateform))
    except HostDoesNotExist as hde:
        print hde
        exit(hde.code)
