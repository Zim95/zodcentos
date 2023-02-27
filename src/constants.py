"""
Constants for the applicationsrc/instance_exec.py

Author: Namah Shrestha
"""
import os

# Keys
INSTANCE_OS: str = "instance_os"
COMMAND: str = "command"
INSTANCE_HASH: str = "instance_hash"
EXEC_COMMAND: str = "exec_command"

# SUPPORTED COMMANDS
CREATE: str = "CREATE"
EXECUTE: str = "EXEC"
DELETE: str = "DELETE"
SUPPORTED_COMMANDS: list = [CREATE, EXECUTE, DELETE]

# SUPPORTED OS
CENTOS: str = "centos"
UBUNTU: str = "ubuntu"
SUPPORTED_OS: list = [CENTOS, UBUNTU]

# Directory constants
CHANGE_DIRECTORY_CMD_PATTERN: str = "^cd [/a-zA-Z0-9.+~]+$"
MAIN_WORKING_DIRECTORY: str = os.path.abspath("")

# CENTOS IMAGE DEVELOPMENT
CENTOS_IMAGE_NAME: str = "centos-demo"
CENTOS_IMAGE_TAG: str = "latest"
CENTOS_DOCKERFILE_NAME: str = "Dockerfile.centos"
CENTOS_CONTAINER_NAME: str = "centos_demo_{}"
CENTOS_FILTER_CONTAINER: str = "docker container ls -q --filter 'name={}'"

# UBUNTU IMAGE DEVELOPMENT
UBUNTU_IMAGE_NAME: str = "ubuntu-demo"
UBUNTU_IMAGE_TAG: str = "latest"
UBUNTU_DOCKERFILE_NAME: str = "Dockerfile.ubuntu"
UBUNTU_CONTAINER_NAME: str = "ubuntu_demo_{}"
UBUNTU_FILTER_CONTAINER: str = "docker container ls -q --filter 'name={}'"
