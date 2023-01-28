# modules
import src


class InstanceExec(src.Instance):
    """
    A class to execute commands in the docker container
    It needs to capture the results and return it back as well.
    Hence, this is another class. Single Responsibility.
    """

    def __init__(self, command: str, instance_hash: str) -> None:
        super().__init__(instance_hash)
        self.command: str = command

    def handle(self) -> list:
        """run the docker command capture the output and return the result"""
        pass
