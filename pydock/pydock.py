import argparse
import copy
import fnmatch
import logging
import os

import docker
import yaml


class ComposeFileManager(object):
    def __init__(self, config):
        self.docker_client = docker.from_env()
        self.versions = config["general"]["versions"]
        self.compose_file_with_path = config["general"]["compose_file"]
        self.compose_file = os.path.basename(config["general"]["compose_file"])
        self.compose_path = os.path.dirname(config["general"]["compose_file"])
        if not os.path.isfile(self.compose_file_with_path):
            raise FileNotFoundError("Unable to locate " + self.compose_file_with_path)

    def rotate_files(self):
        """Makes docker-compose.yml docker-compose.yml.1
        and rotates other files up to docker-compose.yml.n"""

        file_list = self.list_versions()
        os.chdir(self.compose_path)
        for file_index in range(len(file_list) - 1, -1, -1):
            if file_index > self.versions:
                os.remove(file_list[file_index])
            elif file_index < self.versions and file_index != 0:
                logging.debug("file_index = " + str(file_index))
                logging.debug("file = " + file_list[file_index])
                split_filename = file_list[file_index].split(".")
                version = int(split_filename[2])
                os.rename(
                    file_list[file_index],
                    split_filename[0]
                    + "."
                    + split_filename[1]
                    + "."
                    + str(version + 1),
                )

    def add_ids(self):
        """Queries docker to get id of container based on
        image name and tag"""

        with open(self.compose_file_with_path, "r") as ymlfile:
            self.original_compose = yaml.load(ymlfile, Loader=yaml.FullLoader)
        self.new_compose = copy.deepcopy(self.original_compose)
        for app in self.new_compose["services"]:
            logging.debug("Found app " + app)
            app_config = self.new_compose["services"][app]
            if "image" in app_config:
                logging.debug(app + " is using image " + app_config["image"])
                logging.debug(
                    app + " container is named " + app_config["container_name"]
                )
                container = self.docker_client.containers.get(
                    app_config["container_name"]
                )
                reg_data = self.docker_client.images.get_registry_data(
                    container.attrs["Config"]["Image"]
                )
                base_image = app_config["image"].split(":")[0]
                logging.info(
                    app
                    + " is using image "
                    + app_config["image"]
                    + " with registry id "
                    + reg_data.id
                )
                self.new_compose["services"][app]["image"] = (
                    base_image + "@" + reg_data.id
                )
        with open(
            os.path.join(self.compose_path, self.compose_file) + ".1", "w"
        ) as first_backup:
            yaml.dump(self.new_compose, first_backup, sort_keys=False)

    def list_versions(self):
        """returns 'compose_file', 'compose_file'.1, .2 etc.
        removes everything else including other variations of 'compose-file'
        e.g. - 'compose-file'.save would not be included"""

        file_list = []
        temp_list = os.listdir(self.compose_path)
        for filename in temp_list:
            if filename == self.compose_file:
                file_list.append(filename)
            elif filename.startswith(self.compose_file):
                file_parts = filename.split(".")
                if len(file_parts) == 3:
                    if file_parts[2].isdigit():
                        file_list.append(filename)
        file_list.sort()
        return file_list

    def __del__(self):
        self.docker_client.close()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--config",
        help="path where config.yaml is located",
        default=os.path.dirname(os.path.realpath(__file__)),
    )
    args = parser.parse_args()

    if args.config[-1] == "/":
        config_file = args.config + "config.yaml"
    else:
        config_file = args.config + "/config.yaml"
    with open(config_file, "r") as ymlfile:
        config = yaml.load(ymlfile, Loader=yaml.SafeLoader)
        print("using configuration from " + config_file)
    logging.basicConfig(level=config["logging"]["log_level"])
    cfm = ComposeFileManager(config)
    cfm.rotate_files()
    cfm.add_ids()


if __name__ == "__main__":
    main()
