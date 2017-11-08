# -*- coding: utf-8 -*-


from fabric.api import run, env, output, put, sudo, local, get

env.fabfile = __name__
env.colorize_errors = True
env.warn_only = True
output['everything'] = False


def check_is_configured(account):
    env.user = account
    env.abort_on_prompts = False
    if env.user == 'heimdall':
        env.key_filename = '/opt/heimdall/.ssh/id_rsa'
    print "[*] - Looking for end configuration file on %s" % env.host
    result = run('ls /opt/heimdall/iamconfigured')
    if result.failed:
        print "[*] - End configuration file not present"
        return result.return_code
    else:
        print "[*] - Found what i was looking for"
    return result.return_code


def deploy_config_script(localpath, remotepath, account):
    env.user = account

    print "[*] - Deploying configuration script on %s " % env.host
    result = put(local_path=localpath, remote_path=remotepath, mode=700)
    if result.failed:
        print "ERROR during %s upload" % result.failed
        return 1
    else:
        print "[*] - Script successfully deployed on %s\n" % env.host
    return 0


def execute_config_script(remotepath, account):
    env.user = account
    print "[*] - Executing configuration script with %s on %s " % (account, env.host)
    if account != 'root':
        print "[*] - Trying execution as superuser ..."
        result = sudo('%s' % remotepath)
        if result.return_code != 0:
            result = run("sudo su - -c '%s'" % remotepath)  # if admin can only do sudo su -
            if result.return_code != 0:
                print "ERROR during config script execution :\n%s" % result
                return result.return_code
            else:
                print "[*] - Host in now configured on %s\n" % env.host
                return result.return_code
        else:
            print "[*] - Host in now configured on %s\n" % env.host
            return result.return_code
    else:
        print "[*] - Trying execution as root ..."
        result = run('/bin/bash %s' % remotepath)
        if result.return_code != 0:
            print "Execution failed for %s:" % remotepath
            print "Error :\n", result
            print "Host %s isn't configured" % env.host
            print "Execute sudo /bin/bash %s manually (with a superuser)" % remotepath
            return result.return_code
        else:
            print "[*] - Host in now configured on %s\n" % env.host
            return result.return_code


def deploy_audit_script(script_path):
    env.key_filename = '/opt/heimdall/.ssh/id_rsa'
    env.user = 'heimdall'
    print "[*] - Deploying audit script on %s" % env.host
    env.abort_on_prompts = True
    try:
        result = run('ls -d /opt/heimdall/audit')
    except SystemExit:
        print '[*] - PASSWORD ASKED during connection to %s (seems pubkey is not valid anymore)!' % env.host
        return 255
    if result.return_code == 0:
        result = put(local_path=script_path, remote_path='/opt/heimdall/audit/heimdall_audit.py', mode=600)
        if result.failed:
            print "ERROR during upload: %s" % result.failed
            return 1
        else:
            print "[*] - Audit script successfully deployed on %s" % env.host
            print "[*] - Adjusting rights on audit script"
            result = run('chmod 600 /opt/heimdall/audit/heimdall_audit.py')
            if result.return_code != 0:
                print "ERROR can't adjust rights on audit script: %s" % result.failed
                return 1
            else:
                print "[*] - Rights are now correct on audit script\n"
                return 0
    else:
        print "ERROR /opt/heimdall/audit doesnt exist on %s" % env.host
        return 1


def execute_audit_script(md5local):
    env.key_filename = '/opt/heimdall/.ssh/id_rsa'
    env.user = 'heimdall'
    print "[*] - Checking integrity of audit script"
    result = run("md5sum /opt/heimdall/audit/heimdall_audit.py |awk '{print $1}'")
    if result.return_code != 0:
        print result
        print "ERROR can't read md5sum of remote audit script"
        return 1
    else:
        if result == md5local:
            print "[*] - Integrity is correct"
            print "[*] - Executing audit script on %s " % env.host
            result = sudo("/usr/bin/env python /opt/heimdall/audit/heimdall_audit.py")
            if result.return_code != 0:
                print "ERROR during audit script execution :\n%s" % result
                return 1
            else:
                print "[*] - Audit script execution finished on %s\n" % env.host
                return 0
        else:
            print "[*] - Integrity is incorrect! Exiting"
            return 1


def get_results(picklename):
    env.key_filename = '/opt/heimdall/.ssh/id_rsa'
    env.user = 'heimdall'
    print "[*] - Downloading audit results from %s" % env.host
    from reports import __reportdir__
    remotepickle = '/opt/heimdall/audit/%s' % picklename
    result = get(remote_path=remotepickle, local_path=__reportdir__)
    if result.failed:
        print "ERROR can't download %s" % result.failed
        return 1
    else:
        print "[*] - Audit results successfully downloaded from %s\n" % env.host
        print "[*] - Deleting generated picklefile on %s" % env.host
        result = run('/bin/rm -f %s' % remotepickle)
        if result.failed:
            print "ERROR can't delete %s : %s" % (remotepickle, result.failed)
            return 1
        else:
            print "[*] - Generated pickle file successfully removed on %s\n" % env.host
            return 0


def remove_remote_script(remotepath, account):
    env.user = account
    print "[*] - Removing configuration script on %s " % env.host
    if account != 'root':
        print "[*] - Trying remove as superuser ..."
        result = run("sudo su - -c '/bin/rm -f %s'" % remotepath)
        if result.return_code != 0:
            print result
            print "Not enough rights for removing %s\n" % remotepath
            return result.return_code
    else:
        print "[*] - Trying remove as root ..."
        result = run('/bin/rm -f %s' % remotepath)
        if result.return_code != 0:
            print "Removing failed for %s:" % remotepath
            print "Error :\n", result
            print "Try remove it manually"
            return result.return_code
        else:
            print "[*] - Script removed successfully on %s\n" % env.host
    return result.return_code


def remove_script_needed(account):
    env.user = account
    scriptspath = '/opt/heimdall/scripts'
    print "[*] - Removing uploaded scripts on %s " % env.host
    result = run("/bin/rm -f %s/*.sh" % scriptspath)
    if result.return_code != 0:
        print result
        print "Not enough rights for removing %s\n" % scriptspath
    else:
        print "[*] - Scripts removed successfully on %s\n" % env.host
    return result.return_code


def get_server_distrib():
    env.key_filename = '/opt/heimdall/.ssh/id_rsa'
    env.user = 'heimdall'
    print "[*] - Getting distribution info on %s" % env.host
    # maybe its a centos server
    result = run(
        "if [ -f /etc/centos-release ];then export rel=$(egrep -o '[0-9.]+' /etc/centos-release) && echo \"CentOS \"$rel;else exit 255;fi")
    if result.return_code == 255:
        # try something else, maybe os release
        result = run(
            "if [ -f /etc/os-release];then awk -F'=' '/^NAME=|^VERSION=/ {split($2, a, \"\"\");{printf \"%s\", a[2]}}' /etc/os-release;else exit 255;fi")
        if result.return_code == 255:
            # try again, last attempt
            result = run("awk 'NR==1{print $1 $2 $3}' /etc/issue")
            if result.return_code != 0:
                print "Error :\n", result
                return ''
            else:
                return result
        elif result.return_code == 0:
            return result
        else:
            print "Error :\n", result
            return ''
    elif result.return_code == 0:
        return result
    else:
        print "Error :\n", result
        return ''


def get_server_kernel():
    env.user = 'heimdall'
    env.key_filename = '/opt/heimdall/.ssh/id_rsa'
    print "[*] - Getting kernel info on %s" % env.host
    result = run("awk '{print $3}' /proc/version")
    if result.return_code != 0:
        print "Error :\n", result
        return ''
    else:
        return result


def remove_local_script(script_path):
    print "[*] - Deleting %s" % script_path
    result = local('rm -f %s' % script_path)
    if result.return_code != 0:
        print "ERROR can't remove %s" % script_path
        print result
        return 1
    else:
        print "[*] - %s successfully deleted\n" % script_path
        return 0


def deploy_script_needed(scripts):
    env.key_filename = '/opt/heimdall/.ssh/id_rsa'
    env.user = 'heimdall'
    print "[*] - Deploying scripts needed on %s" % env.host
    result = run('ls -d /opt/heimdall/scripts')
    if result.return_code == 0:
        for s in scripts:
            result = put(local_path=s, remote_path='/opt/heimdall/scripts/', mode=700)
            if result.failed:
                print "ERROR during %s upload: %s" % (s, result.failed)
                return 1
        print "[*] - Adjusting rights on needed audit scripts"
        result = run('chmod 300 /opt/heimdall/scripts/*.sh')
        if result.failed:
            print "ERROR can't adjust rights on needed audit scripts: %s" % result.failed
            return 1
        print "[*] - Scripts needed successfully deployed on %s\n" % env.host
        return 0
    else:
        print "ERROR /opt/heimdall/scripts doesnt exist on %s " % env.host
        return 1


def calculate_md5(script_path):
    print "[*] - Calculating md5sum of %s" % script_path
    result = local("md5sum %s|awk '{print $1}'" % script_path, capture=True)
    if result.return_code != 0:
        print "ERROR can't calculate md5 of %s" % script_path
        print result
        return ''
    else:
        print "[*] - md5 calculated for %s\n" % script_path
        return result
