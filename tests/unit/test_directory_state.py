"""
Tests the directory state management. Unit.

We are not mocking external calls,
because the external operations are not costly.
They do not create containers or anything.
Therefore, we are testing them like integration tests,
by testing the actual results.

Author: Namah Shrestha
"""

# built-ins
import unittest
import os

# modules
import src.directory_state as ds
import src.constants as constants


class TestDirectoryStateManager(unittest.TestCase):
    """
    Test DirectoryStateManager class. Unit

    Author: Namah Shrestha
    """

    def setUp(self) -> None:
        """
        Create a directorystate handler object.

        Author: Namah Shrestha
        """
        self.dir_state_manager: ds.DirectoryStateManager = ds.DirectoryStateManager()

    def test_get_curr_dir(self) -> None:
        """
        Get the curr directory value.

        Author: Namah Shrestha
        """
        self.assertEqual(
            self.dir_state_manager.curr_dir, constants.MAIN_WORKING_DIRECTORY
        )

    def test_set_curr_dir(self) -> None:
        """
        Test the setting of curr directory value.

        1. Invalid directory value should not change.
        2. Valid directory value should only change.

        Author: Namah Shrestha
        """
        self.dir_state_manager.curr_dir = "asd qasd"  # invalid directory
        # should not change value
        self.assertEqual(
            self.dir_state_manager.curr_dir, constants.MAIN_WORKING_DIRECTORY
        )
        # valid directory
        self.dir_state_manager.curr_dir = "asd/"
        # should change value.
        self.assertEqual(self.dir_state_manager.curr_dir, "asd/")


class TestChangeDirectoryHandler(unittest.TestCase):
    """
    Test ChangeDirectoryHandler class. Unit.

    Author: Namah Shrestha
    """

    def setUp(self) -> None:
        """
        Create a change directory handler object.

        Author: Namah Shrestha
        """
        self.chdh: ds.ChangeDirectoryHandler = ds.ChangeDirectoryHandler()

    def test_is_cd_command(self) -> None:
        """
        Test if is_cd_command detects directory commands properly.

        Author: Namah Shrestha
        """
        self.assertEqual(self.chdh.is_cd_command("cd"), False)
        self.assertEqual(self.chdh.is_cd_command("cd ../"), True)
        self.assertEqual(self.chdh.is_cd_command("cd ../."), True)
        self.assertEqual(self.chdh.is_cd_command("cd asd"), True)
        self.assertEqual(self.chdh.is_cd_command("cd asd/"), True)
        self.assertEqual(self.chdh.is_cd_command("cd asd/asd/"), True)
        self.assertEqual(self.chdh.is_cd_command("cd asd asd/"), False)
        self.assertEqual(self.chdh.is_cd_command("cd asd/asd////"), True)
        self.assertEqual(self.chdh.is_cd_command("cd asd001/asd1123/"), True)
        self.assertEqual(self.chdh.is_cd_command("cd asd001"), True)
        self.assertEqual(self.chdh.is_cd_command("cd 1235asd/asd123////"), True)

    def test_parse_cd_command(self) -> None:
        """
        Test the output of parse_cd_command method.

        Author: Namah Shrestha
        """
        self.assertEqual(self.chdh.parse_cd_command("cd"), "")
        self.assertEqual(self.chdh.parse_cd_command("cd ../"), "../")
        self.assertEqual(self.chdh.parse_cd_command("cd ../."), "../.")
        self.assertEqual(self.chdh.parse_cd_command("cd asd"), "asd")
        self.assertEqual(self.chdh.parse_cd_command("cd asd/"), "asd/")
        self.assertEqual(self.chdh.parse_cd_command("cd asd/asd/"), "asd/asd/")
        self.assertEqual(self.chdh.parse_cd_command("cd asd asd/"), "")
        self.assertEqual(self.chdh.parse_cd_command("cd asd/asd////"), "asd/asd/")
        self.assertEqual(
            self.chdh.parse_cd_command("cd asd001/asd1123/"), "asd001/asd1123/"
        )
        self.assertEqual(self.chdh.parse_cd_command("cd asd001"), "asd001")
        self.assertEqual(
            self.chdh.parse_cd_command("cd 1235asd//asd123////"), "1235asd/asd123/"
        )

    def test_initial_value(self) -> None:
        """
        Test the initial value of the current working directory
        should be the absolute path.

        Author: Namah Shrestha
        """
        self.assertEqual(self.chdh.get_cwd(), constants.MAIN_WORKING_DIRECTORY)

    def test_get_cwd(self) -> None:
        """
        Test the get cwd method.
        At first test the actual value.
        Then go one step back.
        Then test the changed value.

        Author: Namah Shrestha
        """
        self.assertEqual(self.chdh.get_cwd(), constants.MAIN_WORKING_DIRECTORY)
        self.chdh.change_directory("cd ../")
        self.assertEqual(
            self.chdh.get_cwd(),
            "/".join(constants.MAIN_WORKING_DIRECTORY.split("/")[:-1]),
        )

    def test_change_directory(self) -> None:
        """
        Test cases for change directory.
        0. Invalid directory command returns "".
        1. Go one step back and test value.
        2. Go one step forward and test value.
        3. Going one step back and going to invalid directory
            should not change the curr_dir value.
        4. The actual current working directory should not change
            at last no matter what.

        Author: Namah Shrestha
        """
        """
        0. Invalid directory command returns ""
        """
        self.assertEqual(
            self.chdh.change_directory("cd"),
            "",
        )
        """
        1. one step back
        """
        self.assertEqual(
            self.chdh.change_directory("cd ../"),
            "/".join(constants.MAIN_WORKING_DIRECTORY.split("/")[:-1]),
        )
        """
        2. one step forward to a valid directory
        """
        self.assertEqual(
            self.chdh.change_directory("cd ./zodcentos"),
            constants.MAIN_WORKING_DIRECTORY,
        )
        """
        3. one step forward to invalid directory

        NOTE: We are already at zodcentos directory which is the main_work_dir.
                If we go to zodcentos again, there is no such directory,
                we should get an error.
                This will not change the value of the curr_dir
                Therefore we get the value of main_working_dir.
        """
        self.assertEqual(
            self.chdh.change_directory("cd ./zodcentos"),
            constants.MAIN_WORKING_DIRECTORY,
        )
        """
        4. Actual work dir should not change no matter what.
           Despite changing the current working directory to one step back.
        """
        self.chdh.change_directory("cd ../")
        self.assertEqual(os.getcwd(), constants.MAIN_WORKING_DIRECTORY)
