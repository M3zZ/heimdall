# -*- coding: utf-8 -*-
from fabric.tasks import execute

from core import commands as cmd
from core.exceptions import FabricCommandError


def run_audit(audits=None, plateform=None):
    """ Take one or more Audit Objects and execute all functions used during and Audit.

        :param: audits: Audit Objects created that contains all information needed.
        :type: audits: list of Audit Objects
        :return: True if succeed
        :rtype: bool
    """
    from utils.plateform import update_plateform
    for audit in audits:
        import time
        start_time = time.time()
        audit.generate_scripts()
        print_step('Auditing %s with profile %s' % (audit.host.name, audit.profile.name))
        print_step('Initiate SSH Session on %s (%s@%s)\n' % (audit.host.name, audit.host.account, audit.host.ip))

        audit.host = configure_host(audit.host, audit.config_script_path)
        update_plateform(plateform)  # Updating yml file with new account and status values

        remove_generated_scripts(audit.config_script_path)

        if not audit.host.distribution:
            audit.host = get_distribution_info(audit.host)

        if not audit.host.kernel_version:
            audit.host = get_kernel_info(audit.host)
        update_plateform(plateform)

        host = deploy_audit_script(audit.host, audit.audit_script_path)

        if host:  # if host need to be reconfigured, update account and status and exit
            audit.host = host
            update_plateform(plateform)
            exit(1)

        if audit.scripts_needed:
            deploy_script_needed(audit.host, audit.scripts_needed)

        execute_audit_script(audit.host, audit.audit_script_path)
        remove_generated_scripts(audit.audit_script_path)
        update_plateform(plateform)

        get_results(audit.host, audit.pickle_name)

        remove_script_needed(audit.host)
        from core.report import Report
        audit.report = Report(data=load_report(audit.pickle_name))
        print_step('Generating html report from audit results\n')
        audit.generate_report()
        print_step('HTML report successfully generated -> %s\n' % audit.report_path)
        print_step('Auditing %s with profile %s successfully finished in %d seconds\n' % (
            audit.host.name, audit.profile.name, int(time.time() - start_time)))
    return True


def load_report(picklename):
    """ Open pickle file, and load all data in it.

        :param: picklename: pickle file's name generated during audit.
        :type: picklename: str
        :return: data from pickle file
        :rtype: dict

        ..seealso:: remove_generated_scripts()
    """
    print_step("Loading data from pickle file")

    from pickle import load
    from reports import __reportdir__
    path = __reportdir__ + '/' + picklename
    result = load(open(path, 'rb'))
    print_step("Data successfully loaded\n")
    if result:
        print_step("Removing pickle file")
        remove_generated_scripts(script_path=path)
        return result
    else:
        return None


def remove_generated_scripts(script_path):
    """ Delete temporary file passed in parameter, generated during audit.

        :param: script_path: path to generated script.
        :type: script_path: str
        :return: True if succeed
        :rtype: bool

        ..seealso:: heimdall.core.commands.remove_local_script()
    """
    print_step('Deleting generated script on local server')
    try:
        if execute(cmd.remove_local_script, script_path).get('<local-only>'):
            raise FabricCommandError("Error during fabric execution", cmd.remove_local_script.__name__)
        return True
    except FabricCommandError as ffe:
        print ffe
        exit(ffe.code)


def deploy_audit_script(host, script_path):
    """ take Host Object and path to script to deploy, then execute fabric command for deployment.

        :param: host: Host Object currently audited
        :param: script_path: script to deploy
        :type: host: Host Object
        :type: script_path: str
        :return: Modified host, if command result equal 255 retur0 otherwise.
        :rtype: Host object or 0

        ..seealso:: heimdall.core.commands.calculate_md5(), heimdall.core.deploy_audit_script()
    """
    h = '%s@%s' % (host.account, host.ip)
    try:
        result = execute(cmd.deploy_audit_script, script_path, host=h).get(h)
        if result == 255:  # Server need to be reconfigured
            print_step('%s need to be reconfigured' % host.name)
            new_account = raw_input('[*] - Sudo account for reconfiguration : ')
            host.account = new_account
            host.status = 'unconfigured'
            print_step('account and status changed, run audit again for reconfiguration')
            return host
        if execute(cmd.deploy_audit_script, script_path, host=h).get(h):
            raise FabricCommandError("Error during %s deploy" % script_path, cmd.deploy_audit_script.__name__)
        return 0
    except FabricCommandError as ffe:
        print ffe
        exit(ffe.code)


def execute_audit_script(host, script_path):
    """ take Host Object and md5sum of local generated script and return result of fabric command executed.

        :param: host: Host Object currently audited
        :param: md5local: md5sum of audit script
        :type: host: Host Object
        :type: md5local: str
        :return: result of fabric command
        :rtype: int

        ..seealso:: heimdall.core.commands.execute_audit_script()
    """
    h = '%s@%s' % (host.account, host.ip)
    try:
        md5local = execute(cmd.calculate_md5, script_path).get('<local-only>')
        if not md5local:
            raise FabricCommandError("Can't calculate md5 for %s" % script_path, cmd.calculate_md5.__name__)
        result = execute(cmd.execute_audit_script, md5local, host=h).get(h)
        if result:
            raise FabricCommandError("Error during audit script execution.", cmd.execute_audit_script.__name__)
        # update last audit
        from datetime import datetime
        host.last_audit = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        return result
    except FabricCommandError as ffe:
        print ffe
        exit(ffe.code)


def get_results(host, picklename):
    """ take Host Object and pickle file's name and return result of fabric command executed.

        :param: host: Host Object currently audited
        :param: picklename: pickle file's name
        :type: host: Host Object
        :type: picklename: str
        :return: result of fabric command
        :rtype: int

        ..seealso:: heimdall.core.commands.get_results()
    """
    h = '%s@%s' % (host.account, host.ip)
    result = execute(cmd.get_results, picklename, host=h).get(h)
    try:
        if result:
            raise FabricCommandError("Error during result download.", cmd.get_results.__name__)
    except FabricCommandError as ffe:
        print ffe
        exit(ffe.code)
    return result


def deploy_script_needed(host, scripts):
    """ take Host Object and list of scripts needed for audit, then return result of fabric command executed.

        :param: host: Host Object currently audited.
        :param: scripts: list of scripts needed.
        :type: host: Host Object
        :type: picklename: str
        :return: result of fabric command
        :rtype: int

        ..seealso:: heimdall.core.commands.deploy_script_needed()
    """
    h = '%s@%s' % (host.account, host.ip)
    result = execute(cmd.deploy_script_needed, scripts, host=h).get(h)
    try:
        if result:
            raise FabricCommandError("Error during audit scripts upload.", cmd.deploy_script_needed.__name__)
        return result
    except FabricCommandError as ffe:
        print ffe
        exit(ffe.code)


def remove_script_needed(host):
    """ take Host Object and list of scripts needed for audit, then return result of fabric command executed.

        :param: host: Host Object currently audited.
        :param: scripts: list of scripts needed.
        :type: host: Host Object
        :type: picklename: str
        :return: result of fabric command
        :rtype: int

        ..seealso:: heimdall.core.commands.remove_script_needed()
    """
    h = '%s@%s' % (host.account, host.ip)
    result = execute(cmd.remove_script_needed, host.account, host=h).get(h)
    try:
        if result:
            raise FabricCommandError("Error during audit scripts removal.", cmd.deploy_script_needed.__name__)
        return result
    except FabricCommandError as ffe:
        print ffe
        exit(ffe.code)


def get_distribution_info(host):
    """ take Host Object, then return result of fabric command executed.

        :param: host: Host Object currently audited.
        :type: host: Host Object
        :return: Modified host.
        :rtype: Host object

        ..seealso:: heimdall.core.commands.get_server_distrib()
    """
    print_step('Updating distribution info')
    h = '%s@%s' % (host.account, host.ip)
    result = execute(cmd.get_server_distrib, host=h).get(h)
    if result:
        host.distribution = str(result)
    else:
        host.distribution = ''
    return host


def get_kernel_info(host):
    """ take Host Object, then return result of fabric command executed.

        :param: host: Host Object currently audited.
        :type: host: Host Object
        :return: Modified host.
        :rtype: Host object

        ..seealso:: heimdall.core.commands.get_server_kernel()
    """
    print_step("Updating kernel version")
    h = '%s@%s' % (host.account, host.ip)
    result = execute(cmd.get_server_kernel, host=h).get(h)
    if result:
        host.kernel_version = str(result)
    else:
        host.distribution = ''
    return host


def configure_host(host, config_script_path):
    """ take Host Object and path to configuration script, then return result of fabric command executed.

        :param: host: Host Object currently audited.
        :param: config_script_path: path to configuration script
        :type: host: Host Object
        :type: config_script_path: str
        :return: Modified host.
        :rtype: Host object

        ..seealso:: heimdall.core.commands.check_is_configured(), heimdall.core.commands.deploy_config_script(), heimdall.core.commands.execute_config_script(), heimdall.core.commands.remove_remote_script()
    """
    print_step('Checking host %s configuration' % host.name)
    if host.status == 'configured':
        print_step('Host %s is already configured' % host.name)
        if host.account != 'heimdall':
            host.account = 'heimdall'
    else:
        if host.account != 'root' and host.account != 'heimdall':
            print_step('Starting configuration with %s, hope this account has sudo rights...' % host.account)
        h = '%s@%s' % (host.account, host.ip)
        print_step('Host %s is not configured' % host.name)
        print_step('Checking if was manually installed..')
        # Looking for /opt/heimdall/imconfigured, maybe server was manually configured

        if not execute(cmd.check_is_configured, host.account, host=h).get(h):
            print_step('Host %s was manually configured\n' % host.name)
            host.status = 'configured'
            host.account = 'heimdall'
            return host
        # Deploying configure script to tmp
        try:
            # Check if /opt/
            if host.account == 'root':
                remote_path = '/root/'
            else:
                remote_path = '/home/%s/' % host.account
            if not execute(cmd.deploy_config_script, config_script_path, remote_path, host.account, host=h).get(
                    h):
                config_script = config_script_path.split('/')[-1]
                if not execute(cmd.execute_config_script, remote_path + config_script, host.account, host=h).get(
                        h):
                    print_step('Host %s is configured\n' % host.name)
                    host.status = 'configured'
                    host.account = 'heimdall'
                    execute(cmd.remove_remote_script, remote_path + config_script, host.account, host=h).get(h)
                    return host
                else:
                    raise FabricCommandError("Error during configuration script execution.",
                                             cmd.execute_config_script.__name__)
            else:
                raise FabricCommandError("Error during configuration script deployment.",
                                         cmd.deploy_config_script.__name__)
        except FabricCommandError as ffe:
            print ffe
            exit(ffe.code)
    return host


def create_audit(plateform=None, profile=None, hosts=None, environment=None):
    """ Create an Audit Object from data passed by user, and return a list of Audit Objects.

        :param: plateform: list of plateform audited.
        :param: profile: list of profiles used for auditing.
        :param: hosts: hosts audited
        :type: plateform: list of str
        :type: config_script_path: list of str
        :type: config_script_path: list of str
        :return: List of Audit Objects created with profile and plateform
        :rtype: list of Audit Objects

        ..seealso:: heimdall.conf.hosts.getPlateformObject(), heimdall.conf.profiles.getProfileObject(),
    """
    # generating hosts
    from conf.hosts import getPlateformObject
    from conf.profiles import getProfileObject
    from core.exceptions import EnvironmentDoesNotExist

    audits = []
    pl = getPlateformObject(plateform[0])

    if not pl.check_environment(environment[0]):
        raise EnvironmentDoesNotExist('Environment %s in plateform %s does not exists!' % (environment[0], pl.name),
                                      pl.name)

    audit_hosts = []

    # Filter all hosts choose from env and plateform
    if hosts:
        [audit_hosts.append(host) for host in pl.environment[environment[0]] for h in hosts if host.name == h]
    else:
        [audit_hosts.append(host) for host in pl.environment[environment[0]]]

    from core.audit import Audit

    for prof in profile:
        pr = getProfileObject(prof)
        for h in audit_hosts:
            audits.append(Audit(host=h, profile=pr, plateform=pl.name, environment=environment[0]))
    return audits, pl


def print_step(step=''):
    print "[*] - %s" % step
