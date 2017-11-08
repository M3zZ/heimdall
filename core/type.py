# -*- coding: utf-8 -*-


class Type(object):
    """ Class who define a rule.
         yml files are read from heimdall/conf/rules/type_name.yml and used for Type Object instantiation

         Keyword Args:
             :param: name: type's name.
             :param: id: type's id.
             :param: desc: type's description.
             :param: path: type's path to yaml file.
             :param: rules: list of Rule Objects.
             :param: all: True if contains all Rule, False otherwise.
             :type: name: str
             :type: id: int
             :type: desc: str
             :type: path: list of str
             :type: rules: list of Rule Object
             :type: all: boolean
             :return: Type object
             :rtype: object
     """

    def __init__(self, **kwargs):
        self.id = kwargs.get('id', 1)
        self.name = kwargs.get('name', '')
        self.desc = kwargs.get('desc', '')
        self.path = kwargs.get('path', '')
        self.rules = []  # List that contains all rules object in this type
        self.all = False

    def __str__(self):
        return super(Type, self).__str__()

    def __repr__(self):
        return super(Type, self).__repr__()

    def __setattr__(self, name, value):
        return object.__setattr__(self, name, value)

    def __getattribute__(self, name):
        return object.__getattribute__(self, name)

    def __iter__(self):
        del self.__dict__['all']
        for k, v in self.__dict__.iteritems():
            if k == 'rules':
                v = []
                for r in self.rules:
                    v.append(dict(r))
            yield (k, v)

    def get_new_id(self):
        """ Return a new id available for a rule.

            :return: Length of list of all Rule Objects in rules attribute.
            :rtype: int
        """
        return len(self.rules) + 1

    def check_id_exist(self, id):
        """ Check if id exist in list of all Rule Objects.

            :param id:
            :type: id: int
            :return: If id exist return id, return False otherwise.
            :rtype: bool or int
        """
        exist = False
        for i in self.rules:
            if str(i.id) == str(id):
                exist = i
        return exist

    def remove_rule(self, rule):
        """ Remove a Rule Object from Type.

            :param: rule: Rule Object that must be removed.
            :type: rule: Rule Object
            :return: Updated Type Object
            :rtype: Type Object
        """
        self.rules.remove(rule)
        return self

    def add_rule(self, rule):
        """ Add a Rule Object to Type.

            :param: rule: Rule Object that must be added.
            :type: rule: Rule Object
            :return: Updated Type Object
            :rtype: Type Object
        """
        self.rules.append(rule)
        return self
