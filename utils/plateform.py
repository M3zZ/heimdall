# -*- coding: utf-8 -*-


def get_all_plateforms():
    """ Return all plateforms objects read from yaml file in heimdall/conf/hosts/plateform.yml

        :return: return all plateforms objects
        :rtype: list of plateform object

        .. seealso:: heimdall.conf.hosts.getAllPlateformObjects()
    """
    from conf.hosts import getAllPlateformObjects
    return getAllPlateformObjects()


def get_plateform(plateform=None, environment=None, id=None):
    """ Take plateform information passed by user, and return list of plateforms filtered

        :param: plateform: plateform's name (same as plateform yaml file) passed by user
        :param: environment: plateform's environment passed by user
        :param: id: plateform's id passed by user
        :type: plateform: list of str
        :type: environment: list of str
        :type: id: list of int
        :return: list of plateform objects filtered
        :rtype: list of plateform objects

        .. seealso::: heimdall.conf.hosts.getPlateformObject(), heimdall.conf.hosts.getAllPlateformObjects()
    """

    plateforms_availables = []
    all_plateform = []

    from conf.hosts import getAllPlateformObjects, getPlateformObject
    if plateform:
        [all_plateform.append(getPlateformObject(p)) for p in plateform]
    else:
        all_plateform = getAllPlateformObjects()

    for p in all_plateform:
        if environment:  # if environment is set
            for env in environment:
                if id:  # if id is set, filter with environment AND id
                    [[plateforms_availables.append(p) for i in id if i == p.id] for e in p.environment if e == env]
                else:  # only filter with environment
                    [plateforms_availables.append(p) for e in p.environment if e == env]
        elif id:  # if environment is not set, but id is set filter only with id
            [plateforms_availables.append(p) for i in id if i == p.id]
        else:  # environment and id are not set, just return all plateforms
            plateforms_availables = all_plateform
    return plateforms_availables


def add_plateform(plateform=None, desc=None, environment=None):
    """ Create a Plateform object from information passed by user, and return the new plateform object created.

        :param: plateform: plateform's name (same as plateform yaml file) passed by user
        :param: desc: plateform's description passed by user
        :param: environment: plateform's environment passed by user
        :type: plateform: list of one str element
        :type: desc: list of one str element
        :type: environment: list of one str element
        :return: updated new plateform object
        :rtype: plateform object

        .. seealso:: update_plateform(),
    """
    from core.plateform import Plateform
    from conf.hosts import __pdir__

    env = {}
    for e in environment:
        env[e] = []
    newplateform = {'id': get_new_id(), 'name': plateform[0], 'desc': desc[0], 'environment': env,
                    'path': __pdir__ + '/' + plateform[0] + '.yml'}

    p = Plateform(**newplateform)
    update_plateform(p)
    return p


def update_plateform(plateform=None):
    """ Take a Plateform object and write his data in plateform.yml file.

        :param: plateform: a plateform object
        :type: plateform: Plateform Object
        :return: True if succeed, raise an error otherwise.
        :rtype: bool

        .. seealso:: heimdall.core.yml.write_yml(), heimdall.core.plateform.Plateform

    """
    from core.exceptions import PlateformTypeError
    from core.plateform import Plateform
    from core.yml import write_yml

    try:
        if isinstance(plateform, Plateform):
            for env, hosts in plateform.environment.iteritems():
                # environment and plateform name isn't needed in yml file
                for h in hosts:
                    try:
                        del h.environment
                        del h.plateform
                    except AttributeError:  # If environment or plateform doesnt exist skip
                        pass

            write_yml(path=plateform.path, data=plateform)
            print "[*] - Plateform %s successfully updated" % plateform.name
            return True
        else:
            raise PlateformTypeError("Argument passed to %s must be a Platform object." % update_plateform.__name__)
    except PlateformTypeError as pte:
        print pte
        exit(pte.code)


def update_self_plateform(name=None, desc=None, newname=None):
    """ Update a Plateform Object from information passed by user, and return the new Plateform Object created.
        New object is write in corresponding yaml file.

        :param: name: plateform's name (same as plateform yaml file) passed by user
        :param: desc: plateform's description passed by user
        :param: newname: plateform's new name (plateform yaml file will be rename) passed by user
        :type: name: list of one str element
        :type: desc: list of one str element
        :type: newname: list of one str element
        :return: updated new plateform object
        :rtype: plateform object

        .. seealso:: heimdall.conf.hosts.getPlateformObject(), heimdall.core.yml.rename_yml(), update_plateform()
    """
    from core.exceptions import PlateformTypeError
    from core.plateform import Plateform
    from core.yml import rename_yml
    from conf.hosts import getPlateformObject

    p = getPlateformObject(name[0])
    oldpath = p.path

    if desc:
        p.desc = desc[0]
    if newname:
        p.name = newname[0]
        p.path = p.path.replace(name[0], newname[0])

    try:
        if isinstance(p, Plateform):
            rename_yml(oldpath=oldpath, newpath=p.path)
        else:
            raise PlateformTypeError("Argument passed to %s must be a Platform object." % update_plateform.__name__)
    except PlateformTypeError as pte:
        print pte
        exit(pte.code)
    update_plateform(p)
    return p


def remove_plateform(name=None):
    """ Remove plateform file from plateform name passed by user.

        :param: name: plateform's name (same as plateform yaml file) passed by user
        :type: name: list of one str element
        :return: True if remove succeed
        :rtype: bool

        .. seealso:: heimdall.conf.hosts.getPlateformObject(), heimdall.core.yml.remove_yml()
    """
    from core.exceptions import PlateformTypeError
    from core.yml import remove_yml
    from core.plateform import Plateform
    from conf.hosts import getPlateformObject

    p = getPlateformObject(name[0])
    try:
        if isinstance(p, Plateform):
            remove_yml(p.path)
            print "[*] - %s successfully removed!" % name
            return True
        else:
            raise PlateformTypeError("Argument passed to %s must be a Platform object." % update_plateform.__name__)
    except PlateformTypeError as pte:
        print pte
        exit(pte.code)


def get_new_id():
    """ Return a new id available from all plateform.
        If heimdall/conf/host/ is empty, return 1

        :return: new id if one plateform exist, 1 otherwise
        :rtype: int

        .. seealso:: heimdall.conf.hosts.getAllPlateformObjects()
    """
    from conf.hosts import getAllPlateformObjects

    allplateform = getAllPlateformObjects()

    if not allplateform:
        return 1

    newid = []
    [newid.append(p.id) for p in allplateform]
    return max(newid) + 1


def get_new_host_id(plateform=None, environment=None):
    """ Return a new id available in plateform for one environment

        :return: new id if none host exist, 1 otherwise
        :rtype: int

        .. seealso:: heimdall.conf.hosts.getAllPlateformObjects()
    """

    from conf.hosts import getPlateformObject

    p = getPlateformObject(plateform)

    if not p:
        return 1

    for env, hosts in p.environment.iteritems():
        if environment == env:  # found our environment
            return len(hosts) + 1
    else:
        return 1


def check_plateform(plateform=None):
    """ Check if plateform exist by plateform name.

        :param: plateform: plateform's name passed by user.
        :type: plateform: list of str
        :return: True if plateform exist, False otherwise.
        :rtype: bool

        .. seealso:: heimdall.conf.hosts.getAllPlateformObjects()
    """
    from conf.hosts import getAllPlateformObjects
    from core.exceptions import PlateformDoesNotExist

    if not plateform:
        return False

    plateform_available = []
    for p in getAllPlateformObjects():
        if plateform[0] == p.name:
            plateform_available.append(p.name)
    exist = set(plateform_available).intersection(set(plateform))

    try:
        if not exist:
            raise PlateformDoesNotExist('Plateform %s does not exists!' % plateform, plateform)
        else:
            return True
    except PlateformDoesNotExist as pde:
        print pde
        exit(pde.code)


def check_plateform_exist(plateform=None):
    """ Check if plateform already exist.

        :param: plateform: plateform's name passed by user.
        :type: plateform: list of str
        :return: False if type doesnt exist, raise an error otherwise.
        :rtype: bool

        .. seealso:: heimdall.conf.hosts.getAllPlateformObjects()
    """
    from conf.hosts import getAllPlateformObjects
    from core.exceptions import PlateformAlreadyExist

    if not plateform:
        return False

    plateform_available = []
    [plateform_available.append(p.name) for p in getAllPlateformObjects()]
    exist = set(plateform_available).intersection(set(plateform))

    try:
        if exist:
            raise PlateformAlreadyExist("Plateform %s already exist !" % plateform, plateform)
        else:
            return False
    except PlateformAlreadyExist as pae:
        print pae
        exit(pae.code)
