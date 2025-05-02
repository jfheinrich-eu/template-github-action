"""Modul github_action"""

from github_action import config
from github_action import main

GitHubAction = main.GitHubAction


def get_info():
    print(
        f"{config.PACKAGE_NAME} v{config.__version__}")
    print(
        f"Created by: {config.__author__} <{config.__email__}>")
