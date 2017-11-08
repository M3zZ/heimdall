# -*- coding: utf-8 -*-


def get_all_types():
    """ Return all Type Objects read from yaml file in heimdall/conf/rules/type.yml

        :return: return all Type Objects
        :rtype: list of Type Object

        .. seealso:: heimdall.conf.rules.getAllTypesObjects()
    """
    from conf.rules import getAllTypesObjects
    return getAllTypesObjects()


def get_type(name=None):
    """ Take type information passed by user, and return list of type filtered

        :param: name: type's type (same as type yaml file) passed by user
        :type: name: list of str
        :return: list of Type Objects filtered
        :rtype: list of Type Objects

        ..seealso:: heimdall.conf.rules.getTypeObject()
    """
    from conf.rules import getTypeObject

    types = []
    [types.append(getTypeObject(n)) for n in name]

    return types


def add_type(name=None, desc=None):
    """ Create a Type Object from information passed by user, and return it.

        :param: name: type's name (same as type yaml file) passed by user.
        :param: desc: type's description.
        :type: name: list of str
        :type: desc: list of str
        :return: new Type Object
        :rtype: Type Object

        ..seealso: heimdall.core.type.Type, update_type()
    """
    from core.type import Type
    from conf.rules import __tdir__
    from utils.wiki import create_wikidir
    newtype = {'id': get_new_id(), 'name': name[0], 'desc': desc[0], 'path': __tdir__ + '/' + name[0] + '.yml',
               'rules': [], 'all': False}

    t = Type(**newtype)
    update_type(t)
    create_wikidir(t)
    return t


def update_type(type=None):
    """ Take a Type Object and write his data in type.yml file.

        :param: type: a Type object
        :type: type: Type Object
        :return: True if succeed, raise an error otherwise.
        :rtype: bool

        .. seealso:: heimdall.core.yml.write_yml(), heimdall.core.type.Type
    """
    from core.type import Type
    from core.yml import write_yml
    from core.exceptions import TypeInstanceError

    try:
        if isinstance(type, Type):
            for r in type.rules:
                # type isn't needed in yml file
                del r.type
            write_yml(path=type.path, data=type)
            print "[*] - Type %s successfully updated" % type.name
            return True
        else:
            raise TypeInstanceError('Argument for %s must be an Type Instance' % update_type.__name__)
    except TypeInstanceError as tie:
        print tie
        exit(tie.code)


def update_self_type(name=None, desc=None, newname=None):
    """ Update a Type object from information passed by user, and return the new Type Object created.
            New Object is write in corresponding yaml file.

            :param: name: type's name (same as plateform yaml file) passed by user
            :param: desc: type's description passed by user
            :param: newname: type's new name (plateform yaml file will be rename) passed by user
            :type: name: list of one str element
            :type: desc: list of one str element
            :type: newname: list of one str element
            :return: updated new Type Object
            :rtype: Type Object

            .. seealso:: heimdall.conf.rules.getTypeObject(), heimdall.core.yml.rename_yml(), update_type()
        """
    from core.type import Type
    from core.yml import rename_yml
    from conf.rules import getTypeObject
    from core.exceptions import TypeInstanceError
    from utils.wiki import rename_wikidir

    t = getTypeObject(name[0])
    ot = t

    if desc:
        t.desc = desc[0]
    if newname:
        t.name = newname[0]
        t.path = t.path.replace(name[0], newname[0])
        try:
            if isinstance(t, Type):
                rename_yml(oldpath=ot.path, newpath=t.path)
                rename_wikidir(oldtype=ot, newtype=t)
            else:
                raise TypeInstanceError('Argument for %s must be an Type Instance' % update_self_type.__name__)
        except TypeInstanceError as tie:
            print tie
            exit(tie.code)
        for r in t.rules:
            r.type = t.name
    update_type(t)
    return t


def remove_type(name=None):
    """ Remove type file from type name passed by user.

        :param: name: type's name (same as type yaml file) passed by user
        :type: name: list of one str element
        :return: True if remove succeed
        :rtype: bool

        .. seealso:: heimdall.conf.rule.getTypeObject(), heimdall.core.yml.remove_yml()
    """
    from core.yml import remove_yml
    from core.type import Type
    from conf.rules import getTypeObject
    from core.exceptions import TypeInstanceError
    from utils.wiki import remove_wikidir
    t = getTypeObject(name[0])
    try:
        if isinstance(t, Type):
            remove_yml(t.path)
            remove_wikidir(t)
            print "Type %s successfully removed!" % name
            return True
        else:
            raise TypeInstanceError('Argument for %s must be an Type Instance' % update_self_type.__name__)
    except TypeInstanceError as tie:
        print tie
        exit(tie.code)


def get_new_id():
    """ Return a new id available from all type.
        If heimdall/conf/rules/ is empty, return 1

        :return: new id if one type exist, 1 otherwise
        :rtype: int

        .. seealso:: heimdall.conf.rules.getAllTypesObjects()
    """
    from conf.rules import getAllTypesObjects

    alltype = getAllTypesObjects()

    if not alltype:
        return 1

    newid = []
    [newid.append(t.id) for t in alltype]
    return max(newid) + 1


def check_type(type=None):
    """ Check if type exist by type name.

        :param: type: type's name passed by user.
        :type: type: list of str
        :return: True if type exist, False otherwise.
        :rtype: bool

        .. seealso:: heimdall.conf.rules.getAllTypesObjects()
    """
    from conf.rules import getAllTypesObjects
    from core.exceptions import TypeDoesNotExist

    if not type:
        return False

    type_available = []
    [type_available.append(t.name) for t in getAllTypesObjects()]
    exist = set(type_available).intersection(set(type))

    try:
        if not exist:
            raise TypeDoesNotExist('Type %s does not exists!' % type)
        else:
            return True
    except TypeDoesNotExist as tne:
        print tne
        exit(tne.code)


def check_type_exist(type=None):
    """ Check if type already exist by type name.

        :param: type: type's name passed by user.
        :type: type: list of str
        :return: False if type doesnt exist, raise an error otherwise.
        :rtype: bool

        .. seealso:: heimdall.conf.rules.getAllTypesObjects()
    """
    from conf.rules import getAllTypesObjects
    from core.exceptions import TypeAlreadyExist

    if not type:
        return False

    type_available = []
    [type_available.append(t.name) for t in getAllTypesObjects()]
    exist = set(type_available).intersection(set(type))

    try:
        if exist:
            raise TypeAlreadyExist('Type %s already exist!' % type)
        else:
            return False
    except TypeAlreadyExist as tae:
        print tae
        exit(tae.code)
