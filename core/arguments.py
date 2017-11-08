#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse


class ArgumentsHandler:
    """ Simple class who initialize arguments passed to Heimdall."""

    def __init__(self):
        self.parser = initialize_args()


def rulesActionsHandler(args):
    """ Check rule action and execute associates functions.
        :param args: Rule action
        :return: Return result from the executed functions.
    """
    if 'get' == args.action:
        # get rule arguments :
        #   - id:
        #       type: int
        #       args number : 1 or more
        #       required: False
        #   - type:
        #       type: str
        #       args number: 1 or more
        #       required: False

        from utils.format import format_output
        if not args.id and not args.type:
            from utils.rule import get_all_rules
            rules = get_all_rules()
        else:
            if args.type:
                from utils.type import check_type
                check_type(type=args.type)
            from utils.rule import get_rules
            rules = get_rules(type=args.type, id=args.id)
        return format_output(rules)

    if 'add' == args.action:
        # add rule arguments :
        #   - type:
        #         type: str
        #         args number : 1
        #         required: True
        #   - desc:
        #         type: str
        #         args number: 1
        #         required: True
        #   - auditcmd:
        #       type: str
        #       args number: 1 or more
        #       required: False
        #       note: can't be set with auditscript
        #   - remedcmd:
        #       type: str
        #       args number: 1 or more
        #       required: False
        #       note: can't be set with remedscript
        #   - auditscript:
        #       type: str
        #       args number: 1
        #       required: False
        #       note: can't be set with auditcmd
        #   - remedscript:
        #       type: str
        #       args number: 1
        #       required: False
        #       note: can't be set with remedcmd

        from core.exceptions import RuleArgumentsError
        try:
            if args.audit_cmd and args.audit_script:
                raise RuleArgumentsError('Rule cant have auditscript AND auditcmd at the same time')
            # elif args.remed_cmd and args.remed_script:
            #     raise RuleArgumentsError('Rule cant have remedscript AND remedcmd at the same time')
            elif not (args.audit_cmd or args.audit_script):
                raise RuleArgumentsError('Rule must have at least one auditcmd OR one auditscript')
                # elif not (args.remed_cmd or args.remed_script):
                #     raise RuleArgumentsError('Rule must have at least one remedcmd OR one remedscript')
        except RuleArgumentsError as rvd:
            print rvd
            exit(rvd.code)

        from utils.type import update_type, check_type
        from utils.rule import add_rule

        check_type(type=args.type)
        updated_type = add_rule(desc=args.desc, type=args.type, audit_cmd=args.audit_cmd,
                                audit_script=args.audit_script, remed_cmd=args.remed_cmd,
                                remed_script=args.remed_script)
        return update_type(type=updated_type)

    if 'update' == args.action:
        # update rule arguments :
        #   - type:
        #       type: str
        #       args number : 1
        #       required: True
        #   - id:
        #       type: int
        #       args number : 1
        #       required: True
        #   - desc:
        #       type: str
        #       args number: 1
        #       required: False
        #   - auditcmd:
        #       type: str
        #       args number: 1 or more
        #       required: False
        #       note: can't be set with auditscript
        #   - remedcmd:
        #       type: str
        #       args number: 1 or more
        #       required: False
        #       note: can't be set with remedscript
        #   - auditscript:
        #       type: str
        #       args number: 1
        #       required: False
        #       note: can't be set with auditcmd
        #   - remedscript:
        #       type: str
        #       args number: 1
        #       required: False
        #       note: can't be set with remedcmd

        from core.exceptions import RuleArgumentsError

        try:
            # if args.audit_cmd and args.audit_script:
            #     raise RuleArgumentsError('Rule cant have auditscript AND auditcmd at the same time')
            # elif args.remed_cmd and args.remed_script:
            #     raise RuleArgumentsError('Rule cant have remedscript AND remedcmd at the same time')
            if not (args.audit_cmd or args.audit_script):
                raise RuleArgumentsError('Rule must have at least one auditcmd OR one auditscript')
        except RuleArgumentsError as rvd:
            print rvd
            exit(rvd.code)

        from utils.rule import update_rule, check_rule
        from utils.type import update_type

        check_rule(type=args.type, id=args.id)
        updated_type = update_rule(desc=args.desc, type=args.type, audit_cmd=args.audit_cmd,
                                   audit_script=args.audit_script, remed_cmd=args.remed_cmd,
                                   remed_script=args.remed_script, id=args.id)
        return update_type(updated_type)

    if 'remove' == args.action:
        # remove rule arguments :
        #   - type:
        #       type: str
        #       args number : 1
        #       required: True
        #   - id:
        #       type: int
        #       args number : 1
        #       required: True
        #   - all

        from core.exceptions import RuleArgumentsError
        try:
            if args.id:
                if args.all:
                    raise RuleArgumentsError("--all option doesn't need an id (all rules will be deleted)")
                else:
                    from utils.rule import check_rule
                    check_rule(type=args.type, id=args.id)

                    from utils.profile import clean_profiles
                    clean_profiles(type=args.type, id=args.id)

                    from utils.rule import remove_rule
                    updated_type = remove_rule(type=args.type, id=args.id)

                    from utils.type import update_type
                    return update_type(updated_type)
            else:
                if args.all:
                    from utils.profile import clean_profiles
                    clean_profiles(type=args.type)

                    from utils.rule import remove_rule
                    updated_type = remove_rule(type=args.type)

                    from utils.type import update_type
                    return update_type(updated_type)
                else:
                    raise RuleArgumentsError("For removing one rule, id must be set !")
        except RuleArgumentsError as rae:
            print rae
            exit(rae.code)

    if 'link' == args.action:
        # link rule arguments :
        #   - profile:
        #       type: str
        #       args number : 1 or more
        #       required: True
        #   - type:
        #       type: str
        #       args number : 1
        #       required: True
        #   - id:
        #       type: int
        #       args number: 1 or more
        #       required: False
        #   - all

        from core.exceptions import RuleArgumentsError

        try:
            if args.all and not args.type:
                raise RuleArgumentsError("--all options can't be used without rule type")
            if args.id:
                if args.all:
                    raise RuleArgumentsError("--all option doesn't need an id (all rules will be added)")

                from utils.rule import check_rule, link_rule
                check_rule(type=args.type, id=args.id)

                return link_rule(profile=args.profile, type=args.type, id=args.id)
            else:
                from utils.rule import link_rule
                return link_rule(profile=args.profile, type=args.type, id=-1)
        except RuleArgumentsError as rae:
            print rae
            exit(rae.code)

    if 'unlink' == args.action:
        # unlink rule arguments :
        #   - profile:
        #       type: str
        #       args number : 1 or more
        #       required: True
        #   - type:
        #       type: str
        #       args number : 1
        #       required: True
        #   - id:
        #       type: int
        #       args number: 1 or more
        #       required: False
        #   - all

        from core.exceptions import RuleArgumentsError
        try:
            if args.id:
                if args.all:
                    raise RuleArgumentsError("--all option doesn't need an id (all rules will be added)")
                else:
                    from utils.rule import unlink_rule, check_rule
                    check_rule(type=args.type, id=args.id)

                    return unlink_rule(profile=args.profile, type=args.type, id=args.id)
            else:
                from utils.rule import unlink_rule
                return unlink_rule(profile=args.profile, type=args.type, id=-1)
        except RuleArgumentsError as rae:
            print rae
            exit(rae)

    if 'move' == args.action:
        # move rule arguments :
        #   - type:
        #       type: str
        #       args number : 1
        #       required: True
        #   - id:
        #       type: int
        #       args number: 1 or more
        #       required: True
        #   - newtype:
        #       type: str
        #       args number : 1
        #       required: True
        #   - all

        from utils.type import check_type, update_type
        check_type(args.type)
        check_type(args.newtype)

        from utils.rule import check_rule, move_rule
        check_rule(type=args.type, id=args.id)
        updated_oldtype, updated_newtype = move_rule(oldtype=args.type, id=args.id, newtype=args.newtype)

        update_type(updated_oldtype)
        return update_type(updated_newtype)
    return


def scriptsActionsHandler(args):
    """ Check script action and execute associates functions.
        :param args: Script action
        :return: Return result from the executed functions.
    """
    if 'get' == args.action:
        # get script arguments :
        #   - type:
        #       type: str, choice [audit, remediation]
        #       args number : 1
        #       required: False

        from utils.format import format_output
        from utils.script import get_script
        return get_script(script_type=args.type)

    if 'add' == args.action:
        # add script arguments :
        #   - type:
        #       type: str, choice [audit, remediation]
        #       args number : 1
        #       required: True
        #   - path:
        #       type: str
        #       args number : 1
        #       required: True
        #   - name:
        #       type: str
        #       args number : 1
        #       required: True

        from utils.script import add_script
        return add_script(script_type=args.type, scriptpath=args.path, name=args.name)

    if 'remove' == args.action:
        # remove script arguments :
        #   - type:
        #       type: str, choice [audit, remediation]
        #       args number : 1
        #       required: True
        #   - name:
        #       type: str
        #       args number : 1
        #       required: True
        from utils.script import remove_script
        return remove_script(script_type=args.type, name=args.name)


def typesActionsHandler(args):
    """ Check type action and execute associates functions.
        :param args: Type action
        :return: Return result from the executed functions.
    """
    if 'get' == args.action:
        # get type arguments :
        #   - type:
        #       type: str
        #       args number : 1 or more
        #       required: False

        from utils.format import format_output
        if not args.type:
            from utils.type import get_all_types
            return format_output(get_all_types())
        else:
            from utils.type import check_type, get_type

            check_type(type=args.type)
            return format_output(get_type(name=args.type))

    if 'add' == args.action:
        # add type arguments :
        #   - type:
        #       type: str
        #       args number : 1
        #       required: True
        #   - desc:
        #       type: str
        #       args number : 1
        #       required: True

        from utils.type import add_type, check_type_exist

        check_type_exist(type=args.type)
        return add_type(name=args.type, desc=args.desc)

    if 'update' == args.action:
        # update type arguments :
        #   - type:
        #       type: str
        #       args number : 1
        #       required: True
        #   - desc:
        #       type: str
        #       args number : 1
        #       required: False
        #   - newname:
        #       type: str
        #       args number : 1
        #       required: False

        from utils.type import check_type, update_self_type

        check_type(type=args.type)
        return update_self_type(name=args.type, desc=args.desc, newname=args.newname)

    if 'remove' == args.action:
        # remove type arguments :
        #   - type:
        #       type: str
        #       args number : 1
        #       required: True

        from utils.type import check_type, remove_type
        from utils.profile import clean_profiles

        check_type(type=args.type)
        clean_profiles(type=args.type)
        return remove_type(name=args.type)
    return


def profilesActionsHandler(args):
    """ Check profile action and execute associates functions.
        :param args: Profile action
        :return: Return result from the executed functions.
    """
    if 'get' == args.action:
        # get profile arguments :
        #   - profile:
        #       type: str
        #       args number : 1 or more
        #       required: False
        #   - type:
        #       type: str
        #       args number : 1 or more
        #       required: False
        #   - id:
        #       type: int
        #       args number : 1 or more
        #       required: False

        from utils.format import format_output
        if args.type:
            from utils.type import check_type
            check_type(type=args.type)
        if args.profile:
            from utils.profile import check_profile, get_profile

            check_profile(profile=args.profile)
            profiles = get_profile(profiles=args.profile, type=args.type, id=args.id)
        else:
            from utils.profile import get_all_profiles
            profiles = get_all_profiles()
        return format_output(profiles)

    if 'add' == args.action:
        # add profile arguments :
        #   - profile:
        #       type: str
        #       args number : 1
        #       required: True
        #   - desc:
        #       type: str
        #       args number : 1
        #       required: True

        from utils.profile import add_profile
        return add_profile(name=args.profile, desc=args.desc)

    if 'update' == args.action:
        # update profile arguments :
        #   - profile:
        #       type: str
        #       args number : 1
        #       required: True
        #   - desc:
        #       type: str
        #       args number : 1
        #       required: False
        #   - newname:
        #       type: str
        #       args number : 1
        #       required: False

        from utils.profile import check_profile, update_self_profile

        check_profile(profile=args.profile)
        return update_self_profile(name=args.profile, desc=args.desc, newname=args.name)

    if 'remove' == args.action:
        # remove profile arguments :
        #   - profile:
        #       type: str
        #       args number : 1
        #       required: True

        from utils.profile import check_profile, remove_profile
        check_profile(profile=args.profile)
        return remove_profile(name=args.profile)
    return


def hostsActionsHandler(args):
    """ Check host action and execute associates functions.
        :param args: Host action
        :return: Return result from the executed functions.
    """
    if 'get' == args.action:
        # get hosts arguments :
        #   - account: type: str, args number : 1 or more, required: False
        #   - status: type: str, choice['configured, unconfigured], args number : 1, required: False
        #   - name: type: str, args number : 1 or more, required: False
        #   - id: type: int, args number : 1 or more, required: False
        #   - plateform: type: str, args number : 1 or more, required: False
        #   - env: type: str, args number : 1 or more, required: False
        #   - ip: type: str, args number : 1 or more, required: False
        #   - distribution: type: str, args number : 1 or more, required: False
        #   - kernel: type: str, args number : 1 or more, required: False

        from utils.host import get_host
        from utils.format import format_output
        return format_output(
            get_host(account=args.account, status=args.status, name=args.name, plateform=args.plateform,
                     environment=args.env, ip=args.ip, distribution=args.distribution,
                     kernel_version=args.kernel_version, id=args.id))
    if 'add' == args.action:
        # add hosts arguments :
        #   - name: type: str, args number : 1, required: True
        #   - plateform: type: str, args number : 1, required: True
        #   - environment: type str, args number: 1, required True
        #   - desc: type: str, args number : 1, required: True
        #   - ip: type: str, args number : 1, required: True
        #   - account: type: str, args number : 1, required: False
        #   - distribution: type: str, args number : 1, required: False
        #   - kernel: type: str, args number : 1, required: False

        from utils.plateform import check_plateform, update_plateform
        check_plateform(plateform=args.plateform)

        from utils.host import add_host, check_host
        check_host(plateform=args.plateform, name=args.name, environment=args.env, check_exist=True)
        updated_plateform = add_host(name=args.name, plateform=args.plateform, desc=args.desc, ip=args.ip,
                                     account=args.account, distrib=args.distribution, environment=args.env,
                                     kernel_version=args.kernel_version)
        return update_plateform(updated_plateform)

    if 'update' == args.action:
        # update hosts arguments :
        #   - name: type: str, args number : 1, required: True
        #   - plateform: type: str, args number : 1, required: True
        #   - desc: type: str, args number : 1, required: False
        #   - ip: type: str, args number : 1, required: False
        #   - account: type: str, args number : 1, required: False
        #   - newname: type: str, args number : 1, required: False

        from utils.plateform import check_plateform, update_plateform
        check_plateform(plateform=args.plateform)

        from utils.host import update_host, check_host
        check_host(plateform=args.plateform, name=args.name, environment=args.env)
        if args.newname:  # if newname, check if host already exist
            check_host(plateform=args.plateform, name=args.newname, environment=args.env, check_exist=True)

        updated_plateform = update_host(name=args.name, desc=args.desc, newname=args.newname, ip=args.ip,
                                        environment=args.env, account=args.account, plateform=args.plateform)
        return update_plateform(updated_plateform)

    if 'move' == args.action:
        # move host arguments :
        #   - plateform:
        #       type: str
        #       args number : 1
        #       required: True
        #   - env:
        #       type: str
        #       args number : 1
        #       required: True
        #   - name:
        #       type: str
        #       args number : 1
        #       required: True
        #   - newplateform:
        #       type: str
        #       args number : 1
        #       required: True
        #   - newenv:
        #       type: str
        #       args number : 1
        #       required: True

        from utils.plateform import check_plateform, update_plateform

        check_plateform(args.plateform)
        check_plateform(args.newplateform)

        from utils.host import check_host, move_host

        check_host(plateform=args.plateform, name=args.name, environment=args.env)
        check_host(plateform=args.newplateform, name=args.name, environment=args.newenv, check_exist=True)

        updated_oldplateform, updated_newplateform = move_host(oldplateform=args.plateform, environment=args.env,
                                                               name=args.name, newplateform=args.newplateform,
                                                               newenvironment=args.newenv)
        update_plateform(updated_oldplateform)

        return update_plateform(updated_newplateform)

    if 'remove' == args.action:
        # remove host arguments :
        #   - plateform:
        #       type: str
        #       args number : 1
        #       required: True
        #   - name:
        #       type: str
        #       args number : 1
        #       required: False
        #   - env:
        #       type: str
        #       args number : 1
        #       required: True
        #   - all

        from core.exceptions import HostArgumentsError
        from utils.plateform import check_plateform, update_plateform
        from utils.host import remove_host

        try:
            if args.name:
                if args.all:
                    raise HostArgumentsError("--all option doesn't need an name (all hosts will be deleted)")
                else:
                    check_plateform(plateform=args.plateform)

                    from utils.host import check_host
                    check_host(plateform=args.plateform, name=args.name, environment=args.env)
                    updated_plateform = remove_host(name=args.name, plateform=args.plateform, environment=args.env)

                    return update_plateform(updated_plateform)
            else:
                if args.all:
                    check_plateform(plateform=args.plateform)
                    updated_plateform = remove_host(name=[-1], plateform=args.plateform, environment=args.env)
                    return update_plateform(updated_plateform)
                else:
                    raise HostArgumentsError("For removing one host, name must be set !")
        except HostArgumentsError as hae:
            print hae
            exit(hae.code)


def plateformsActionsHandler(args):
    """ Check plateform action and execute associates functions.

        :param args: Plateform action
        :return: Return result from the executed functions.
    """
    if 'get' == args.action:
        # get plateform arguments :
        #   - plateform:
        #       type: str
        #       args number : 1 or more
        #       required: False
        #   - env:
        #       type: str
        #       args number : 1 or more
        #       required: False
        #   - id:
        #       type: int
        #       args number : 1 or more
        #       required: False

        from utils.format import format_output
        if not args.plateform and not args.env and not args.id:
            from utils.plateform import get_all_plateforms
            plateforms = get_all_plateforms()
        else:
            from utils.plateform import check_plateform, get_plateform

            if args.plateform:
                check_plateform(plateform=args.plateform)
            plateforms = get_plateform(plateform=args.plateform, environment=args.env, id=args.id)
        return format_output(plateforms)

    if 'add' == args.action:
        # add plateform arguments :
        #   - plateform:
        #       type: str
        #       args number : 1
        #       required: True
        #   - env:
        #       type: str
        #       args number : 1
        #       required: True
        #   - desc:
        #       type: str
        #       args number : 1
        #       required: False

        from utils.plateform import add_plateform, check_plateform_exist
        check_plateform_exist(plateform=args.plateform)
        return add_plateform(plateform=args.plateform, desc=args.desc, environment=args.env)

    if 'update' == args.action:
        # update plateform arguments :
        #   - plateform:
        #       type: str
        #       args number : 1
        #       required: True
        #   - desc:
        #       type: str
        #       args number : 1
        #       required: False
        #   - newname:
        #       type: str
        #       args number : 1
        #       required: False

        from utils.plateform import check_plateform, update_self_plateform
        check_plateform(plateform=args.plateform)
        return update_self_plateform(name=args.plateform, desc=args.desc, newname=args.newname)

    if 'remove' == args.action:
        # remove plateform arguments :
        #   - plateform:
        #       type: str
        #       args number : 1
        #       required: True

        from utils.plateform import check_plateform, remove_plateform
        check_plateform(plateform=args.plateform)
        remove_plateform(name=args.plateform)


def auditActionsHandler(args):
    if 'run' == args.action:
        # run audit arguments :
        #   - plateform:
        #       type: str
        #       args number : 1
        #       required: True
        #   - hosts:
        #       type: str
        #       args number : 1 or more
        #       required: False
        #   - environment:
        #       type: str
        #       args number : 1 or more
        #       required: False
        #   - profile:
        #       type: str
        #       args number : 1 or more
        #       required: True

        from utils.plateform import check_plateform
        from utils.profile import check_profile
        from utils.audit import run_audit, create_audit

        check_plateform(plateform=args.plateform)
        check_profile(profile=args.profile)

        if args.name:
            from utils.host import check_host
            for h in args.name:
                check_host(plateform=args.plateform, name=[h], environment=args.env)

        audits, plateform = create_audit(plateform=args.plateform, environment=args.env, profile=args.profile,
                                         hosts=args.name)

        return run_audit(audits=audits, plateform=plateform)


def initialize_args():
    """ Initialize all subparsers, and create a main parser for arguments passed to Heimdall.
    :return: Main parser
    :rtype: argparse object
    """
    parser = argparse.ArgumentParser(prog='Heimdall',
                                     description="""Heimdall script, for auditing remote CentOS servers.""")
    subparsers = parser.add_subparsers()
    add_group = subparsers.add_parser('add')
    link_group = subparsers.add_parser('link')
    move_group = subparsers.add_parser('move')
    unlink_group = subparsers.add_parser('unlink')
    update_group = subparsers.add_parser('update')
    get_group = subparsers.add_parser('get')
    remove_group = subparsers.add_parser('remove')
    audit_group = subparsers.add_parser('audit')

    # ADD GROUP
    subparsers = add_group.add_subparsers()

    rule_add = subparsers.add_parser('rule')
    rule_add.add_argument('--type', nargs=1, type=str, dest='type', required=True, help='Type where rule is defined')
    rule_add.add_argument('--desc', nargs=1, type=str, dest='desc', required=True, help='Description of the rule')
    rule_add.add_argument('--auditcmd', nargs='+', type=str, dest='audit_cmd', help='Command(s) to run during audit')
    rule_add.add_argument('--remedcmd', nargs='+', type=str, dest='remed_cmd',
                          help='Command(s) to execute for fixing failed audit')
    rule_add.add_argument('--auditscript', nargs=1, type=str, dest='audit_script',
                          help='Script name to run during audit')
    rule_add.add_argument('--remedscript', nargs=1, type=str, dest='remed_script',
                          help='Script name to execute for fixing failed audit')
    rule_add.set_defaults(action='add', func=rulesActionsHandler)

    type_add = subparsers.add_parser('type')
    type_add.add_argument('--type', nargs=1, type=str, dest='type', required=True,
                          help='Type name where rules are defined')
    type_add.add_argument('--desc', nargs=1, type=str, dest='desc', required=True, help='Type description')
    type_add.set_defaults(action='add', func=typesActionsHandler)

    profile_add = subparsers.add_parser('profile')
    profile_add.add_argument('--profile', nargs=1, type=str, dest='profile', required=True, help='Profile name')
    profile_add.add_argument('--desc', nargs=1, type=str, dest='desc', required=True, help='Profile description')
    profile_add.set_defaults(action='add', func=profilesActionsHandler)

    plateform_add = subparsers.add_parser('plateform')
    plateform_add.add_argument('--plateform', nargs=1, type=str, dest='plateform', required=True,
                               help='Plateform name where host are defined')
    plateform_add.add_argument('--desc', nargs=1, type=str, dest='desc', required=True, help='Plateform description')
    plateform_add.add_argument('--env', nargs='+', type=str, dest='env', required=True, help='Plateform environment')
    plateform_add.set_defaults(action='add', func=plateformsActionsHandler)

    host_add = subparsers.add_parser('host')
    host_add.add_argument('--name', nargs=1, type=str, dest='name', required=True, help='Host name')
    host_add.add_argument('--plateform', nargs=1, type=str, dest='plateform', required=True,
                          help='Plateform name where host is defined ')
    host_add.add_argument('--env', nargs=1, type=str, dest='env', required=True,
                          help='Environment name where host is defined ')
    host_add.add_argument('--desc', nargs=1, type=str, dest='desc', required=True, help='Host description')
    host_add.add_argument('--ip', nargs=1, type=str, dest='ip', required=True, help='Host ip address')
    host_add.add_argument('--account', nargs=1, type=str, dest='account',
                          help='Super user account for configuring host')
    host_add.add_argument('--distribution', nargs=1, type=str, dest='distribution', help='Host linux distribution')
    host_add.add_argument('--kernel', nargs=1, type=str, dest='kernel_version', help='Host kernel version')
    host_add.set_defaults(action='add', func=hostsActionsHandler)

    script_add = subparsers.add_parser('script')
    script_add.add_argument('--type', nargs=1, type=str, dest='type', choices=['audit', 'remediation'], required=True,
                            help='Script type (audit or remediation)')
    script_add.add_argument('--path', nargs=1, type=str, dest='path', required=True, help='Path to the script')
    script_add.add_argument('--name', nargs=1, type=str, dest='name', required=True, help='Script name')
    script_add.set_defaults(action='add', func=scriptsActionsHandler)

    # LINK GROUP
    subparsers = link_group.add_subparsers()

    rule_link = subparsers.add_parser('rule')
    rule_link.add_argument('--profile', nargs='+', type=str, dest='profile', required=True,
                           help='Profile name where rule will be linked')
    rule_link.add_argument('--type', nargs=1, type=str, dest='type', required=True,
                           help='Type name where rule is defined')
    rule_link.add_argument('--id', nargs='+', type=int, dest='id', help='Rule id')
    rule_link.add_argument('--all', action='store_true', dest='all',
                           help='Link all rules from one type (cannot be set if id is present)')
    rule_link.set_defaults(action='link', func=rulesActionsHandler)

    # UNLINK GROUP
    subparsers = unlink_group.add_subparsers()

    rule_unlink = subparsers.add_parser('rule')
    rule_unlink.add_argument('--profile', nargs='+', type=str, dest='profile', required=True,
                             help='Profile name where rule will be unlinked')
    rule_unlink.add_argument('--type', nargs=1, type=str, dest='type', help='Type name where rule is defined')
    rule_unlink.add_argument('--id', nargs='+', type=int, dest='id', help='Rule id')
    rule_unlink.add_argument('--all', action='store_true', dest='all',
                             help='Unlink all rules from one type (cannot be set if id is present)')
    rule_unlink.set_defaults(action='unlink', func=rulesActionsHandler)

    # MOVE GROUP
    subparsers = move_group.add_subparsers()

    host_move = subparsers.add_parser('host')
    host_move.add_argument('--plateform', nargs=1, type=str, dest='plateform', required=True,
                           help='Plateform name where hosts are defined')
    host_move.add_argument('--env', nargs=1, type=str, dest='env', required=True,
                           help='Environment name where host is defined ')
    host_move.add_argument('--name', nargs=1, type=str, dest='name', required=True, help='Host name')
    host_move.add_argument('--newplateform', nargs=1, type=str, dest='newplateform', required=True,
                           help='Plateform name where host will be defined')
    host_move.add_argument('--newenv', nargs=1, type=str, dest='newenv', required=True,
                           help='Environment name where host will be defined ')
    host_move.set_defaults(action='move', func=hostsActionsHandler)

    rule_move = subparsers.add_parser('rule')
    rule_move.add_argument('--type', nargs=1, type=str, dest='type', required=True,
                           help='Type name where rule is defined')
    rule_move.add_argument('--id', nargs=1, type=int, dest='id', required=True, help='Rule id')
    rule_move.add_argument('--newtype', nargs=1, type=str, dest='newtype', required=True,
                           help='Type name where rule will be defined')
    rule_move.set_defaults(action='move', func=rulesActionsHandler)

    # UPDATE GROUP
    subparsers = update_group.add_subparsers()
    rule_update = subparsers.add_parser('rule')
    rule_update.add_argument('--type', nargs=1, type=str, dest='type', required=True,
                             help='Type name where rule is defined')
    rule_update.add_argument('--id', nargs=1, type=int, dest='id', required=True, help='Rule id')
    rule_update.add_argument('--desc', nargs=1, type=str, dest='desc', help='Rule description')
    rule_update.add_argument('--auditcmd', nargs='+', type=str, dest='audit_cmd',
                             help='Command(s) to run during audit')
    rule_update.add_argument('--remedcmd', nargs='+', type=str, dest='remed_cmd',
                             help='Command(s) to execute for fixing failed audit')
    rule_update.add_argument('--auditscript', nargs=1, type=str, dest='audit_script',
                             help='Script name to run during audit')
    rule_update.add_argument('--remedscript', nargs=1, type=str, dest='remed_script',
                             help='Script name to execute for fixing failed audit')
    rule_update.set_defaults(action='update', func=rulesActionsHandler)

    type_update = subparsers.add_parser('type')
    type_update.add_argument('--type', nargs=1, type=str, dest='type', required=True,
                             help='Type name where rules are defined')
    type_update.add_argument('--desc', nargs=1, type=str, dest='desc', help='Type description')
    type_update.add_argument('--newname', nargs=1, type=str, dest='newname', help='Type new name')
    type_update.set_defaults(action='update', func=typesActionsHandler)

    profile_update = subparsers.add_parser('profile')
    profile_update.add_argument('--profile', nargs=1, type=str, dest='profile', required=True, help='Profile name')
    profile_update.add_argument('--desc', nargs=1, type=str, dest='desc', help='Profile description')
    profile_update.add_argument('--newname', nargs=1, type=str, dest='name', help='Profile new name')
    profile_update.set_defaults(action='update', func=profilesActionsHandler)

    plateform_update = subparsers.add_parser('plateform')
    plateform_update.add_argument('--plateform', nargs=1, type=str, dest='plateform', required=True,
                                  help='Plateform name')
    plateform_update.add_argument('--desc', nargs=1, type=str, dest='desc', help='Plateform description')
    plateform_update.add_argument('--newname', nargs=1, type=str, dest='newname', help='Plateform new name')
    plateform_update.set_defaults(action='update', func=plateformsActionsHandler)

    host_update = subparsers.add_parser('host')
    host_update.add_argument('--name', nargs=1, type=str, dest='name', required=True, help='Host name')
    host_update.add_argument('--plateform', nargs=1, type=str, dest='plateform', required=True,
                             help='Plateform name where host is defined')
    host_update.add_argument('--env', nargs=1, type=str, dest='env', required=True,
                             help='Environment name where host is defined ')
    host_update.add_argument('--desc', nargs=1, type=str, dest='desc', help='Host description')
    host_update.add_argument('--ip', nargs=1, type=str, dest='ip', help='Host ip address')
    host_update.add_argument('--account', nargs=1, type=str, dest='account',
                             help='Super user account used to configure host')
    host_update.add_argument('--newname', nargs=1, type=str, dest='newname')
    host_update.set_defaults(action='update', func=hostsActionsHandler)

    # GET GROUP
    subparsers = get_group.add_subparsers()

    rule_get = subparsers.add_parser('rule')
    rule_get.add_argument('--id', nargs='+', type=int, dest='id', help='Rule id')
    rule_get.add_argument('--type', nargs='+', type=str, dest='type', help='Type name where rule is defined')
    rule_get.set_defaults(action='get', func=rulesActionsHandler)

    type_get = subparsers.add_parser('type')
    type_get.add_argument('--type', nargs='+', type=str, dest='type', help='Type name')
    type_get.set_defaults(action='get', func=typesActionsHandler)

    profile_get = subparsers.add_parser('profile')
    profile_get.add_argument('--profile', nargs='+', type=str, dest='profile', help='Profile name')
    profile_get.add_argument('--type', nargs='+', type=str, dest='type', help='Profile\'s type name')
    profile_get.add_argument('--id', nargs='+', type=int, dest='id', help='Profile id')
    profile_get.set_defaults(action='get', func=profilesActionsHandler)

    plateform_get = subparsers.add_parser('plateform')
    plateform_get.add_argument('--plateform', nargs='+', type=str, dest='plateform', help='Plateform name')
    plateform_get.add_argument('--env', nargs='+', type=str, dest='env', help='Plateform environment')
    plateform_get.add_argument('--id', nargs='+', type=int, dest='id', help='Plateform id')
    plateform_get.set_defaults(action='get', func=plateformsActionsHandler)

    host_get = subparsers.add_parser('host')
    host_get.add_argument('--account', nargs='+', type=str, dest='account',
                          help='Super user account for configuring host')
    host_get.add_argument('--status', type=str, nargs=1, choices=['configured', 'unconfigured'], dest='status',
                          help='Host configuration status')
    host_get.add_argument('--name', nargs='+', type=str, dest='name', help='Host name')
    host_get.add_argument('--id', nargs='+', type=int, dest='id', help='Host id')
    host_get.add_argument('--plateform', nargs='+', type=str, dest='plateform',
                          help='Plateform name where host is defined')
    host_get.add_argument('--env', nargs='+', type=str, dest='env', help='Host environment')
    host_get.add_argument('--ip', nargs='+', type=str, dest='ip', help='Host ip address')
    host_get.add_argument('--distribution', nargs='+', type=str, dest='distribution', help='Host distribution')
    host_get.add_argument('--kernel', nargs='+', type=float, dest='kernel_version', help='Host kernel version')
    host_get.set_defaults(action='get', func=hostsActionsHandler)

    script_get = subparsers.add_parser('script')
    script_get.add_argument('--type', nargs=1, type=str, dest='type', choices=['audit', 'remediation'],
                            help='Script type (audit or remediation')
    script_get.set_defaults(action='get', func=scriptsActionsHandler)

    # REMOVE GROUP
    subparsers = remove_group.add_subparsers()

    rule_remove = subparsers.add_parser('rule')
    rule_remove.add_argument('--id', nargs=1, type=int, dest='id', help='Rule id')
    rule_remove.add_argument('--type', nargs=1, type=str, dest='type', required=True,
                             help='Type name where rule is defined')
    rule_remove.add_argument('--all', action='store_true', dest='all',
                             help='Remove all rules from one type if is set')
    rule_remove.set_defaults(action='remove', func=rulesActionsHandler)

    type_remove = subparsers.add_parser('type')
    type_remove.add_argument('--type', nargs=1, type=str, dest='type', required=True, help='Type name')
    type_remove.set_defaults(action='remove', func=typesActionsHandler)

    profile_remove = subparsers.add_parser('profile')
    profile_remove.add_argument('--profile', nargs=1, type=str, dest='profile', required=True, help='Profile name')
    profile_remove.set_defaults(action='remove', func=profilesActionsHandler)

    plateform_remove = subparsers.add_parser('plateform')
    plateform_remove.add_argument('--plateform', nargs='+', type=str, dest='plateform', required=True,
                                  help='Plateform name')
    plateform_remove.set_defaults(action='remove', func=plateformsActionsHandler)

    host_remove = subparsers.add_parser('host')
    host_remove.add_argument('--plateform', nargs=1, type=str, dest='plateform', required=True,
                             help='Plateform name where host is defined')
    host_remove.add_argument('--env', nargs=1, type=str, dest='env', required=True,
                             help='Environment name where host is defined ')
    host_remove.add_argument('--name', nargs='+', type=str, dest='name', help='Host name')
    host_remove.add_argument('--all', action='store_true', dest='all', help='Remove all host if is set')
    host_remove.set_defaults(action='remove', func=hostsActionsHandler)

    script_remove = subparsers.add_parser('script')
    script_remove.add_argument('--type', nargs=1, type=str, dest='type', choices=['audit', 'remediation'],
                               required=True, help='Script type')
    script_remove.add_argument('--name', nargs=1, type=str, dest='name', required=True, help='Script name')
    script_remove.set_defaults(action='remove', func=scriptsActionsHandler)

    # AUDIT GROUP
    subparsers = audit_group.add_subparsers()

    run_audit = subparsers.add_parser('run')
    run_audit.add_argument('--plateform', nargs=1, type=str, dest='plateform', required=True,
                           help='Plateform name where host(s) is/are defined')
    run_audit.add_argument('--env', nargs=1, type=str, dest='env', required=True,
                           help='Environment name where host is defined ')
    run_audit.add_argument('--hosts', nargs='+', type=str, dest='name', help='Host(s) name(s)')
    run_audit.add_argument('--profile', nargs='+', type=str, dest='profile', required=True, help='Profile name')
    run_audit.set_defaults(action='run', func=auditActionsHandler)

    args = parser.parse_args()
    args.func(args)
    return parser
