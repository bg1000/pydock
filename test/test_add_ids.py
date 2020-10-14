import unittest
import os
from pydock.pydock import ComposeFileManager
from unittest.mock import Mock
from unittest.mock import call
import logging
import yaml
import docker
config = {"general":{}}
config["general"]["versions"] = 3
config["general"]["compose_file"] = "/docker/docker-compose.yml"

# logging.basicConfig(level=logging.DEBUG)
class AddIdsTest(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(AddIdsTest, self).__init__(*args, **kwargs)
        with open('./test/test_input.yml', 'r') as ymlfile:
            self.test_input = yaml.load(ymlfile, Loader=yaml.FullLoader)
        with open('./test/test_output.yml', 'r') as ymlfile:
            self.test_output = yaml.load(ymlfile, Loader=yaml.FullLoader)
    
    def test_yaml(self):
        pass
        # This test mocks both reading/writing files and using the docker sdk.
        # It verifies that given a certain return value from the docker sdk
        # add-ids will correctly change the yaml in the first backup

        open = Mock()
        yaml.load = Mock()
        yaml.load.return_value = self.test_input
        test_cfm = ComposeFileManager(config)
        # need to mock the two docker api calls 
        # so that reg_data and base_image are set correctly.

        # use .assert_called_once_with on the two docker sdk calls
        # use self.assertEqual(xxx, yyy) to verify the output was set correctly

    
if __name__ == '__main__':
    unittest.main()