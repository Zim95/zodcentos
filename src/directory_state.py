"""
This is the current state of the directory.
We need to change it as per the commands.

Author: Namah Shrestha
"""

# builtins
import os
import re

# modules
import src.constants as constants


class DirectoryStateManager:
    """
    This will keep track of the working directory.

    Author: Namah Shrestha
    """

    def __init__(self) -> None:
        """
        Set the default value of current working directory
        Author: Namah Shrestha
        """
        self._curr_dir: str = os.path.abspath("")

    @property
    def curr_dir(self) -> None:
        """
        Get the value of current working directory.
        Author: Namah Shrestha
        """
        return self._curr_dir

    @curr_dir.setter
    def curr_dir(self, dirc: str) -> str:
        """
        Set the value of the current working directory.
        Here we need to validate the dir first.
        Author: Namah Shrestha
        """
        if re.match(constants.CHANGE_DIRECTORY_CMD_PATTERN.split(" ")[-1], dirc):
            """Repeatedly remove // until only one is found"""
            while dirc.find("//") >= 0:
                dirc = dirc.replace("//", "/")
            self._curr_dir = dirc


class ChangeDirectoryHandler:
    def __init__(self) -> None:
        """
        Create a directory state manager.

        Author: Namah Shrestha
        """
        self.dir_state_manager: DirectoryStateManager = DirectoryStateManager()

    def is_cd_command(self, cmd: str) -> bool:
        """
        Check if the command is a valid cd command

        Author: Namah Shrestha
        """
        if re.match(constants.CHANGE_DIRECTORY_CMD_PATTERN, cmd):
            return True
        return False

    def parse_cd_command(self, cmd: str) -> str:
        """
        Return the directory location after cd command
        Eg: cd <location> -> <location>

        Also replace all instances of continuous backslashes.
        Eg: /// -> /, // -> /

        Author: Namah Shrestha
        """
        if not self.is_cd_command(cmd):
            return ""
        dirc = cmd.split(
            " ",
        )[-1]
        """Repeatedly remove // until only one is found"""
        while dirc.find("//") >= 0:
            dirc = dirc.replace("//", "/")
        return dirc

    def change_directory(self, cmd: str) -> str:
        """
        Change the directory based on the cd command

        Author: Namah Shrestha
        """
        if not self.is_cd_command(cmd):
            return ""
        dirc: str = self.parse_cd_command(cmd)
        if not dirc:
            return ""
        """
        Now use os.chdir without actually changing the directory
        We do this by reseting the actual workdir to abspath.
        We only change the curr_dir to the desired path.
        """
        # get the current working directory
        current_dir: str = self.get_cwd()
        os.chdir(current_dir)  # change to current_dir_value
        try:
            os.chdir(dirc)  # change directory relatively
            self.dir_state_manager.curr_dir = (
                os.getcwd()
            )  # change the current directory to the change directory
        except FileNotFoundError:
            """
            When there is an error in this step chdir.
            Dont change curr_dir.
            But continue with the remaining process
            """
            print("No such directory, will not set the value")
        os.chdir(
            constants.MAIN_WORKING_DIRECTORY
        )  # re-set the actual working directory to the abspath
        return self.get_cwd()

    def get_cwd(self) -> str:
        """
        Get the current working directory from the directory state manager

        Author: Namah Shrestha
        """
        return self.dir_state_manager.curr_dir
