#!/usr/bin/env python
# -*- coding: utf-8 -*-

from os import path

from conf.scripts import __auditscriptsfile__, __remedscriptsfile__


def add_script(script_type=None, scriptpath=None, name=None):
    """ Add properly a new audit/remed script.

    :param: script_type: script's type (audit or remediation)
    :param: scriptpath: path to script to add.
    :param: name: script name.
    :type: script_type: str
    :type: scriptpath: str
    :type: name: str
    :return: path to added script
    :rtype: str
    """
    from conf.scripts import __auditdir__, __remeddir__
    if 'audit' in script_type:
        directory = __auditdir__
    else:
        directory = __remeddir__
    try:
        if '.sh' != name[0][-3:]:
            name[0] += '.sh'
        if check_script(scriptpath[0]):
            from shutil import copyfile
            copyfile(scriptpath[0], path.join(directory, name[0]))
            print "script %s successfully created !" % name[0]
            return path.join(directory, name[0])
    except IOError as ioe:
        print 'Error during %s copy!' % scriptpath
        print ioe


def remove_script(script_type=None, name=None):
    """ Remove properly an audit/remed script.

    :param: script_type: script's type (audit or remediation)
    :param: name: script name.
    :type: script_type: str
    :type: name: str
    :return: path to removed script
    :rtype: str
    """
    from conf.scripts import __auditdir__, __remeddir__
    if 'audit' in script_type:
        directory = __auditdir__
    else:
        directory = __remeddir__
    try:
        if check_script(path.join(directory, name[0])):
            from os import remove
            remove(path.join(directory, name[0]))
            print "script %s successfully deleted !" % name[0]
            return path.join(directory, name[0])
    except IOError as ioe:
        print 'Error during %s remove!' % path.join(directory, name)
        print ioe


def get_script(script_type=None):
    """ Print the list of existing scripts.

    :param: script_type: script's type (audit or remediation)
    :type: script_type: str
    """
    if not script_type:
        print "Audit scripts :"
        for s in __auditscriptsfile__:
            print "\t- %s" % s.split('/')[-1]
        print "\nRemediation scripts :"
        for s in __remedscriptsfile__:
            print "\t- %s" % s.split('/')[-1]
    elif script_type[0] == 'audit':
        print "Audit scripts :"
        for s in __auditscriptsfile__:
            print "\t- %s" % s.split('/')[-1]
    else:
        for s in __remedscriptsfile__:
            print "\t- %s" % s.split('/')[-1]


def check_script(scriptpath=None):
    """ Check if script exist.

    :param: scriptpath: path to script to add.
    :type: scriptpath: str
    :return: True if script exist, raise an Exception otherwise.
    :rtype: bool
    """
    from core.exceptions import ScriptDoesNotExist
    try:
        if path.isfile(scriptpath):
            return True
        else:
            raise ScriptDoesNotExist("Script %s doesnt exists!" % scriptpath)
    except ScriptDoesNotExist as sne:
        print sne
        exit(sne.code)
