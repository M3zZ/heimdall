#!/usr/bin/env python
# -*- coding: utf-8 -*-

from core.exceptions import RuleDataError


class Rule(object):
    """ Class who define a rule.
        yml files are read from heimdall/conf/rules/type_name.yml and used for Rule Object instantiation

        Keyword Args:
            :param: type: rule's type.
            :param: id: rules's id.
            :param: desc: rules's description.
            :param: audit: rule's audit commands or script (must be a list)
            :param: remed: rule's remed commands or script (must be a list)
            :param: wikipage: if rule has or not a wikipage
            :type: type: str
            :type: id: int
            :type: desc: str
            :type: audit: list of str
            :type: remed: list of str
            :type: wikipage: boolean
            :return: Rule object
            :rtype: object
    """

    def __init__(self, **kwargs):
        self.type = kwargs.get('type', '')
        self.id = kwargs.get('id', 1)
        self.desc = kwargs.get('desc', '')
        self.audit = kwargs.get('audit', '')
        self.remed = kwargs.get('remed', '')
        self.wikipage = self.check_wikipage()

        try:
            if not isinstance(self.audit, list):
                raise RuleDataError("Audit commands/scripts must be a list", self.type)
            if self.remed and not isinstance(self.remed, list):
                raise RuleDataError("Remediation commands/scripts must be a list", self.type)
        except RuleDataError as rde:
            print rde
            exit(rde.code)

    def __str__(self):
        return super(Rule, self).__str__()

    def __repr__(self):
        return super(Rule, self).__repr__()

    def __setattr__(self, name, value):
        return object.__setattr__(self, name, value)

    def __getattribute__(self, name):
        return object.__getattribute__(self, name)

    def __iter__(self):
        for k, v in self.__dict__.iteritems():
            yield (k, v)

    def check_wikipage(self):
        from wikibase import __wikipath__
        from os import path
        if self.type:
            if path.isfile(path.join(path.join(__wikipath__, self.type), '%s-%s.html' % (self.type, self.id))):
                self.wikipage = '%s-%s.html' % (self.type, self.id)
            else:
                self.wikipage = 'DEFAULT.html'
        else:
            self.wikipage = 'DEFAULT.html'
        return self.wikipage
