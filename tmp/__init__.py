# -*- coding: utf-8 -*-
from os import path, listdir

__generatedscripts__ = 'generated_scripts/'
__tmpdir__ = path.join(path.dirname(__file__), __generatedscripts__)
__tmpfiles__ = [tmpf for tmpf in listdir(__tmpdir__) if (path.isfile(path.join(__tmpdir__, tmpf)))]
