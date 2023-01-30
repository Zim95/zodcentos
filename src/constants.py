"""
Constants for the applicationsrc/instance_exec.py
"""

COMMAND = "command"
INSTANCE_HASH = "instance_hash"


CREATE = "CREATE"
EXECUTE = "EXEC"
DELETE = "DELETE"

# CENTOS IMAGE DEVELOPMENT
CENTOS_IMAGE_NAME = "centos-demo"
CENTOS_IMAGE_TAG = "latest"
CENTOS_DOCKERFILE_NAME = "Dockerfile.centos"
CENTOS_CONTAINER_NAME = "centos_demo_{}"
CENTOS_FILTER_CONTAINER = "docker container ls --aq --filter 'name={}'"
