# -*- coding: utf-8 -*-

from os import path, listdir

__reportdir__ = path.dirname(__file__)
__reportsfile__ = [rf for rf in listdir(__reportdir__) if
                   (path.isfile(path.join(__reportdir__, rf)))]
