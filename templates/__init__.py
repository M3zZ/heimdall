# -*- coding: utf-8 -*-
from os import path, listdir

__tdir__ = path.dirname(__file__)

__audittemplate__ = [at for at in listdir(__tdir__) if
                     (path.isfile(path.join(__tdir__, at)) and 'audit' in path.basename(path.join(__tdir__, at)))][0]
__configtemplate__ = [at for at in listdir(__tdir__) if
                      (path.isfile(path.join(__tdir__, at)) and 'configure' in path.basename(path.join(__tdir__, at)))][
    0]
__reporttemplate__ = [at for at in listdir(__tdir__) if
                      (path.isfile(path.join(__tdir__, at)) and 'report' in path.basename(path.join(__tdir__, at)))][
    0]
__templatesfiles__ = [tf for tf in listdir(__tdir__) if
                      (path.isfile(path.join(__tdir__, tf)) and 'jinja' in path.basename(path.join(__tdir__, tf)))]
