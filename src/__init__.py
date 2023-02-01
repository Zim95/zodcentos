"""
Here we have instance related code.

Functional Dependencies:
------------------------
1. Should create a container for the mentioned operating system. Currently only Centos is supported.
2. Should delete the container.
3. Should execute commands on the container.
"""

# builtins
import json
import typing

# modules
import src.constants as constants


class Instance:
    """
    This is the instance class. It has a instance hash that is used to uniquely identify it.
    Every new session has an instance created.

    Author: Namah Shrestha
    """

    def __init__(self, instance_hash: str) -> None:
        self.instance_hash: str = instance_hash

    def handle(self, exec_command: typing.Optional[str] = None) -> list:
        """
        This method will be implemented by various functionalities of the instance.
        This method is the handler for each funtional dependency.

        Author: Namah Shrestha
        """
        pass


class InstanceMessage:
    @staticmethod
    def is_schema_valid(message: str) -> bool:
        """
        Checks the shchema of the message and raises error if schema mismatch happens.

        Author: Namah Shrestha
        """
        try:
            json_message: dict = json.loads(message)
            instance_os: str = json_message.get(constants.INSTANCE_OS)
            command: str = json_message.get(constants.COMMAND)
            instance_hash: str = json_message.get(constants.INSTANCE_HASH)
            if not any([command, instance_hash, instance_os]):
                return False
            return True
        except json.decoder.JSONDecodeError:
            raise json.decoder.JSONDecodeError(
                """
                Please provide proper json format.
                """
            )

    @staticmethod
    def decode_message(message: str) -> str:
        """
        Decodes the message.
        Recommend validating schema before decoding.

        Author: Namah Shrestha
        """
        try:
            return json.loads(message)
        except json.decoder.JSONDecodeError:
            raise json.decoder.JSONDecodeError(
                """
                Please provide proper json format.
                """
            )
