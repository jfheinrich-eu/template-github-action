#!/usr/bin/env python3
import os
import sys

from github_action import config


class GitHubAction:
    """Main class for this action"""

    @staticmethod
    def get_argument(arg_position: int, env_name: str = "", args: list[str] = []) -> (str | None):
        """
        Helper function to get the program arguments from the commandline or the environment

        Args:
            arg_position: Index in sys.argv
            env_name: Name of the environment variable, optional
            args: List of arguments, if None then use sys.argv
        """
        ArgumentList = sys.argv if args == [] else args

        if len(ArgumentList) > arg_position:
            return ArgumentList[arg_position]

        return None if env_name == "" else os.getenv(env_name)

    @staticmethod
    def get_info() -> str:  # pragma no cover
        return f"{config.PACKAGE_NAME} v{config.__version__}\nCreated by: {config.__author__} <{config.__email__}>"


if __name__ == '__main__':  # pragma no cover
    print(GitHubAction.get_info())
    argument: (str | None) = GitHubAction.get_argument(1, "INPUT_ARGUMENT")
