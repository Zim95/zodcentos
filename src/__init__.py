# builtins
import json
import abc

# modules
import src.constants as constants


class Instance:
    def __init__(self, instance_hash: str) -> None:
        self.instance_hash: str = instance_hash

    def handle(self) -> list:
        pass


class InstanceMessage:
    @staticmethod
    def is_schema_valid(message: str) -> bool:
        try:
            json_message: dict = json.loads(message)
            command: str = json_message.get(constants.COMMAND)
            instance_hash: str = json_message.get(constants.INSTANCE_HASH)
            if not command or not instance_hash:
                return False
            return True
        except json.JSONDecodeError:
            raise json.JSONDecodeError(
                "Invalid message body format. Message body format is \{'command': '<command>', 'instance_hash': '<instance_hash>'\}"
            )

    @staticmethod
    def decode_message(message: str) -> str:
        return json.loads(message)
