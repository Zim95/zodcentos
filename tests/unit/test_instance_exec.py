"""
Unit tests for instance exec

Author: Namah Shrestha
"""
# built-ins
import unittest
import unittest.mock as mock

# modules
import src.instance_exec as ie
import src.constants as constants


class BaseTestInstanceExec:
    """
    Base Test Instance Exec for executing commands for the container.
    Since the method of initialization is common for object for each implementation of OS,
    a common class is used for it.

    Author: Namah Shrestha
    """

    def __init__(
        self,
        command: str,
        instance_hash: str,
        container_name: str,
        filter_container_command: str,
        instance_exec_obj: ie.InstanceExec,
    ) -> None:
        """
        Base instance exec test constructor

        Author: Namah Shrestha
        """
        self.command: str = command
        self.instance_hash: str = instance_hash
        self.container_name: str = container_name
        self.filter_container_command: str = filter_container_command.format(
            self.container_name
        )
        self.instance_exec_obj: ie.InstanceExec = instance_exec_obj


class TestCentosInstanceExec(unittest.TestCase, BaseTestInstanceExec):
    """
    Centos Instance Exec test case

    Author: Namah Shrestha
    """

    def setUp(self) -> None:
        """
        Setup for CentosInstanceExec.

        Author: Namah Shrestha
        """
        self.instance_hash: str = "test_centos_instance_hash"
        self.container_name: str = constants.CENTOS_CONTAINER_NAME.format(
            self.instance_hash
        )
        self.filter_container_command: str = constants.CENTOS_FILTER_CONTAINER.format(
            self.container_name
        )

    def test_parse_command_result(self) -> None:
        """
        Test the functionality of parse_command_result method.

        Author: Namah Shrestha
        """
        self.command = "EXEC"
        self.exec_command = "ls"
        self.instance_exec_obj: ie.InstanceExec = ie.CentosInstanceExec(
            self.command, self.instance_hash
        )
        res: list = self.instance_exec_obj.parse_command_result("a\nb")
        self.assertEqual(res, ["a", "b"])

    @mock.patch("os.popen")
    def test_exec_instance(self, mock_popen: mock.MagicMock) -> None:
        """
        Test execution command for docker container exec

        Author: Namah Shrestha
        """
        mock_popen.read = mock.MagicMock()
        self.command = "EXEC"
        self.exec_command = "ls"
        self.instance_exec_obj: ie.InstanceExec = ie.CentosInstanceExec(
            self.command, self.instance_hash
        )
        super(BaseTestInstanceExec, self).__init__()
        self.instance_exec_obj.exec_instance(self.exec_command)
        mock_popen.assert_called_with(
            f"docker container exec -it $({self.filter_container_command}) {self.exec_command}"
        )

    @mock.patch("src.instance_exec.InstanceExec.parse_command_result")
    @mock.patch("src.instance_exec.InstanceExec.exec_instance")
    def test_handle(
        self,
        mock_exec_instance: mock.MagicMock,
        mock_parse_command_result: mock.MagicMock,
    ) -> None:
        """
        When command is exec, execute the exec_command in the instance.

        Author: Namah Shrestha
        """
        self.command = "EXEC"
        self.exec_command = "ls"
        self.instance_exec_obj: ie.InstanceExec = ie.CentosInstanceExec(
            self.command, self.instance_hash
        )
        super(BaseTestInstanceExec, self).__init__()
        self.instance_exec_obj.handle(self.exec_command)
        mock_exec_instance.assert_called_with("ls")
        mock_parse_command_result.assert_called()
