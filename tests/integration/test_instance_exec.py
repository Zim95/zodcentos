"""
Integration tests for instance exec

Author: Namah Shrestha
"""
# built-ins
import unittest

# modules
import src.instance_exec as ie
import src.instance_manager as im
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
        Here we need to make sure the container exists before actually executing the commands.
        Therefore, we need to use the instance manager to create the container.

        Author: Namah Shrestha
        """
        self.instance_hash: str = "test_centos_instance_hash"
        self.container_name: str = constants.CENTOS_CONTAINER_NAME.format(
            self.instance_hash
        )
        self.filter_container_command: str = constants.CENTOS_FILTER_CONTAINER.format(
            self.container_name
        )

        """ create the container """
        self.command = constants.CREATE
        super(BaseTestInstanceExec, self).__init__()
        self.instance_mgr_obj: im.InstanceManager = im.CentosInstanceManager(
            self.command, self.instance_hash
        )
        self.instance_mgr_obj.handle()

    def test_exec_instance(self) -> None:
        """
        Test execution command for docker container exec

        Author: Namah Shrestha
        """
        self.command = constants.EXECUTE
        self.exec_command = "ls"
        self.instance_exec_obj: ie.InstanceExec = ie.CentosInstanceExec(
            self.command, self.instance_hash
        )
        super(BaseTestInstanceExec, self).__init__()
        res: str = self.instance_exec_obj.exec_instance(self.exec_command)
        self.assertEqual(
            res,
            (
                "bin  etc   lib\t  lost+found  mnt  "
                "proc  run   srv  tmp  var\ndev  home  lib64  media       "
                "opt  root  sbin  sys  usr\n"
            ),
        )

    def test_handle(self) -> None:
        """
        When command is exec, execute the exec_command in the instance.

        Author: Namah Shrestha
        """
        self.command = constants.EXECUTE
        self.exec_command = "ls"
        self.instance_exec_obj: ie.InstanceExec = ie.CentosInstanceExec(
            self.command, self.instance_hash
        )
        super(BaseTestInstanceExec, self).__init__()
        res: list = self.instance_exec_obj.handle(self.exec_command)
        self.assertEqual(
            res,
            [
                "bin  etc   lib\t  lost+found  mnt  proc  run   srv  tmp  var",
                "dev  home  lib64  media       opt  root  sbin  sys  usr",
                "",
            ],
        )

    def tearDown(self) -> None:
        """
        Delete the container

        Author: Namah Shrestha
        """

        """ delete the container """
        self.command = constants.DELETE
        super(BaseTestInstanceExec, self).__init__()
        self.instance_mgr_obj: im.InstanceManager = im.CentosInstanceManager(
            self.command, self.instance_hash
        )
        self.instance_mgr_obj.handle()
