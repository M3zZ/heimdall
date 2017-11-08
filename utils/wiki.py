# -*- coding: utf-8 -*-

from os import mkdir, path, rename, removedirs, remove, listdir

from wikibase import __wikipath__


def create_wikidir(type=None):
    if not path.isdir(path.join(__wikipath__, type.name)):
        mkdir(path.join(__wikipath__, type.name))
    return


def rename_wikidir(oldtype=None, newtype=None):
    if path.isdir(path.join(__wikipath__, oldtype.name)):
        rename(path.join(__wikipath__, oldtype.name), path.join(__wikipath__, newtype.name))


def remove_wikidir(type=None):
    if path.isdir(path.join(__wikipath__, type.name)):
        for file in listdir(path.join(__wikipath__, type.name)):
            remove(path.join(path.join(__wikipath__, type.name), file))
        removedirs(path.join(__wikipath__, type.name))
    return


def create_wikirule(rule=None):
    skel_wiki_rule = "{% set name = \"Insert rule name here\" %}\n" + \
                     "{% set description = \"Insert rule description here\" %}\n" + \
                     "{% set rationale = \"Insert rule rationale here\" %}\n" + \
                     "{% include 'wiki_template.jinja' with context %}"
    rpath = path.join(path.join(__wikipath__, rule.type), '%s-%s.html' % (rule.type, rule.id))
    if not path.isfile(rpath):
        fd = open(rpath, 'a')
        fd.write(skel_wiki_rule)
        fd.close()
    print "[*] - Wikipage for rule type: %s id: %s created at %s, don't forget to add name/description/rationale " \
          % (rule.type, rule.id, rpath)
    return


def move_wikirule(oldtype=None, newtype=None, oldruleid=None, newruleid=None):
    if path.join(path.join(__wikipath__, oldtype.name), '%s-%s.html' % (oldtype.name, oldruleid)):
        oldpath = path.join(path.join(__wikipath__, oldtype.name), '%s-%s.html' % (oldtype.name, oldruleid))
        newpath = path.join(path.join(__wikipath__, newtype.name), '%s-%s.html' % (newtype.name, newruleid))
        rename(oldpath, newpath)
    return


def remove_wikirule(rule=None):
    if path.isfile(path.join(path.join(__wikipath__, rule.type), '%s-%s.html' % (rule.type, rule.id))):
        remove(path.join(path.join(__wikipath__, rule.type), '%s-%s.html' % (rule.type, rule.id)))
    return
