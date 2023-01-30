"""
This is the main application. This creates async web sockets to pass message to and from the 
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
command_switch: dict = {
    constants.CREATE: im.InstanceManager,
    constants.EXECUTE: ie.InstanceExec,
    constants.DELETE: im.InstanceManager,
}


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
            command: str = json_message.get(constants.COMMAND)
            if not command:
                raise ValueError(f"Unsupported command: {command}")
            instance_hash: str = json_message[constants.INSTANCE_HASH]
            exec_class: typing.Union[
                im.InstanceManager, ie.InstanceExec
            ] = command_switch.get(command)
            exec_obj: typing.Union[im.InstanceManager, ie.InstanceExec] = exec_class(
                command, instance_hash
            )
            response: list = exec_obj.handle()
            await websocket.send(json.dumps(response))
    except Exception as e:
        raise Exception(e)


if __name__ == "__main__":
    """
    Server creation and service.

    Author: Namah Shrestha
    """
    start_server = websockets.serve(socket_handler, "0.0.0.0", 8888)
    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever()
