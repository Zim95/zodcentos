# builtins
import os

# module
import src


class InstanceManager(src.Instance):
    def __init__(self, command: str, instance_hash: str) -> None:
        super().__init__(instance_hash)
        self.command: str = command

    def create_instance(self) -> None:
        """
        1. Build the image from the dockerfile.
        2. Create a container from the image.
        3. Run the container.
        """
        try:
            os.system("docker image build . -t centos-demo:latest -f Dockerfile.centos")
            os.system(
                f"docker container run --name centos_demo_{self.instance_hash} -p 0.0.0.0:7777:22 -d centos-demo:latest"
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
                f"docker container stop $(docker container ls -aq --filter 'name=centos_demo_{self.instance_hash}')"
            )
            os.system(
                f"docker container rm $(docker container ls -aq --filter 'name=centos_demo_{self.instance_hash}')"
            )
            os.system("docker image rm -f centos-demo:latest")
        except Exception as e:
            raise Exception(e)

    def handle(self) -> list:
        if self.command == src.constants.CREATE:
            self.create_instance()
            return [0]
        elif self.command == src.constants.DELETE:
            self.delete_instance()
            return [2]
