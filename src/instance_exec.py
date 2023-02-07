"""
This is the instance execution functional dependency section.

Here commands are executed in the container. Everything related to commands
like execution, parsing and returning the captured output happens here.

Author: Namah Shrestha
"""


# modules
import src
import src.constants as constants

# builtins
import os
import typing


class InstanceExec(src.Instance):
    """
    A class to execute commands in the docker container
    It needs to capture the results and return it back as well.
    Hence, this is another class. Single Responsibility.

    This is the execution controller of the application.

    Author: Namah Shrestha
    """

    def __init__(
        self,
        command: str,
        instance_hash: str,
        filter_container_command: str,
    ) -> None:
        """
        NOTE:
        For every command we create a new instance. This is so that
        every command can be executed in a different thread seperately.
        Thread safety considerations.
        If we use a single manager then there might be a time where
        we might need to use mutex locks for the manager.
        Causing synchronization issues.
        Rather we would like to create separate instances per thread.

        Therefore the command is part of the constructor.
        For every command a new instance will run.
        Of course we need to make sure the container exists
        before we delete it and things like that.
        All of that will be handled with exceptions.

        Author: Namah Shrestha
        """
        super().__init__(instance_hash)
        self.command: str = command
        self.filter_container_command: str = filter_container_command

    def parse_command_result(self, command_result: str) -> list:
        """
        Parse command result.
        Steps:
        1. Split the lines
        2. Return

        We will add the steps as per requirements.
        For now only split and return

        Author: Namah Shrestha
        """
        res: str = command_result.split("\n")
        return res

    def exec_instance(self, exec_command: typing.Optional[str] = None) -> str:
        """
        Run the docker command capture the output and return the result

        Author: Namah Shrestha
        """
        try:
            result: str = os.popen(
                f"docker container exec $({self.filter_container_command})"
                f" {exec_command}"
            ).read()
            return result
        except Exception as e:
            raise Exception(e)

    def handle(self, exec_command: typing.Optional[str] = None) -> list:
        """
        Run the docker command capture the output and return the result

        Author: Namah Shrestha
        """
        try:
            exec_result: list = self.exec_instance(exec_command)
            return self.parse_command_result(exec_result)
        except Exception as e:
            raise Exception(e)


class CentosInstanceExec(InstanceExec):
    """
    CENTOS implementation of instance exec

    Author: Namah Shrestha
    """

    def __init__(self, command: str, instance_hash: str) -> None:
        self.command: str = command
        self.instance_hash: str = instance_hash
        self.container_name: str = constants.CENTOS_CONTAINER_NAME.format(
            self.instance_hash
        )
        self.filter_container_command: str = constants.CENTOS_FILTER_CONTAINER.format(
            self.container_name
        )  # noop
        super().__init__(
            self.command,
            self.instance_hash,
            self.filter_container_command,
        )
