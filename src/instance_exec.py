# modules
import src
import constants

# builtins
import os


class InstanceExec(src.Instance):
    """
    A class to execute commands in the docker container
    It needs to capture the results and return it back as well.
    Hence, this is another class. Single Responsibility.
    """

    def __init__(self, command: str, instance_hash: str) -> None:
        super().__init__(instance_hash)
        self.command: str = command

    def parse_command_result(self, command_result: str) -> list:
        """
        Parse command result.
        Steps:
        1. Split the lines
        2. Return

        We will add the steps as per requirements
        """
        res: str = command_result.split("\n")
        return res

    def handle(self) -> list:
        """run the docker command capture the output and return the result"""
        try:
            result: list = os.popen(
                f"docker container exec -it {constants.CENTOS_FILTER_CONTAINER.format(self.instance_hash)} {self.command}"
            ).read()
            return self.parse_command_result(result)
        except Exception as e:
            raise Exception(e)
