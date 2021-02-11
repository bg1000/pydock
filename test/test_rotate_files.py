import logging
import os
import unittest
from unittest.mock import Mock
from unittest.mock import call

from pydock.pydock import ComposeFileManager


config = {"general": {}}
config["general"]["versions"] = 3
config["general"]["compose_file"] = "/docker/docker-compose.yml"


class RotateFilesTest(unittest.TestCase):
    def test_only_compose_file(self):
        """ Test file rotation with only compose file. """

        test_cfm = ComposeFileManager(config)
        test_cfm.list_versions = Mock()
        os.remove = Mock()
        os.rename = Mock()
        test_cfm.list_versions.return_value = ["docker-compose.yml"]
        test_cfm.rotate_files()
        os.remove.assert_not_called()
        os.rename.assert_not_called()

    def test_compose_with_one_backup(self):
        """ Test file rotation with compose file and a backup. """

        test_cfm = ComposeFileManager(config)
        test_cfm.list_versions = Mock()
        os.remove = Mock()
        os.rename = Mock()
        test_cfm.list_versions.return_value = [
            "docker-compose.yml",
            "docker-compose.yml.1",
        ]
        test_cfm.rotate_files()
        os.remove.assert_not_called()
        os.rename.assert_called_once_with(
            "docker-compose.yml.1", "docker-compose.yml.2"
        )

    def test_skip_a_backup(self):
        """ Test file rotation if a backup is skipped. """

        test_cfm = ComposeFileManager(config)
        test_cfm.list_versions = Mock()
        os.remove = Mock()
        os.rename = Mock()
        test_cfm.list_versions.return_value = [
            "docker-compose.yml",
            "docker-compose.yml.1",
            "docker-compose.yml.3",
        ]
        test_cfm.rotate_files()
        os.remove.assert_not_called()
        calls = [
            call("docker-compose.yml.3", "docker-compose.yml.4"),
            call("docker-compose.yml.1", "docker-compose.yml.2"),
        ]
        os.rename.assert_has_calls(calls, any_order=False)

    def test_too_many_backups(self):
        """Test file rotation if we start with more than the
        number of configured backups."""

        test_cfm = ComposeFileManager(config)
        test_cfm.list_versions = Mock()
        os.remove = Mock()
        os.rename = Mock()
        test_cfm.list_versions.return_value = [
            "docker-compose.yml",
            "docker-compose.yml.1",
            "docker-compose.yml.2",
            "docker-compose.yml.3",
            "docker-compose.yml.4",
        ]
        test_cfm.rotate_files()
        os.remove.assert_called_once_with("docker-compose.yml.4")
        calls = [
            call("docker-compose.yml.2", "docker-compose.yml.3"),
            call("docker-compose.yml.1", "docker-compose.yml.2"),
        ]
        os.rename.assert_has_calls(calls, any_order=False)


if __name__ == "__main__":
    unittest.main()
