"""
Here we test instance message. Unit

Author: Namah Shrestha
"""
# builitins
import unittest
import json

# modules
import src
import src.constants as constants


class TestInstanceInitialization(unittest.TestCase):
    """
    We will check the initialization of the instance class.

    Author: Namah Shrestha
    """

    def setUp(self) -> None:
        """
        Initialize the instance.

        Author: Namah Shrestha
        """
        self.dummy_instance_hash: str = "asdf"
        self.instance_obj: src.Instance = src.Instance(self.dummy_instance_hash)

    def test_instance_hash_data_member(self) -> None:
        """
        Here we test and see that a proper instance hash has been set for the
        instance_hash data member.

        Author: Namah Shrestha
        """
        self.assertEqual(self.instance_obj.instance_hash, self.dummy_instance_hash)


class TestSrcInstanceMessage(unittest.TestCase):
    """
    We will be testing instance message outcomes.

    Author: Namah Shrestha
    """

    def setUp(self) -> None:
        """
        Here we initialize dummy messages to test.
        """
        self.dummy_text_message: str = "dummy_test_message"
        self.dummy_incorrectformat_message: dict = json.dumps({"x": 1})
        self.dummy_proper_message: dict = json.dumps(
            {
                constants.INSTANCE_OS: constants.CENTOS,
                constants.COMMAND: constants.CREATE,
                constants.INSTANCE_HASH: "test_hash",
                constants.EXEC_COMMAND: "ls",
            }
        )

    def test_is_schema_valid(self) -> None:
        """
        Here we will test the is_schema_valid static method.
        1. Dummy text message should raise an error.
        2. Dummy json but incorrect schema should return false.
        3. Proper message with correct schema should return true.

        Author: Namah Shrestha
        """
        try:
            src.InstanceMessage.is_schema_valid(self.dummy_text_message)
        except TypeError as te:
            self.assertEqual(
                isinstance(te, TypeError),
                True,
            )
        self.assertEqual(
            False,
            src.InstanceMessage.is_schema_valid(self.dummy_incorrectformat_message),
        )
        self.assertEqual(
            True, src.InstanceMessage.is_schema_valid(self.dummy_proper_message)
        )

    def test_decode_message(self) -> None:
        """
        Here we will test the decode_message static method.
        1. Dummy text message should raise an error.
        2. Dummy json dumps should return a dictionary.

        Author: Namah Shrestha
        """
        try:
            src.InstanceMessage.decode_message(self.dummy_text_message)
        except TypeError as te:
            self.assertEqual(
                isinstance(te, TypeError),
                True,
            )
        self.assertEqual(
            {"x": 1},
            src.InstanceMessage.decode_message(self.dummy_incorrectformat_message),
        )
