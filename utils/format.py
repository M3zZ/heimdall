# -*- coding: utf-8 -*-
""" Formating Output class """

from core.host import Host
from core.plateform import Plateform
from core.profile import Profile
from core.rule import Rule
from core.type import Type


def format_output(object=None):
    for o in object:
        if isinstance(o, Type):
            print print_box_type(o)
        if isinstance(o, Rule):
            print print_box_rules(o)
        if isinstance(o, Profile):
            print print_box_profile(o)
        if isinstance(o, Plateform):
            print print_box_plateform(o)
        if isinstance(o, Host):
            print print_box_rules(o)


def print_box_type(data):
    """ Transform a Type Object to format string

    :param: data: Type Object where print format is needed.
    :type: data: Type Object
    :return: format string.
    :rtype: str
    """
    form = '|{:^%ds}|{:^%ds}|\n'
    box_table = ''
    if data:
        max_key_len = 0
        max_value_len = 0
        type_data = dict(data)
        for k, v in type_data.iteritems():
            if k == 'all':
                del type_data[k]
            if k == 'rules':
                id_len = ', '.join(str(x['id']) for x in v)  # We just want the length of id list
                if len(id_len) > max_value_len:
                    max_value_len = len(id_len)
            if len(k) > max_key_len:
                max_key_len = len(k)
            if len(str(v)) > max_value_len and k != 'rules':
                max_value_len = len(str(v))
        max_key_len += 10
        max_value_len += 10
        box_table += '+' + '-' * ((max_value_len + max_key_len) + 1) + '+' + '\n'
        i = 0
        for k, v in type_data.iteritems():
            if i:
                box_table += '|' + '-' * max_key_len + '|' + '-' * max_value_len + '|\n'
            else:
                i = 1
            if k == 'rules':
                id_list = []
                [id_list.append(value) for i in v for key, value in i.iteritems() if key == 'id']
                box_table += (form % (max_key_len, max_value_len)).format(k, id_list)
            else:
                box_table += (form % (max_key_len, max_value_len)).format(k, str(v))
        box_table += '+' + '-' * ((max_value_len + max_key_len) + 1) + '+'

        return box_table
    else:
        return ''


def print_box_rules(data):
    """ Transform a Rule or Host Object to format string

    :param: data: Rule / Host Object where print format is needed.
    :type: data: Rule / Host Object
    :return: format string.
    :rtype: str
    """
    form = '|{:^%ds}|{:^%ds}|\n'
    box_table = ''
    if data:
        max_key_len = 0
        max_value_len = 0
        for k, v in dict(data).iteritems():
            if len(k) > max_key_len:
                max_key_len = len(k)
            if isinstance(v, list):
                for i in v:
                    if len(str(i)) > max_value_len:
                        max_value_len = len(str(i))
            else:
                if len(str(v)) > max_value_len:
                    max_value_len = len(str(v))
        max_key_len += 10
        max_value_len += 20
        box_table += '+' + '-' * ((max_value_len + max_key_len) + 1) + '+' + '\n'
        i = 0
        for k, v in dict(data).iteritems():
            if i:
                box_table += '|' + '-' * max_key_len + '|' + '-' * max_value_len + '|\n'
            else:
                i = 1
            if isinstance(v, list):
                box_table += (form % (max_key_len, max_value_len)).format(k, str(v[0]))
                for value in v[1:]:
                    box_table += (form % (max_key_len, max_value_len)).format('', str(value))
            else:
                box_table += (form % (max_key_len, max_value_len)).format(k, str(v))
        box_table += '+' + '-' * ((max_value_len + max_key_len) + 1) + '+'

        return box_table
    else:
        return ''


def print_box_plateform(data):
    """ Transform a Plateform Object to format string

    :param: data: Plateform Object where print format is needed.
    :type: data: Plateform Object
    :return: format string.
    :rtype: str
    """
    form = '|{:^%ds}|{:^%ds}|\n'
    box_table = ''
    if data:
        key_len = [len(str(k)) for k in dict(data).keys()]
        value_len = [len(str(v)) for k, v in dict(data).iteritems() if k != 'environment']
        max_key_len = max(key_len) + 10
        max_value_len = max(value_len) + 10
        box_table += '+' + '-' * ((max_value_len + max_key_len) + 1) + '+' + '\n'
        i = 0
        for k, v in dict(data).iteritems():
            if i:
                box_table += '|' + '-' * max_key_len + '|' + '-' * max_value_len + '|\n'
            else:
                i = 1
            if isinstance(v, dict) and v:  # environment's hosts
                i = 0
                for key, value in v.iteritems():
                    host = []
                    [host.append(h['name']) for h in value]
                    out = '%s: %s' % (key, host)
                    if len(out) > max_value_len:  # if output of one couple key/value is > max_value_len set new length
                        max_value_len = len(out) + 5
                    if not i:
                        box_table += (form % (max_key_len, max_value_len)).format(k, out)  # first line
                        i = 1
                    else:
                        box_table += (form % (max_key_len, max_value_len)).format('', out)  # other lines
            else:
                box_table += (form % (max_key_len, max_value_len)).format(k, str(v))
        box_table += '+' + '-' * ((max_value_len + max_key_len) + 1) + '+'
        return box_table
    else:
        return ''


def print_box_profile(data):
    """ Transform a Profile Object to format string

    :param: data: Profile Object where print format is needed.
    :type: data: Profile Object
    :return: format string.
    :rtype: str
    """
    form = '|{:^%ds}|{:^%ds}|\n'
    box_table = ''
    if data:
        key_len = [len(str(k)) for k in dict(data).keys()]
        # Calculate value_len for all value except types which is a dictionnary
        value_len = [len(str(v)) for v in dict(data).values() if not isinstance(v, dict)]
        max_key_len = max(key_len) + 10
        max_value_len = max(value_len) + 5
        # Calculate length of keys + values from types dict
        for v in dict(data).values():
            if isinstance(v, dict):
                for key, value in v.iteritems():
                    out = '%s: %s' % (str(key), value)
                    if len(out) > max_value_len:  # if output of one couple key/value is > max_value_len set new length
                        max_value_len = len(out) + 5
        for k, v in dict(data).iteritems():
            box_table += '+' + '-' * ((max_value_len + max_key_len) + 1) + '+' + '\n'
            if isinstance(v, dict):
                i = 0
                for keys, values in v.iteritems():
                    out = '%s: %s' % (str(keys), values)
                    if not i:
                        box_table += (form % (max_key_len, max_value_len)).format(k, out)  # first line
                        i = 1
                    else:
                        box_table += (form % (max_key_len, max_value_len)).format('', out)  # other lines
            else:
                box_table += (form % (max_key_len, max_value_len)).format(k, str(v))
        box_table += '+' + '-' * ((max_value_len + max_key_len) + 1) + '+' + '\n'
        return box_table
    else:
        return ''
