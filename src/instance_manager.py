import os


class InstanceManager:
    def create_instance(self) -> None:
        """
        1. Build the image from the dockerfile.
        2. Create a container from the image.
        3. Run the container.
        """
        try:
            os.system("docker image build . -t centos-demo:latest -f Dockerfile.centos")
            os.system("docker container run --name centos_demo -d centos-demo:latest")
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
                "docker container stop $(docker container ls -aq --filter 'name=centos_demo')"
            )
            os.system(
                "docker container rm $(docker container ls -aq --filter 'name=centos_demo')"
            )
            os.system("docker image rm -f centos-demo:latest")
        except Exception as e:
            raise Exception(e)
