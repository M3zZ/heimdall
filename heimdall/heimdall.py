#!/usr/bin/env python
# -*- coding: utf-8 -*-

from core.arguments import ArgumentsHandler

if __name__ == "__main__":
    try:
        ArgumentsHandler()
    except KeyboardInterrupt:
        print '\nExiting Heimdall ...'
        exit(1)
