"""
Unit test for the main web socket application.

Author: Namah Shrestha
"""
# builtins
import unittest
import unittest.mock as mock
import json

# modules
import app
import asyncio
import src.constants as constants


class TestApp(unittest.TestCase):
    """
    Tests for the socket application function. Unit.
    We will mock all external calls.

    Author: Namah Shrestha
    """

    def setUp(self) -> None:
        """
        Socket handler function mock setup

        Author: Namah Shrestha
        """
        self.mock_handler: mock.AsyncMock = mock.AsyncMock
        self.mock_handler.recv: mock.AsyncMock = mock.AsyncMock()
        self.mock_handler.send: mock.AsyncMock = mock.AsyncMock()
        self.mock_handler.send.return_value = "test_send"
        self.dummy_return_value: dict = {
            constants.INSTANCE_OS: constants.CENTOS,
            constants.COMMAND: constants.CREATE,
            constants.INSTANCE_HASH: "test_hash",
            constants.EXEC_COMMAND: "ls",
        }

    def test_socket_handler_with_nondecodable_string(self) -> None:
        """
        Invalid message format: non decodable string should raise TypeError

        Author: Namah Shrestha
        """
        self.mock_handler.recv.return_value = "test_message"
        async_handler: mock.MagicMock = app.socket_handler(self.mock_handler)
        try:
            asyncio.run(async_handler)
        except TypeError as e:
            self.assertEqual(isinstance(e, TypeError), True)

    def test_socket_handler_with_invalid_message_format(self) -> None:
        """
        Invalid message format: improper schema should raise ValueError

        Author: Namah Shrestha
        """
        self.mock_handler.recv.return_value = '{"x": 1}'
        async_handler: mock.MagicMock = app.socket_handler(self.mock_handler)
        try:
            asyncio.run(async_handler)
        except ValueError as e:
            self.assertEqual(isinstance(e, ValueError), True)

    def test_unsupported_instance_os(self) -> None:
        """
        Valid message format but unsupported OS command should raise ValueError

        Author: Namah Shrestha
        """
        self.dummy_return_value[constants.INSTANCE_OS] = "unsupported_dummy_os"
        self.mock_handler.recv.return_value = json.dumps(self.dummy_return_value)
        async_handler: mock.MagicMock = app.socket_handler(self.mock_handler)
        try:
            asyncio.run(async_handler)
        except ValueError as e:
            self.assertEqual(isinstance(e, ValueError), True)

    def test_unsupported_command(self) -> None:
        """
        Valid message format but unsupported command should raise ValueError

        Author: Namah Shrestha
        """
        self.dummy_return_value[constants.COMMAND] = "unsupported_dummy_command"
        self.mock_handler.recv.return_value = json.dumps(self.dummy_return_value)
        async_handler: mock.MagicMock = app.socket_handler(self.mock_handler)
        try:
            asyncio.run(async_handler)
        except ValueError as e:
            self.assertEqual(isinstance(e, ValueError), True)


class TestAppCentos(TestApp):
    """
    Tests for socket application related to Centos instance.

    Author: Namah Shrestha
    """

    def setUp(self) -> None:
        super().setUp()
        self.instance_hash: str = "test_hash"
        self.container_name: str = constants.CENTOS_CONTAINER_NAME.format(
            self.instance_hash
        )
        self.filter_container_command: str = constants.CENTOS_FILTER_CONTAINER.format(
            self.container_name
        )
        self.image_name: str = constants.CENTOS_IMAGE_NAME
        self.image_tag: str = constants.CENTOS_IMAGE_TAG

    @mock.patch("os.system")
    def test_instance_manager_call(self, mock_system) -> None:
        """
        Check if instance manager commands are called upon setting appropriate commands
        and instance os.

        Author: Namah Shrestha
        """
        self.dummy_return_value[constants.COMMAND] = constants.CREATE
        self.mock_handler.recv.return_value = json.dumps(self.dummy_return_value)
        async_handler: mock.MagicMock = app.socket_handler(self.mock_handler)
        try:
            asyncio.run(async_handler)
        except Exception:
            """
            This shows that instance_manager handle was called which inturn called
            instance_manager.create_instance method.

            Author: Namah Shrestha
            """
            mock_system.assert_called_with(
                f"docker container run --name {self.container_name} -d {self.image_name}:{self.image_tag}"
            )

        self.dummy_return_value[constants.COMMAND] = constants.DELETE
        self.mock_handler.recv.return_value = json.dumps(self.dummy_return_value)
        async_handler: mock.MagicMock = app.socket_handler(self.mock_handler)
        try:
            asyncio.run(async_handler)
        except Exception:
            """
            This shows that instance_manager handle was called which inturn called
            instance_manager.delete_instance method.

            Author: Namah Shrestha
            """
            mock_system.assert_called_with(
                f"docker image rm -f {self.image_name}:{self.image_tag}"
            )

    @mock.patch("os.popen")
    def test_instance_exec_call(self, mock_popen) -> None:
        """
        Check if instance exec command is called upon setting appropriate commands
        and instance os.

        Author: Namah Shrestha
        """
        self.dummy_return_value[constants.COMMAND] = constants.EXECUTE
        self.mock_handler.recv.return_value = json.dumps(self.dummy_return_value)
        async_handler: mock.MagicMock = app.socket_handler(self.mock_handler)
        try:
            asyncio.run(async_handler)
        except Exception:
            """
            This shows that intance_exec handle was called which inturn called
            instance_exec.exec_instance method.

            Author: Namah Shrestha
            """
            mock_popen.assert_called_with(
                f"docker container exec $({self.filter_container_command}) {self.dummy_return_value[constants.EXEC_COMMAND]}"
            )
