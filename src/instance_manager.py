"""
This deals with the creation and deletion of os instances.
This is the on demand section of the application.

Author: Namah Shrestha
"""

# builtins
import os

# module
import src
import src.constants as constants


class InstanceManager(src.Instance):
    """
    Manages the creation and deletion of containers.

    This is the controller for instance management.

    Author: Namah Shrestha
    """

    def __init__(
        self,
        command: str,
        instance_hash: str,
        image_name: str,
        image_tag: str,
        container_name: str,
        dockerfile_name: str,
        filter_container_command: str,
    ) -> None:
        """
        NOTE:
        For every command we create a new instance. This is so that
        every command can be executed in a different thread seperately.
        Thread safety considerations.
        If we use a single manager then there might be a time where
        we might need to use mutex locks for the manager. Causing synchronization issues.
        Rather we would like to create separate instances per thread.

        Therefore the command is part of the constructor. For every command a new instance will run.
        Of course we need to make sure the container exists before we delete it and things like that.
        All of that will be handled with exceptions.

        Author: Namah Shrestha
        """
        super().__init__(instance_hash)
        self.command: str = command
        self.image_name: str = image_name
        self.image_tag: str = image_tag
        self.container_name: str = container_name
        self.dockerfile_name: str = dockerfile_name
        self.filter_container_command: str = filter_container_command.format(
            self.container_name
        )

    def create_instance(self) -> None:
        """
        1. Build the image from the dockerfile.
        2. Create a container from the image.
        3. Run the container.

        Author: Namah Shrestha
        """
        try:
            os.system(
                f"docker image build . -t {self.image_name}:{self.image_tag} -f {self.dockerfile_name}"
            )
            os.system(
                f"docker container run --name {self.container_name} -d {self.image_name}:{self.image_tag}"
            )
        except Exception as e:
            raise Exception(e)

    def delete_instance(self) -> None:
        """
        1. Stop the running container
        2. Delete the container
        3. Delete the image

        Author: Namah Shrestha
        """
        try:
            os.system(
                f"docker container stop $({self.filter_container_command.format(self.instance_hash)})"
            )
            os.system(
                f"docker container rm $({self.filter_container_command.format(self.instance_hash)})"
            )
            os.system(f"docker image rm -f {self.image_name}:{self.image_tag}")
        except Exception as e:
            raise Exception(e)

    def handle(self) -> list:
        """
        Handle create and delete container commands

        Author: Namah Shrestha
        """
        if self.command == src.constants.CREATE:
            self.create_instance()
            return [0]
        elif self.command == src.constants.DELETE:
            self.delete_instance()
            return [2]


class CentosInstanceManager(InstanceManager):
    """
    CENTOS implementation of instance manager strategy

    Author: Namah Shrestha
    """

    def __init__(self, command: str, instance_hash: str) -> None:
        self.command: str = command
        self.instance_hash: str = instance_hash
        self.image_name: str = constants.CENTOS_IMAGE_NAME
        self.image_tag: str = constants.CENTOS_IMAGE_TAG
        self.container_name: str = constants.CENTOS_CONTAINER_NAME.format(
            self.instance_hash
        )
        self.dockerfile_name: str = constants.CENTOS_DOCKERFILE_NAME
        self.filter_container_command: str = constants.CENTOS_FILTER_CONTAINER.format(
            self.container_name
        )
        super().__init__(
            self.command,
            self.instance_hash,
            self.image_name,
            self.image_tag,
            self.container_name,
            self.dockerfile_name,
            self.filter_container_command,
        )
