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

        # open = Mock()
        # yaml.load = Mock()
        # yaml.load.return_value = 

        # os.listdir.return_value = ["docker-compose.yml"]
        # file_list = test_cfm.list_versions()
        # expected_list = ["docker-compose.yml"]
        # self.assertEqual(file_list, expected_list)

    def test_with_docker_api(self):
        pass
        # This test mocks readings and writing files and injects a known test input file.
        # It verifies the correct output file is generated and includes actually using the docker sdk
        # If any of the image:tag specified in the test file are deleted from docker hub this test will break
 
        test_cfm = ComposeFileManager(config)
        open = Mock()
        yaml.load = Mock()
        yaml.load.return_value = self.test_input
        test_cfm.add_ids()
 
        self.assertEqual(test_cfm.new_compose, self.test_output) 

    
if __name__ == '__main__':
    unittest.main()