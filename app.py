"""
This is the main application.
This creates async web sockets to pass message to and from the
client side of the application.

This is the view of the backend application.

Author: Namah Shrestha
"""

# builtins
import asyncio
import typing
import json

# third party
import websockets

# modules
import src
import src.instance_manager as im
import src.instance_exec as ie
import src.constants as constants


"""
Supported commands.

Author: Namah Shrestha
"""

instance_manager_switch: dict = {constants.CENTOS: im.CentosInstanceManager}
instance_exec_switch: dict = {constants.CENTOS: ie.CentosInstanceExec}
command_switch: dict = {
    constants.CREATE: instance_manager_switch,
    constants.EXECUTE: instance_exec_switch,
    constants.DELETE: instance_manager_switch,
}


"""
We will have one change directory handler.
This change directory handler should be specific to a session.

Author: Namah Shrestha
"""


async def socket_handler(websocket) -> None:
    try:
        """
        Handle socket connection asynchronusly and return the response.

        This is the core controller of the application.

        Author: Namah Shrestha
        """
        message: str = await websocket.recv()
        if src.InstanceMessage.is_schema_valid(message):
            json_message: dict = src.InstanceMessage.decode_message(message)
            instance_os: str = json_message.get(constants.INSTANCE_OS)
            if instance_os not in constants.SUPPORTED_OS:
                raise ValueError(f"Unsupported instance os: {instance_os}")
            command: str = json_message.get(constants.COMMAND)
            if command not in constants.SUPPORTED_COMMANDS:
                raise ValueError(f"Unsupported command: {command}")
            instance_hash: str = json_message[constants.INSTANCE_HASH]
            instance_class: typing.Union[
                im.InstanceManager, ie.InstanceExec
            ] = command_switch.get(command).get(instance_os)
            instance_obj: typing.Union[
                im.InstanceManager, ie.InstanceExec
            ] = instance_class(command, instance_hash)
            exec_command: typing.Optional[str] = json_message.get(
                constants.EXEC_COMMAND
            )
            """ Now we need to calculate the current working directory """
            response: list = instance_obj.handle(exec_command)
            await websocket.send(json.dumps(response))
        else:
            error_message: str = (
                "Invalid message body format."
                "Message should have 'instance_os',"
                " 'command', 'instance_hash', 'exec_command<optional>'"
            )
            await websocket.send(error_message)
            raise ValueError(error_message)
    except TypeError as te:
        type_error_message: str = str(te)
        await websocket.send(type_error_message)
        raise TypeError(te)
    except ValueError as ve:
        value_error_message: str = str(ve)
        await websocket.send(value_error_message)
        raise ValueError(ve)
    except Exception:
        exception_message: str = "Something went wrong"
        await websocket.send(exception_message)
        raise Exception(exception_message)


if __name__ == "__main__":
    """
    Server creation and service.

    Author: Namah Shrestha
    """
    start_server: websockets.legacy.server.Serve = websockets.serve(
        socket_handler, "0.0.0.0", 8888
    )
    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever()
