"""
Constants for the applicationsrc/instance_exec.py

Author: Namah Shrestha
"""

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
SUPPORTED_OS: list = [CENTOS]

# CENTOS IMAGE DEVELOPMENT
CENTOS_IMAGE_NAME: str = "centos-demo"
CENTOS_IMAGE_TAG: str = "latest"
CENTOS_DOCKERFILE_NAME: str = "Dockerfile.centos"
CENTOS_CONTAINER_NAME: str = "centos_demo_{}"
CENTOS_FILTER_CONTAINER: str = "docker container ls -q --filter 'name={}'"
