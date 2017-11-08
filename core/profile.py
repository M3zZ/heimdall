# -*- coding: utf-8 -*-


class Profile(object):
    """ Class who define a profile.
         yml files are read from heimdall/conf/profiles/profile.yml and used for Profile Object instantiation

         Keyword Args:
             :param: name: profile's name.
             :param: id: profile's id.
             :param: desc: profile's description.
             :param: path: profile's path to yaml file.
             :param: types: list of Type Objects.
             :type: name: str
             :type: id: int
             :type: desc: str
             :type: path: list of str
             :type: types: list of Type Object
             :return: Profile object
             :rtype: object
     """

    def __init__(self, **kwargs):
        self.name = kwargs.get('name', '')
        self.id = kwargs.get('id', 1)
        self.desc = kwargs.get('desc', '')
        self.path = kwargs.get('path', '')
        self.types = []

    def __str__(self):
        return super(Profile, self).__str__()

    def __repr__(self):
        return super(Profile, self).__repr__()

    def __setattr__(self, name, value):
        return super(Profile, self).__setattr__(name, value)

    def __getattribute__(self, name):
        return super(Profile, self).__getattribute__(name)

    def __iter__(self):
        for k, v in self.__dict__.iteritems():
            if k == 'types':
                v = {}
                for t in self.types:
                    if not t.all:
                        list_id = []
                        [list_id.append(r.id) for r in t.rules]
                    else:
                        list_id = -1
                    v.update({t.name: list_id})
            yield (k, v)

    def add_type(self, type):
        self.types.append(type)
        return self

    def remove_type(self, type):
        if type == -1:
            self.types = []
        else:
            if isinstance(type, list):
                [self.types.remove(t) for t in type]
            else:
                self.types.remove(type)
        return self
