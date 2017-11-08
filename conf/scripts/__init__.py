# -*- coding: utf-8 -*-
from os import path, listdir

__sdir__ = path.dirname(__file__)
__auditdir__ = path.join(__sdir__, 'audit')
__remeddir__ = path.join(__sdir__, 'remediation')
__confdir__ = path.join(__sdir__, 'configuration')
__auditscriptsfile__ = [path.join(__auditdir__, af) for af in listdir(__auditdir__) if
                        (path.isfile(path.join(__auditdir__, af)) and 'sh' in path.basename(
                            path.join(__auditdir__, af)))]
__remedscriptsfile__ = [path.join(__remeddir__, rf) for rf in listdir(__remeddir__) if
                        (path.isfile(path.join(__remeddir__, rf)) and 'sh' in path.basename(
                            path.join(__remeddir__, rf)))]
