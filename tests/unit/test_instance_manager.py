"""
Unit tests for instance manager.

Author: Namah Shrestha
"""

# built-ins
import unittest
import unittest.mock as mock
import typing

# modules
import src.instance_manager as im
import src.constants as constants


class BaseTestInstanceManager:
    """
    Base Test Instance Manager for setting instance manager object.
    Since the method is common, a common class is used for it.

    Author: Namah Shrestha
    """

    def __init__(
        self,
        command: str,
        instance_hash: str,
        image_name: str,
        image_tag: str,
        container_name: str,
        dockerfile_name: str,
        filter_container_command: str,
        instance_mgr_obj: im.InstanceManager,
    ) -> None:
        self.command: str = command
        self.instance_hash: str = instance_hash
        self.image_name: str = image_name
        self.image_tag: str = image_tag
        self.container_name: str = container_name
        self.dockerfile_name: str = dockerfile_name
        self.filter_container_command: str = filter_container_command.format(
            self.container_name
        )
        self.instance_mgr_obj: im.InstanceManager = instance_mgr_obj

    def extract_cmd_from_mock_call_str(self, mock_call_str) -> str:
        """
        Turn call(<command>) to <command>
        """
        mock_call_str = mock_call_str.replace("call(", "")
        mock_call_str = mock_call_str[:-1]
        return eval(mock_call_str)


class TestCentosInstanceManager(unittest.TestCase, BaseTestInstanceManager):
    """
    Centos Instance manager test cases

    Author: Namah Shrestha
    """

    def setUp(self) -> None:
        self.instance_hash: str = "test_centos_instance_hash"
        self.image_name: str = constants.CENTOS_IMAGE_NAME
        self.image_tag: str = constants.CENTOS_IMAGE_TAG
        self.container_name: str = constants.CENTOS_CONTAINER_NAME.format(
            self.instance_hash
        )
        self.dockerfile_name: str = constants.CENTOS_DOCKERFILE_NAME
        self.filter_container_command: str = constants.CENTOS_FILTER_CONTAINER.format(
            self.container_name
        )

    @mock.patch("os.system")
    def test_creation(self, mock_system) -> None:
        """
        Test creation of instances. Unit

        Author: Namah Shrestha
        """
        self.command = "CREATE"
        self.instance_mgr_obj: im.InstanceManager = im.CentosInstanceManager(
            self.command, self.instance_hash
        )
        super(BaseTestInstanceManager, self).__init__()
        self.instance_mgr_obj.create_instance()
        result: typing.List = [str(call) for call in mock_system.mock_calls]
        result = list(map(lambda x: self.extract_cmd_from_mock_call_str(x), result))
        self.assertEqual(
            result,
            [
                f"docker image build . -t {self.image_name}:{self.image_tag} -f {self.dockerfile_name}",
                f"docker container run --name {self.container_name} -d {self.image_name}:{self.image_tag}",
            ],
        )

    @mock.patch("os.system")
    def test_deletion(self, mock_system) -> None:
        """
        Test deletion of instances. Unit.

        Author: Namah Shrestha
        """
        self.command = "DELETE"
        self.instance_mgr_obj: im.InstanceManager = im.CentosInstanceManager(
            self.command, self.instance_hash
        )
        super(BaseTestInstanceManager, self).__init__()
        self.instance_mgr_obj.delete_instance()
        result: typing.List = [str(call) for call in mock_system.mock_calls]
        result = list(map(lambda x: self.extract_cmd_from_mock_call_str(x), result))
        self.assertEqual(
            result,
            [
                f"docker container stop $({self.filter_container_command})",
                f"docker container rm $({self.filter_container_command})",
                f"docker image rm -f {self.image_name}:{self.image_tag}",
            ],
        )
