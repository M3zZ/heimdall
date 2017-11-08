# -*- coding: utf-8 -*-


def get_all_profiles():
    """ Return all Profile Objects read from yaml file in heimdall/conf/profiles/profile.yml

        :return: return all Profile Objects
        :rtype: list of Profile Objects

        .. seealso:: heimdall.conf.profiles.getAllProfilesObjects()
    """
    from conf.profiles import getAllProfilesObjects
    return getAllProfilesObjects()


def get_profile(profiles=None, type=None, id=None):
    """ Take profile information passed by user, and return list of Profile Objects filtered.

        :param: profiles: list of profiles's name (same as type yaml file) passed by user
        :param: type: list of type's name (same as type yaml file) passed by user
        :param: id: list of rule's id (same as type yaml file) passed by user
        :type: profiles: list of str
        :type: type: list of str
        :type: id: list of int
        :return: list of Profile Objects filtered
        :rtype: list of Profile Objects

        ..seealso:: heimdall.conf.profiles.getProfileObject()
    """
    from conf.profiles import getAllProfilesObjects, getProfileObject

    profiles_availables = []
    all_profile = []
    if profiles:
        [all_profile.append(getProfileObject(p)) for p in profiles]
    else:
        all_profile = getAllProfilesObjects()

    for p in all_profile:
        rtype = []
        rulesid = []
        if type:
            [rtype.append(t) for t in p.type if t.name in type]
            if rtype:
                if id:
                    [rulesid.append(r.id) for rt in rtype for r in rt.rules]
                    if set(rulesid).intersection(id):
                        profiles_availables.append(p)
                else:
                    profiles_availables.append(p)
        elif id:
            [rtype.append(t) for t in p.type]
            [rulesid.append(r.id) for rt in rtype for r in rt.rules]
            if set(rulesid).intersection(id):
                profiles_availables.append(p)
        else:
            profiles_availables = all_profile

    return profiles_availables


def add_profile(name=None, desc=None):
    """ Create a Profile Object from information passed by user, and return it.

        :param: name: profile's name (same as profile yaml file) passed by user.
        :param: desc: profile's description.
        :type: name: list of one str
        :type: desc: list of one str
        :return: new Profile Object
        :rtype: Profile Object

        ..seealso: heimdall.core.profile..Profile, update_profile()
    """
    from core.profile import Profile
    from conf.profiles import __pdir__

    newprofile = {'id': get_new_id(), 'name': name[0], 'desc': desc[0], 'path': __pdir__ + '/' + name[0] + '.yml',
                  'types': []}
    p = Profile(**newprofile)
    update_profile(p)
    return p


def update_profile(profile=None):
    """ Take a Profile Object and write his data in type.yml file.

        :param: profile: a Profile object
        :type: profile: Profile Object
        :return: True if succeed, raise an error otherwise.
        :rtype: bool

        .. seealso:: heimdall.core.yml.write_yml(), heimdall.core.type.Type
    """
    from core.profile import Profile
    from core.yml import write_yml
    from core.exceptions import ProfileTypeError

    try:
        if isinstance(profile, Profile):
            write_yml(path=profile.path, data=profile)
            print "[*] - Profile %s successfully updated" % profile.name
            return True
        else:
            raise ProfileTypeError("Argument passed to %s must be a Profile Object." % update_profile.__name__)
    except ProfileTypeError as pte:
        print pte
        exit(pte.code)


def update_self_profile(name=None, desc=None, newname=None):
    """ Update a Profile Object from information passed by user, and return the new Profile Object created.
        New object is write in corresponding yaml file.

        :param: name: profile's name (same as profile yaml file) passed by user
        :param: desc: profile's description passed by user
        :param: newname: profile's new name (profile yaml file will be rename) passed by user
        :type: name: list of one str element
        :type: desc: list of one str element
        :type: newname: list of one str element
        :return: updated new Profile Object
        :rtype: Profile Object

        .. seealso:: heimdall.conf.profiles.getProfileObject(), heimdall.core.yml.rename_yml(), update_profile()
    """
    from core.profile import Profile
    from core.yml import rename_yml
    from conf.profiles import getProfileObject
    from core.exceptions import ProfileTypeError

    p = getProfileObject(name[0])
    oldpath = p.path

    if desc:
        p.desc = desc[0]
    if newname:
        p.name = newname[0]
        p.path = p.path.replace(name[0], newname[0])

    try:
        if isinstance(p, Profile):
            rename_yml(oldpath=oldpath, newpath=p.path)
            update_profile(p)
            return True
        else:
            raise ProfileTypeError("Argument passed to %s must be a Profile Object." % update_profile.__name__)
    except ProfileTypeError as pte:
        print pte
        exit(pte.code)

    update_profile(p)
    return p


def remove_profile(name=None):
    """ Remove profile file from profile name passed by user.

        :param: name: profile's name (same as plateform yaml file) passed by user
        :type: name: list of one str element
        :return: True if remove succeed
        :rtype: bool

        .. seealso:: heimdall.conf.profiles.getProfileObject(), heimdall.core.yml.remove_yml()
    """
    from core.yml import remove_yml
    from core.profile import Profile
    from conf.profiles import getProfileObject
    from core.exceptions import ProfileTypeError
    p = getProfileObject(name[0])
    try:
        if isinstance(p, Profile):
            remove_yml(p.path)
            print "[*] - Profile %s successfully removed" % name
            return True
        else:
            raise ProfileTypeError("Argument passed to %s must be a Profile Object." % update_profile.__name__)
    except ProfileTypeError as pte:
        print pte
        exit(pte.code)


def get_new_id():
    """ Return a new id available from all profile.
        If heimdall/conf/profile/ is empty, return 1

        :return: new id if one plateform exist, 1 otherwise
        :rtype: int

        .. seealso:: heimdall.conf.profiles.getAllProfilesObjects
    """
    from conf.profiles import getAllProfilesObjects

    allprofiles = getAllProfilesObjects()

    if not allprofiles:
        return 1

    newid = []
    [newid.append(t.id) for t in allprofiles]
    return max(newid) + 1


def check_profile(profile=None):
    """ Check if profile exist by profile name.

        :param: profile: profile's name passed by user.
        :type: profile: list of str
        :return: True if profile exist, False otherwise.
        :rtype: bool

        .. seealso:: heimdall.conf.profiles.getAllProfilesObjects
    """
    from conf.profiles import getAllProfilesObjects
    from core.exceptions import ProfileDoesNotExist

    if not profile:
        return False

    profile_available = []
    [profile_available.append(p.name) for p in getAllProfilesObjects()]
    try:
        for p in profile:
            if p not in profile_available:  # Check profile exist
                raise ProfileDoesNotExist("Profile %s doesnt exist !" % profile)
        else:
            return True
    except ProfileDoesNotExist as pne:
        print pne
        exit(pne.code)


def clean_profiles(type=None, id=None):
    """ update profile file when one or more rules are deleted.

        :param: type: type's name passed by user.
        :param: id: rule's id passed by user.
        :type: type: list of str
        :type: id: list of int
        :return: True
        :rtype: bool

        .. seealso:: heimdall.conf.profiles.getAllProfilesObjects(), heimdall.utils.rule.unlink_rule()
    """
    from conf.profiles import getAllProfilesObjects
    from utils.rule import unlink_rule

    if not id:
        id = -1
    unlink_rule(getAllProfilesObjects(), type, id)
    return True
