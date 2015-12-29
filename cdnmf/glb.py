#! /usr/bin/env python
# -*- coding: utf-8 -*-
import logging.config
import json
import os
global log, basepath

#basepath = os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir))
basepath = os.path.abspath(os.path.dirname(__file__))
config = json.load(open(os.path.join(basepath, 'logging.json'), 'r'))
logging.config.dictConfig(config)
log = logging.getLogger(__name__)
