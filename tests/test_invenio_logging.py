# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
# Copyright (C) 2015 CERN.
#
# Invenio is free software; you can redistribute it
# and/or modify it under the terms of the GNU General Public License as
# published by the Free Software Foundation; either version 2 of the
# License, or (at your option) any later version.
#
# Invenio is distributed in the hope that it will be
# useful, but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Invenio; if not, write to the
# Free Software Foundation, Inc., 59 Temple Place, Suite 330, Boston,
# MA 02111-1307, USA.
#
# In applying this license, CERN does not
# waive the privileges and immunities granted to it by virtue of its status
# as an Intergovernmental Organization or submit itself to any jurisdiction.


"""Module tests."""

from __future__ import absolute_import, print_function

import os
from flask import Flask
from flask_babelex import Babel


from invenio_logging.ext_fs import InvenioLoggingFs
from invenio_logging.ext_sentry import InvenioLoggingSentry
import mock


def test_version():
    """Test version import."""
    from invenio_logging import __version__
    assert __version__


def test_init(generic_app):
    """Test extension initialization."""
    # raise Exception("test_init")

    ext = InvenioLoggingSentry(generic_app)
    assert 'invenio-logging-sentry' in generic_app.extensions
    ext = InvenioLoggingFs(generic_app)
    assert 'invenio-logging-fs' in generic_app.extensions

    """app = Flask('testapp')
    ext = InvenioLoggingFs()
    assert 'invenio-logging-fs' not in app.extensions
    ext.init_app(app)
    assert 'invenio-logging-fs' in app.extensions"""


def test_sentry(app_for_sentry):
    simple_mock = mock.MagicMock(return_value=True)
    # print ("Starting sentry registration")
    # assert False
    # InvenioLoggingSentry(app=app_for_sentry, test_param=simple_mock)

    # Do the logging
    import random
    test_strings = [str(random.random()) for i in range(2)]
    # app_for_sentry.logger.warning(test_strings[0])
    # app_for_sentry.logger.error(test_strings[1])
    print ("CALLCOUNT={} ARGS={}".format(
        simple_mock.call_count, simple_mock.call_args_list))
    assert False


def test_fs(app_for_fs):
    """Test view."""
    InvenioLoggingFs(app_for_fs)

    import random
    test_strings = [str(random.random()) for i in range(2)]
    app_for_fs.logger.warning(test_strings[0])
    app_for_fs.logger.error(test_strings[1])

    log_file_name = os.path.join(app_for_fs.instance_path,
                                 app_for_fs.config.get('CFG_LOGDIR', ''),
                                 app_for_fs.logger_name) + '.log'
    log_file_contents = open(log_file_name).read()

    # Test whether logfiles contain required string
    assert ("WARNING: " + test_strings[0]) in log_file_contents
    assert ("ERROR: " + test_strings[1]) in log_file_contents
