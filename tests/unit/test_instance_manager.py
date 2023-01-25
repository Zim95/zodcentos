# built-ins
import unittest
import unittest.mock as mock
import typing

# modules
import src.instance_manager as im


class TestInstance(unittest.TestCase):
    def setUp(self) -> None:
        self.instance_mgr_obj: im.InstanceManager = im.InstanceManager()

    @mock.patch("os.system")
    def test_creation(self, mock_system) -> None:
        self.instance_mgr_obj.create_instance()
        result: typing.List = [str(call) for call in mock_system.mock_calls]
        self.assertEqual(
            result,
            [
                "call('docker image build . -t centos-demo:latest -f Dockerfile.centos')",
                "call('docker container run --name centos_demo -d centos-demo:latest')",
            ],
        )

    @mock.patch("os.system")
    def test_deletion(self, mock_system) -> None:
        self.instance_mgr_obj.delete_instance()
        result: typing.List = [str(call) for call in mock_system.mock_calls]
        self.assertEqual(
            result,
            [
                "call(\"docker container stop $(docker container ls -aq --filter 'name=centos_demo')\")",
                "call(\"docker container rm $(docker container ls -aq --filter 'name=centos_demo')\")",
                "call('docker image rm -f centos-demo:latest')",
            ],
        )
