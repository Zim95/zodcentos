# builtins
import os

# module
import src
import constants


class InstanceManager(src.Instance):
    def __init__(
        self,
        command: str,
        instance_hash: str,
        image_name: str,
        image_tag: str,
        dockerfile_name: str,
        filter_container_command: str,
    ) -> None:
        super().__init__(instance_hash)
        self.command: str = command
        self.image_name: str = image_name
        self.image_tag: str = image_tag
        self.dockerfile_name: str = dockerfile_name
        self.filter_container_command: str = filter_container_command

    def create_instance(self) -> None:
        """
        1. Build the image from the dockerfile.
        2. Create a container from the image.
        3. Run the container.
        """
        try:
            os.system(
                f"docker image build . -t {self.image_name}:{self.image_tag} -f {self.dockerfile_name}"
            )
            os.system(
                f"docker container run $({self.filter_container_command.format(self.instance_hash)}) -d {self.image_name}:{self.image_tag}"
            )
        except Exception as e:
            raise Exception(e)

    def delete_instance(self) -> None:
        """
        1. Stop the running container
        2. Delete the container
        3. Delete the image
        """
        try:
            os.system(
                f"docker container stop $({self.filter_container_command.format(self.instance_hash)})')"
            )
            os.system(
                f"docker container rm $({self.filter_container_command.format(self.instance_hash)})')"
            )
            os.system(f"docker image rm -f {self.image_name}:{self.image_tag}")
        except Exception as e:
            raise Exception(e)

    def handle(self) -> list:
        if self.command == src.constants.CREATE:
            self.create_instance()
            return [0]
        elif self.command == src.constants.DELETE:
            self.delete_instance()
            return [2]


class CentosInstanceManager(InstanceManager):
    """
    CENTOS implementation of instance manager strategy
    """

    def __init__(self, command: str, instance_hash: str) -> None:
        self.command: str = command
        self.instance_hash: str = instance_hash
        self.image_name: str = constants.CENTOS_IMAGE_NAME
        self.image_tag: str = constants.CENTOS_IMAGE_TAG
        self.dockerfile_name: str = constants.CENTOS_DOCKERFILE_NAME
        self.filter_container_command: str = constants.CENTOS_FILTER_CONTAINER
        super().__init__(
            self.command,
            self.instance_hash,
            self.image_name,
            self.image_tag,
            self.dockerfile_name,
            self.filter_container_command,
        )
