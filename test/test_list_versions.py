import os
import unittest
from unittest.mock import Mock

from pydock.pydock import ComposeFileManager

config = {"general": {}}
config["general"]["versions"] = 5
config["general"]["compose_file"] = "/docker/docker-compose.yml"


class ListVersionsTest(unittest.TestCase):
    def test_only_compose_file(self):
        """ Test case where only compose file is in directory. """

        os.listdir = Mock()
        test_cfm = ComposeFileManager(config)
        os.listdir.return_value = ["docker-compose.yml"]
        file_list = test_cfm.list_versions()
        expected_list = ["docker-compose.yml"]
        self.assertEqual(file_list, expected_list)

    def test_multiple_backups_found(self):
        """ Test case where compose file plus multiple backups are in directory. """

        os.listdir = Mock()
        test_cfm = ComposeFileManager(config)
        os.listdir.return_value = [
            "docker-compose.yml",
            "docker-compose.yml.3",
            "docker-compose.yml.1",
            "docker-compose.yml.2",
        ]
        file_list = test_cfm.list_versions()
        expected_list = [
            "docker-compose.yml",
            "docker-compose.yml.1",
            "docker-compose.yml.2",
            "docker-compose.yml.3",
        ]
        self.assertEqual(file_list, expected_list)

    def test_other_files_found(self):
        """ Test case where other non-related files are in directory. """

        os.listdir = Mock()
        test_cfm = ComposeFileManager(config)
        os.listdir.return_value = [
            "docker-compose.yml",
            "whatever.txt",
            "docker-compose.save",
            "docker-compose.yml.1",
        ]
        file_list = test_cfm.list_versions()
        expected_list = ["docker-compose.yml", "docker-compose.yml.1"]
        self.assertEqual(file_list, expected_list)

    def test_non_conforming_files_found(self):
        """ Test case where docker-compose.yml.XXX (not an integer) files are found in directory """

        os.listdir = Mock()
        test_cfm = ComposeFileManager(config)
        os.listdir.return_value = [
            "docker-compose.yml",
            "whatever.txt",
            "docker-compose.yml.save",
            "docker-compose.yml.1",
        ]
        file_list = test_cfm.list_versions()
        expected_list = ["docker-compose.yml", "docker-compose.yml.1"]
        self.assertEqual(file_list, expected_list)


if __name__ == "__main__":
    unittest.main()
