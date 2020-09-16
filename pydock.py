import docker
import argparse
import yaml
import os
import fnmatch
import copy
import logging

# Make this a class which accepts the compose file as part of its constructor
class ComposeFileManager(object):
    def __init__(self, config):
        self.docker_client = docker.from_env()
        self.versions = config["general"]["versions"]
        self.compose_file = os.path.basename(config["general"]["compose_file"])
        self.compose_path = os.path.dirname(config["general"]["compose_file"])
    
    def rotate_files(self):
        file_list = self.list_versions()
        os.chdir(self.compose_path)
        file_list.sort()
        for file_index in range(len(file_list)-1, -1, -1):
            if file_index > self.versions - 1:
                os.remove(file_list[file_index])
            elif file_index < self.versions and file_index != 0:
                split_filename = file_list[file_index].split(".")
                version = int(split_filename[2])
                os.rename(file_list[file_index],split_filename[0] + "." + split_filename[1]+"." + str(version+1))
    
    def add_ids(self):
        with open(os.path.join(self.compose_path,self.compose_file), 'r') as ymlfile:
            self.original_compose = yaml.load(ymlfile, Loader=yaml.FullLoader)
        self.new_compose = copy.deepcopy(self.original_compose)
        for app in self.new_compose["services"]:
            logging.debug ("Found app " + app)
            app_config = self.new_compose["services"][app]
            if "image" in app_config:
                logging.debug(app + " is using image " + app_config["image"])
                logging.debug(app + " container is named " + app_config["container_name"])
                container = self.docker_client.containers.get(app_config["container_name"])
                reg_data = self.docker_client.images.get_registry_data(container.attrs["Config"]["Image"])
                base_image =  app_config["image"].split(":")[0]
                self.new_compose["services"][app]["image"] = base_image + "@" + reg_data.id
        with open(os.path.join(self.compose_path,self.compose_file)+ ".1", 'w') as first_backup:
            yaml.dump(self.new_compose, first_backup)
    
    def list_versions(self):
        #
        # returns docker-compose.yml + .1, .2, etc.
        # 
        file_list = []
        temp_list = os.listdir(self.compose_path)
        for filename in temp_list:
            if filename.startswith(self.compose_file):
                file_list.append(filename)
        return file_list




def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", help="path where config.yaml is located", 
                   default = os.path.dirname(os.path.realpath(__file__)) )
    args = parser.parse_args()

    if args.config[-1] == "/":
        config_file = args.config + "config.yaml"
    else:
        config_file = args.config + "/config.yaml"
    with open(config_file, 'r') as ymlfile:
        config = yaml.load(ymlfile, Loader=yaml.FullLoader)
        print("using configuration from " + config_file)
    logging.basicConfig(level=config["logging"]["log_level"])
    cfm = ComposeFileManager(config)
    cfm.rotate_files()
    cfm.add_ids()

if __name__ == '__main__':
    main()