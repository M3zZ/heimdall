# -*- coding: utf-8 -*-
from os import path, listdir

__pdir__ = path.dirname(__file__)
__profilesfiles__ = [pf for pf in listdir(__pdir__) if
                     (path.isfile(path.join(__pdir__, pf)) and 'yml' in path.basename(
                         path.join(__pdir__, pf)))]


def getAllProfilesObjects():
    """ Open and read data from heimdall/conf/profiles/profile.yml, then create Profile Objects from data.
        Type Objects are also created and added to Profile Objects.

        :return: list of all Profile Objects available.
        :rtype: list of Profile Objects

        ..seealso:: heimdall.core.profile.Profile, heimdall.conf.rules.getTypeObject()
    """
    from core.profile import Profile
    from conf.rules import getTypeObject
    from core.yml import open_yml

    profile_availables = []
    for profilesfiles in __profilesfiles__:
        filepath = path.join(__pdir__, profilesfiles)
        profile_data = open_yml(path=filepath)

        if profile_data:
            profile_data['path'] = filepath
            profile = Profile(**profile_data)
            [profile.types.append(getTypeObject(t, i)) for t, i in profile_data['types'].iteritems()]
            profile_availables.append(profile)

    return profile_availables


def getProfileObject(name=None):
    """ Open and read data from profile name passed by user, then create Profile Object from data
        Type Objects are also created and added to Profile Object.

        :return: Profile Object created from data read in heimdall/conf/profiles/profile.yml.
        :rtype: Profile Object

        ..seealso:: heimdall.core.profile.Profile, heimdall.conf.rules.getTypeObject()
    """
    from core.profile import Profile
    from conf.rules import getTypeObject
    from core.yml import open_yml

    filepath = path.join(__pdir__, name + '.yml')
    profile_data = open_yml(path=filepath)

    if profile_data:
        profile_data['path'] = filepath
        profile = Profile(**profile_data)
        [profile.types.append(getTypeObject(t, i)) for t, i in profile_data['types'].iteritems()]
        return profile
