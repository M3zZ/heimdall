# -*- coding: utf-8 -*-


def get_all_rules():
    """ Return all Rule Objects read from yaml file in heimdall/conf/rules/type.yml

        :return: return all Rule Objects
        :rtype: list of Rule Objects

        .. seealso:: heimdall.conf.rules.getAllRulesObjects()
    """
    from conf.rules import getAllRulesObjects
    return getAllRulesObjects()


def get_rules(type=None, id=None):
    """ Take rule information passed by user, and return list of rules filtered

        :param: type: rule's type (same as type yaml file) passed by user
        :param: id: rule's id passed by user
        :type: type: list of str
        :type: id: list of int
        :return: list of Rule Objects filtered
        :rtype: list of Rule Objects

        ..seealso:: heimdall.conf.hosts.getPlateformObject(), heimdall.conf.rules.getAllRulesObjects()
    """

    from conf.rules import getAllRulesObjects, getTypeObject

    rules_availables = []
    all_rules = getAllRulesObjects()

    if not type:
        if id:  # if not type set, and id is set filter by id
            [rules_availables.append(r) for ri in id for r in all_rules if r.id == ri]
            return rules_availables
        else:  # id and type are not set, return all_rules
            return all_rules

    # type is set
    types = []
    [types.append(getTypeObject(t)) for t in type]

    if id:  # if id is set, filter by id AND type
        for ri in id:
            [rules_availables.append(r) for t in types for r in t.rules if r.id == ri]
        return rules_availables
    else:  # if id is not set, filter by type only
        [rules_availables.append(r) for t in types for r in t.rules]
        return rules_availables


def add_rule(**kwargs):
    """ Create a Rule Object from information passed by user, and return a TypeObject who contain the new rule Object.

        Keyword Args:
            type (list of one str): rule's type (same as type yaml file) passed by user
            desc (list of one str): rule's description passed by user
            auditcmd (list of str): rule's auditcmd passed by user
            auditscript (list of str): rule's auditscript passed by user
            remedcmd (list of str): rule's remedcmd passed by user
            remedscript (list of str): rule's remedscript passed by use

        :return: updated Type with the new Rule Object
        :rtype: Type Object

        ..seealso: heimdall.core.rule.Rule, heimdall.core.type.Type, heimdall.conf.rules.getTypeObject
    """
    from core.rule import Rule
    # Create new dict with no empty values AND string format if value is list of one element
    newrule = {}
    for k, v in kwargs.iteritems():
        if not v:  # no value passed for this key, just pass
            pass
        elif 'audit' in k:  # key can be 'auditcmd' or 'auditscript', merge into 'audit' key.
            newrule['audit'] = kwargs[k]
        elif 'remed' in k:  # key can be 'remedcmd' or 'remedscript', merge into 'remed' key.
            newrule['remed'] = kwargs[k]
        else:  # type and desc are list of one element
            newrule[k] = kwargs[k][0]

    rule = Rule(**newrule)

    from conf.rules import getTypeObject

    t = getTypeObject(rule.type)  # Retrieve Type Object from rule type attribute
    rule.id = t.get_new_id()  # Setting new id
    from utils.wiki import create_wikirule
    create_wikirule(rule)
    rule.check_wikipage()
    t.add_rule(rule)

    return t


def remove_rule(type=None, id=None):
    """ Remove Rule Object from Type Object attribute rules and return updated Type Object.

        :param: type: rule's type (same as type yaml file) passed by user
        :param: id: rule's id passed by user
        :type: type: list of one str
        :type: id: list of one int
        :return: Updated Type
        :rtype: Type Object

        .. seealso:: heimdall.conf.rules.getTypeObject(), heimdall.core.type.Type
    """
    from conf.rules import getTypeObject
    from utils.wiki import remove_wikirule
    t = getTypeObject(type[0])

    removed_rules = []
    if id:
        from conf.rules import getRuleObject
        for i in id:
            for r in t.rules:
                if str(i) == str(r.id):
                    removed_rules.append(r)
    else:
        removed_rules = t.rules

    for r in removed_rules:
        t.remove_rule(r)
        remove_wikirule(r)

    return t


def move_rule(oldtype=None, id=None, newtype=None):
    """ Move rule from one type to another.
        Retrieve old Type Object and new Type Object and update both with the Rule Object filter by id.

        :param: oldtype: old rule's type (same as type yaml file).
        :param: id: rule's id passed by user.
        :param: newtype: new rule's type (same as type yaml file).
        :type: oldtype: list of one str
        :type: id: list of one int
        :type: newtype: list of one str
        :return: Updated old Type and new Type
        :rtype: Old Type Object, New Type Object

        .. seealso:: heimdall.conf.rules.getTypeObject(), heimdall.core.type.Type
    """
    from conf.rules import getTypeObject
    from utils.wiki import move_wikirule
    old = getTypeObject(oldtype[0])
    new = getTypeObject(newtype[0])

    for r in old.rules:
        if str(r.id) == str(id[0]):  # We found our Rule
            oldid = r.id
            r.type = new.name
            r.id = new.get_new_id()
            old.remove_rule(r)
            new.add_rule(r)
            move_wikirule(old, new, oldid, r.id)
    return old, new


def update_rule(**kwargs):
    """ Update a Rule Object from information passed by user, and return a TypeObject who contain the new rule Object.

        Keyword Args:
            type (list of str): rule's type (same as type yaml file) passed by user
            desc (list of str): rule's description passed by user
            id (list of int): rule's id passed by user
            auditcmd (list of str): rule's auditcmd passed by user
            auditscript (list of str): rule's auditscript passed by user
            remedcmd (list of str): rule's remedcmd passed by user
            remedscript (list of str): rule's remedscript passed by use

        :return: updated Type with the new Rule Object
        :rtype: Type Object

        ..seealso: heimdall.core.rule.Rule, heimdall.core.type.Type, heimdall.conf.rules.getTypeObject
    """
    from conf.rules import getTypeObject

    t = getTypeObject(kwargs.get('type')[0])
    audit = []
    remed = []
    for r in t.rules:
        if str(r.id) == str(kwargs.get('id')[0]):  # We found our Rule
            for k, v in kwargs.iteritems():
                if v:
                    if 'audit' in k:  # key can be 'auditcmd' or 'auditscript', merge into 'audit' key.
                        [audit.append(val) for val in v]
                    elif 'remed' in k:  # key can be 'remedcmd' or 'remedscript', merge into 'remed' key.
                        [remed.append(val) for val in v]
                    elif k == 'id':
                        r.__setattr__('id', kwargs.get('id')[0])
                    else:
                        # update attributes with new values
                        r.__setattr__(k, v[0]) if v else r.__setattr__(k, '')
            if audit:
                r.__setattr__('audit', audit)
            if remed:
                r.__setattr__('remed', remed)
            print r.audit
    return t


def link_rule(profile=None, type=None, id=None):
    """ Link rule to a profile.
        Retrieve Profile Object and update it with new Type Object who contains Rules Objects.

        :param: profile: profile name (same as profile yaml file).
        :param: type: rule's type (same as type yaml file).
        :param: id: rule's id passed by user.
        :type: profile: list of str
        :type: type: list of str
        :type: id: list of int
        :return: list of profile name updated
        :rtype: list of str

        .. seealso:: heimdall.conf.rules.getTypeObject(), heimdall.core.type.Type, heimdall.conf.profiles.getProfileObject()
    """
    from conf.profiles import getProfileObject
    from utils.profile import update_profile
    from conf.rules import getTypeObject, getRuleObject

    for prof in profile:
        p = getProfileObject(prof)
        for ty in p.types:
            if ty.name == type[0]:  # If type exist in profile, we just add all rules or one from this type.
                if id == -1:  # Deleting all rules, and add Type Object with all rules.
                    p.remove_type(ty)
                    p.add_type(getTypeObject(type[0]))
                else:  # add new Rules Objects to Type Object for all id passed by user
                    [ty.add_rule(getRuleObject(ty.name, i)) for i in id]
        else:  # Profile object doesnt have this type
            if id == -1:
                p.add_type(getTypeObject(type[0]))
            else:
                p.add_type(getTypeObject(type[0], id))
        update_profile(p)
    return profile


def unlink_rule(profile=None, type=None, id=None):
    """ Unlink rule to a profile.
        Retrieve Profile Object and update it with new Type Object with Rules Objects deleted.

        :param: profile: profile name (same as profile yaml file).
        :param: type: rule's type (same as type yaml file).
        :param: id: rule's id passed by user.
        :type: profile: list of str
        :type: type: list of str
        :type: id: list of int
        :return: list of profile name updated
        :rtype: list of str

        .. seealso:: heimdall.conf.rules.getTypeObject(), heimdall.core.type.Type, heimdall.conf.profiles.getProfileObject()
    """
    from conf.profiles import getProfileObject
    from utils.profile import update_profile
    from core.profile import Profile

    for prof in profile:
        if not isinstance(prof, Profile):
            p = getProfileObject(prof)
        else:
            p = prof
        if id == -1:  # remove all
            [p.remove_type(t) for t in p.types if t.name == type[0]]
        else:
            update_needed = False
            for t in p.types:
                rules_num = len(t.rules)
                if t.name == type[0]:
                    [t.remove_rule(r) for r in t.rules for i in id if str(i) == str(r.id)]
                if rules_num != len(t.rules):
                    update_needed = True

        if update_needed:  # one or more rules has been removed
            update_profile(p)
    return profile


def check_rule(type=None, id=None):
    """ Check if rule exist.

        :param: type: rule's name passed by user.
        :param: id: rule's name passed by user.
        :type: type: list of one str
        :type: type: list of one int elem
        :return: True if rule exist, False otherwise.
        :rtype: bool

        .. seealso:: heimdall.conf.rules.getTypeObject()
    """
    if not type and not id:
        return False

    from conf.rules import getTypeObject
    from core.exceptions import RuleDoesNotExist

    try:
        for ty in type:
            t = getTypeObject(ty)
            for i in id:
                if not t.check_id_exist(i):
                    raise RuleDoesNotExist('Rule from type %s with id %s Does not exist!' % (t.name, i))
        else:
            return True
    except RuleDoesNotExist as rne:
        print rne
        exit(rne.code)


def check_rule_exist(type=None, id=None):
    """ Check if rule already exist.

        :param: type: rule's name passed by user.
        :param: id: rule's name passed by user.
        :type: type: list of one str
        :type: id: list of one int
        :return: True if rule doesnt exist, False otherwise.
        :rtype: bool

        .. seealso:: heimdall.conf.rules.getTypeObject()
    """
    if not type and not id:
        return

    from conf.rules import getTypeObject
    from core.exceptions import RuleAlreadyExist

    try:
        for ty in type:
            t = getTypeObject(ty)
            rule_id = []
            [rule_id.append(r.id) for r in t.rules]
            exist = set(rule_id).intersection(set(id))
            if exist:
                raise RuleAlreadyExist('Rule from type %s with id %s already exist!' % (t.name, next(iter(exist))))
        else:
            return False
    except RuleAlreadyExist as rae:
        print rae
        exit(rae.code)
