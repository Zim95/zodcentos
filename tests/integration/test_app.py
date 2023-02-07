"""
Integration test for the main web socket application.

Author: Namah Shrestha
"""

# builtins
import unittest
import asyncio
import json
import os

# modules
import src.instance_manager as im
import src.constants as constants

# third party
import websockets


"""
We have to create client tasks to test the execution of the application.
Since our webserver will be running as well.

If we have normal coroutines then another coroutine will run only
after the previous coroutine will end.

If it is a task then they will run in non blocking fashion.
Therefore, we will create client tasks and a server running task.

We will run the server task and then the client tasks and check the response.

We will run these coroutines in proper order within the test_everything coroutine.
The test_everything coroutine will run in the event loop.

If any of the test cases fail, test_everything coroutine will return False
If all tests pass, test_everything coroutine will return True

Author: Namah Shrestha
"""


async def test_send(message: str) -> str:
    """
    This is the client message sending coroutine

    Author: Namah Shrestha
    """
    async with websockets.connect("ws://0.0.0.0:8888") as ws:
        await ws.send(message)
        res: str = await ws.recv()
        return res


class TestApp(unittest.TestCase):
    def setUp(self) -> None:
        """
        1. Create the web server container
        2. Create all the tasks

        Author: Namah Shrestha
        """
        try:
            os.system("docker-compose up -d")
        except Exception as e:
            raise Exception(e)

    def test_all_invalid_message(self) -> None:
        """
        This test is an actual simulation of the entire application

        Author: Namah Shrestha
        """
        test_send_invalid_message_task: asyncio.Task = (
            asyncio.get_event_loop().create_task(test_send("asd"))
        )
        res: bool = asyncio.get_event_loop().run_until_complete(
            test_send_invalid_message_task
        )
        self.assertEqual(
            res, "__init__() missing 2 required positional arguments: 'doc' and 'pos'"
        )

    def test_improper_message(self) -> None:
        """
        This test is for proper json but improper schema

        Author: Namah Shrestha
        """
        test_send_improper_message_task: asyncio.Task = (
            asyncio.get_event_loop().create_task(test_send('{"x": 1}'))
        )
        res: bool = asyncio.get_event_loop().run_until_complete(
            test_send_improper_message_task
        )
        self.assertEqual(
            res,
            "Invalid message body format. Message should have 'instance_os', 'command', 'instance_hash', 'exec_command<optional>'",
        )


class TestCentosApp(TestApp):
    """
    Test centos specific things.

    Author: Namah Shrestha
    """

    def setUp(self) -> None:
        """
        Setup Centos Specific things.

        Author: Namah Shrestha
        """
        self.instance_hash: str = "test_hash"
        self.dummy_create_message: dict = {
            constants.INSTANCE_OS: constants.CENTOS,
            constants.COMMAND: constants.CREATE,
            constants.INSTANCE_HASH: self.instance_hash,
        }
        self.dummy_exec_message: dict = {
            constants.INSTANCE_OS: constants.CENTOS,
            constants.COMMAND: constants.EXECUTE,
            constants.INSTANCE_HASH: self.instance_hash,
            constants.EXEC_COMMAND: "ls",
        }
        self.dummy_delete_message: dict = {
            constants.INSTANCE_OS: constants.CENTOS,
            constants.COMMAND: constants.DELETE,
            constants.INSTANCE_HASH: self.instance_hash,
        }

        self.container_name: str = constants.CENTOS_CONTAINER_NAME.format(
            self.instance_hash
        )
        self.dockerfile_name: str = constants.CENTOS_DOCKERFILE_NAME
        self.filter_container_command: str = constants.CENTOS_FILTER_CONTAINER.format(
            self.container_name
        )

    def test_socket_responses(self) -> None:
        """
        1. Test create container.
            - The response should be [0]
            - The container should be created
        2. Test exec command with ls.
            - The response should be list of directories.
        3. Test delete command.
            - The response should be [2]
            - The container should be deleted.

        Author: Namah Shrestha
        """
        # create the container first
        create_instance_mgr_obj: im.InstanceManager = im.CentosInstanceManager(
            self.dummy_create_message[constants.COMMAND],
            self.dummy_create_message[constants.INSTANCE_HASH],
        )
        test_send_create_container_task: asyncio.Task = (
            asyncio.get_event_loop().create_task(
                test_send(json.dumps(self.dummy_create_message))
            )
        )
        res_create: str = asyncio.get_event_loop().run_until_complete(
            test_send_create_container_task
        )
        self.assertEqual(
            res_create,
            "[0]",
        )
        self.assertEqual(len(create_instance_mgr_obj.list_container()[:-1]), 1)
        test_send_exec_container_task: asyncio.Task = (
            asyncio.get_event_loop().create_task(
                test_send(json.dumps(self.dummy_exec_message))
            )
        )
        res_exec: str = asyncio.get_event_loop().run_until_complete(
            test_send_exec_container_task
        )
        self.assertEqual(
            res_exec,
            '["bin", "dev", "etc", "home", "lib", "lib64", "lost+found", "media", "mnt", "opt", "proc", "root", "run", "sbin", "srv", "sys", "tmp", "usr", "var", ""]',
        )
        test_send_delete_container_task: asyncio.Task = (
            asyncio.get_event_loop().create_task(
                test_send(json.dumps(self.dummy_delete_message))
            )
        )
        delete_instance_mgr_obj: im.InstanceManager = im.CentosInstanceManager(
            self.dummy_delete_message[constants.COMMAND],
            self.dummy_delete_message[constants.INSTANCE_HASH],
        )
        res_delete: bool = asyncio.get_event_loop().run_until_complete(
            test_send_delete_container_task
        )
        self.assertEqual(
            res_delete,
            "[2]",
        )
        self.assertEqual(len(delete_instance_mgr_obj.list_container()[:-1]), 0)
