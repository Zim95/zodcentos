"""
This is the instance execution functional dependency section.

Here commands are executed in the container. Everything related to commands
like execution, parsing and returning the captured output happens here.

Author: Namah Shrestha
"""


# modules
import src

# builtins
import os


class InstanceExec(src.Instance):
    """
    A class to execute commands in the docker container
    It needs to capture the results and return it back as well.
    Hence, this is another class. Single Responsibility.

    This is the execution controller of the application.

    Author: Namah Shrestha
    """

    def __init__(
        self, command: str, instance_hash: str, filter_container_command: str
    ) -> None:
        super().__init__(instance_hash)
        self.command: str = command
        self.filter_container_command: str = filter_container_command

    def parse_command_result(self, command_result: str) -> list:
        """
        Parse command result.
        Steps:
        1. Split the lines
        2. Return

        We will add the steps as per requirements

        Author: Namah Shrestha
        """
        res: str = command_result.split("\n")
        return res

    def handle(self) -> list:
        """
        Run the docker command capture the output and return the result

        Author: Namah Shrestha
        """
        try:
            result: list = os.popen(
                f"docker container exec -it $({self.filter_container_command.format(self.instance_hash)}) {self.command}"
            ).read()
            return self.parse_command_result(result)
        except Exception as e:
            raise Exception(e)


class CENTOSInstanceExec(InstanceExec):
    """
    CENTOS implementation of instance exec

    Author: Namah Shrestha
    """

    def __init__(
        self, command: str, instance_hash: str, filter_container_command: str
    ) -> None:
        self.command: str = command
        self.instance_hash: str = instance_hash
        self.filter_container_command: str = filter_container_command
        super().__init__(
            self.command, self.instance_hash, self.filter_container_command
        )
