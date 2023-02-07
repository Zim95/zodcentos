"""
Integration tests for instance manager.

Author: Namah Shrestha
"""

# built-ins
import unittest

# modules
import src.instance_manager as im
import src.constants as constants


class BaseTestInstanceManager:
    """
    Base Test Instance Manager for setting instance manager object.
    Since the method of initialization is common for object for
    each implementation of OS,
    a common class is used for it.

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
        """
        Base instance manager constructor

        Author: Namah Shrestha
        """
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


class TestCentosInstanceManager(unittest.TestCase, BaseTestInstanceManager):
    """
    Centos Instance manager test cases

    Author: Namah Shrestha
    """

    def setUp(self) -> None:
        """
        Setup for CentosInstanceManager integration test.

        Author: Namah Shrestha
        """
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

    def test_creation(self) -> None:
        """
        Test creation of instances. Integration

        Author: Namah Shrestha
        """
        self.command = constants.CREATE
        self.instance_mgr_obj: im.InstanceManager = im.CentosInstanceManager(
            self.command, self.instance_hash
        )
        super(BaseTestInstanceManager, self).__init__()
        self.instance_mgr_obj.create_instance()
        container_list_res: list = self.instance_mgr_obj.list_container()
        self.assertEqual(len(container_list_res[:-1]), 1)

    def test_deletion(self) -> None:
        """
        Test deletion of instances. Integration.

        Author: Namah Shrestha
        """
        self.command = constants.DELETE
        self.instance_mgr_obj: im.InstanceManager = im.CentosInstanceManager(
            self.command, self.instance_hash
        )
        super(BaseTestInstanceManager, self).__init__()
        self.instance_mgr_obj.delete_instance()
        container_list_res: list = self.instance_mgr_obj.list_container()
        self.assertEqual(len(container_list_res[:-1]), 0)

    def test_handle(self) -> None:
        """
        When command is create, create_instance is called.
        When command is delete, delete_instance is called.

        Author: Namah Shrestha
        """
        self.command = constants.CREATE
        self.instance_mgr_obj: im.InstanceManager = im.CentosInstanceManager(
            self.command, self.instance_hash
        )
        super(BaseTestInstanceManager, self).__init__()
        res: list = self.instance_mgr_obj.handle()
        container_list_res: list = self.instance_mgr_obj.list_container()
        self.assertEqual(len(container_list_res[:-1]), 1)
        self.assertEqual(res, [0])

        self.command = constants.DELETE
        self.instance_mgr_obj: im.InstanceManager = im.CentosInstanceManager(
            self.command, self.instance_hash
        )
        super(BaseTestInstanceManager, self).__init__()
        self.instance_mgr_obj.handle()
        res: list = self.instance_mgr_obj.handle()
        container_list_res: list = self.instance_mgr_obj.list_container()
        self.assertEqual(len(container_list_res[:-1]), 0)
        self.assertEqual(res, [2])
