#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask_script import Manager, Server
from flask_script.commands import Clean, ShowUrls

from wgp_demo.app import create_and_initialize_app

app = create_and_initialize_app()
manager = Manager(app)

manager.add_command('server', Server())
manager.add_command('urls', ShowUrls())
manager.add_command('clean', Clean())

if __name__ == '__main__':
    manager.run()
