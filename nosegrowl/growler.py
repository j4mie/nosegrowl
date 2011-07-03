"""
nose plugin for easy testing of django projects and apps. Sets up a test
database (or schema) and installs apps from test settings file before tests
are run, and tears the test database (or schema) down after all tests are run.
"""
__author = 'Jason Pellerin'
__version__ = '0.1'

import atexit
import logging
import os, sys
import re
import datetime

from nose.plugins import Plugin
from pkg_resources import resource_string
import nose.case

from nose.importer import add_path

log = logging.getLogger('nose.plugins.nosegrowl')

from Growl import GrowlNotifier, GROWL_NOTIFICATIONS_DEFAULT

class SimpleNotifier(object):
    def __init__(self, app_name='PyTest'):
        self.app_icon = resource_string('nosegrowl', 'python.png')
        self.ok_icon = resource_string('nosegrowl', 'dialog-ok.png')
        self.fail_icon = resource_string('nosegrowl', 'dialog-cancel.png')

        self.growl = GrowlNotifier(applicationName=app_name,
                notifications=[GROWL_NOTIFICATIONS_DEFAULT],
                applicationIcon=self.app_icon)

    def register(self):
        self.growl.register()

    def start(self, title, description):
        self.notify(title, description, icon=self.app_icon)

    def success(self, title, description):
        self.notify(title, description, icon=self.ok_icon)

    def fail(self, title, description):
        self.notify(title=title, description=description, icon=self.fail_icon)
        
    def notify(self, title, description, icon=None, sticky=False):
        self.growl.notify(noteType=GROWL_NOTIFICATIONS_DEFAULT,
            title=title,
            description=description,
            icon=icon,
            sticky=sticky)

class NoseGrowl(Plugin):
    """
    Enable Growl notifications
    """
    name = 'growl'

    def begin(self):
        growl = SimpleNotifier()
        growl.register()
        self.start_time = datetime.datetime.now()
        growl.start("Starting tests...", 'Started at : [%s]' % self.start_time.isoformat())

    def finalize(self, result=None):
        """
        Clean up any created database and schema.
        """
        growl = SimpleNotifier()
        fail_msg = '\n'.join(["Failed: %s" % name for name, ex in result.failures])
        err_msg = '\n'.join(["Error: %s" % name for name, ex in result.errors])

        big_msg = '\n'.join([fail_msg, err_msg])

        self.finish_time = datetime.datetime.now()
            
        delta = self.finish_time - self.start_time
        endtime_msg = 'Completed in  %s.%s seconds' % (delta.seconds, delta.microseconds)
        if result.wasSuccessful():
            growl.success("%s tests run ok" % result.testsRun, endtime_msg)
        else:
            growl.fail("%s tests. %s failed. %s errors." % (result.testsRun, len(result.failures), len(result.errors)), "%s\n%s" % (big_msg, endtime_msg))
