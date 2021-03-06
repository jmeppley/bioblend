import os, time
from bioblend import galaxy
from test_util import unittest


class GalaxyTestBase(unittest.TestCase):

    def setUp(self):
        galaxy_key = os.environ['BIOBLEND_GALAXY_API_KEY']
        galaxy_url = os.environ['BIOBLEND_GALAXY_URL']
        self.gi = galaxy.GalaxyInstance(url=galaxy_url, key=galaxy_key)

    def _test_dataset(self, history_id, contents="1\t2\t3", **kwds):
        tool_output = self.gi.tools.paste_content(contents, history_id, **kwds)
        return tool_output["outputs"][0]["id"]

    def _wait_for_history(self, history_id, timeout_seconds=15):
        def _state_ready(state_str):
            if state_str == 'ok':
                return True
            elif state_str == 'error':
                raise Exception('History in error state')
            return False

        for _ in range(timeout_seconds):
            state = self.gi.histories.show_history(history_id)['state']
            if _state_ready(state):
                return
            time.sleep(1)
        return _state_ready(state)
