# -*- coding: utf-8 -*-

from os import path, listdir

__tdir__ = path.dirname(__file__)
__typesfiles__ = [rf for rf in listdir(__tdir__) if
                  (path.isfile(path.join(__tdir__, rf)) and '.yml' in path.basename(path.join(__tdir__, rf)))]


def getAllTypesObjects():
    """ Open and read data from heimdall/conf/rules/type.yaml, then create Type Objects from data.
        Rule Objects are also created and added to Type Objects.

        :return: list of all Type Objects available.
        :rtype: list of Type Objects

        ..seealso:: heimdall.core.type.Type, heimdall.core.rule.Rule
    """
    from core.type import Type
    from core.rule import Rule
    from core.yml import open_yml

    type_availables = []
    for type in __typesfiles__:
        filepath = path.join(__tdir__, type)
        type_data = open_yml(path=filepath)
        if type_data:
            type_data['path'] = filepath
            type = Type(**type_data)
            for r in type_data['rules']:
                r['type'] = type.name
                type.rules.append(Rule(**r))
                type.all = True
            type_availables.append(type)
    return type_availables


def getTypeObject(name=None, id=None):
    """ Open and read data from type name passed by user, then create Type Object from data
        Rule Objects are also created and added to Type Object.

        :return: Type Object created from data read in heimdall/conf/rules/type.yml.
        :rtype: Type Object

        ..seealso:: heimdall.core.type.Type, heimdall.core.rule.Rule
    """
    from core.type import Type
    from core.rule import Rule
    from core.yml import open_yml

    filepath = path.join(__tdir__, name + '.yml')
    type_data = open_yml(path=filepath)
    if type_data:
        type_data['path'] = filepath
        type = Type(**type_data)
        for r in type_data['rules']:
            r['type'] = type.name
            if id and id != -1:
                for i in id:
                    if str(i) == str(r['id']):
                        type.rules.append(Rule(**r))
                        type.all = False
            else:
                type.rules.append(Rule(**r))
                type.all = True
        return type


def getAllRulesObjects():
    """ Open and read data from heimdall/conf/rules/type.yaml, then create Rule Objects from data.

        :return: list of all Rule Objects available.
        :rtype: list of Rule Objects

        ..seealso:: heimdall.core.rule.Rule
    """
    from core.rule import Rule
    from core.yml import open_yml

    rules_availables = []
    for type in __typesfiles__:
        filepath = path.join(__tdir__, type)
        type_data = open_yml(path=filepath)
        if type_data:
            for r in type_data['rules']:
                r['type'] = type_data['name']  # Adding type for format_output
                rules_availables.append(Rule(**r))
    return rules_availables


def getRuleObject(type=None, id=None):
    """ Open and read data from type name passed by user, then create Rule Object from data filtered by id.

        :return: Rule Object created from data read in heimdall/conf/rules/type.yml.
        :rtype: Rule Object

        ..seealso:: heimdall.core.rule.Rule
    """
    from core.rule import Rule
    from core.exceptions import RuleDoesNotExist
    from core.yml import open_yml

    filepath = path.join(__tdir__, type + '.yml')
    type_data = open_yml(path=filepath)

    try:
        if type_data:
            for r in type_data['rules']:
                if str(id) == str(r.get('id')):
                    r['type'] = type_data['name']
                    return Rule(**r)
            else:
                raise RuleDoesNotExist('Rule from type %s with id %s Does not exist!' % (type_data.get('name'), id))
    except RuleDoesNotExist as rde:
        print rde
        exit(rde.code)
