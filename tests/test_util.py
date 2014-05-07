""" General support infrastructure not tied to any particular test.
"""
import os
from operator import itemgetter

import unittest

NO_CLOUDMAN_MESSAGE = "CloudMan required and no CloudMan AMI configured."
NO_GALAXY_MESSAGE = "Externally configured Galaxy required, but not found. Set BIOBLEND_GALAXY_URL and BIOBLEND_GALAXY_API_KEY to run this test."
MISSING_TOOL_MESSAGE = "Externally configured Galaxy instance requires tool %s to run test."


def skip_unless_cloudman():
    """ Decorate tests with this to skip the test if CloudMan is not
    configured.
    """
    test = lambda f: f
    if 'BIOBLEND_AMI_ID' not in os.environ:
        test = unittest.skip(NO_CLOUDMAN_MESSAGE)
    return test


def skip_unless_galaxy():
    """ Decorate tests with this to skip the test if Galaxy is not
    configured.
    """
    test = lambda f: f
    for prop in ['BIOBLEND_GALAXY_URL', 'BIOBLEND_GALAXY_API_KEY']:
        if prop not in os.environ:
            test = unittest.skip(NO_GALAXY_MESSAGE)
            break

    return test


def skip_unless_tool(tool_id):
    """ Decorate an Galaxy test method as requiring a specific tool,
    have skip the test case is the tool is unavailable.
    """

    def method_wrapper(method):

        def get_tool_ids(has_gi):
            tools = has_gi.gi.tools.get_tools()
            # In panels by default, so flatten out sections...
            tool_ids = map(itemgetter("id"), tools)
            return tool_ids

        def wrapped_method(has_gi, *args, **kwargs):
            if tool_id not in get_tool_ids(has_gi):
                raise unittest.SkipTest(MISSING_TOOL_MESSAGE % tool_id)

            return method(has_gi, *args, **kwargs)

        # Must preserve method name so nose can detect and report tests by
        # name.
        wrapped_method.__name__ = method.__name__
        return wrapped_method

    return method_wrapper
