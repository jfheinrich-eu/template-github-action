"""Tests for class GitHubAction"""
import os
import re

import pytest

from github_action import GitHubAction

IN_GITHUB_ACTIONS = os.getenv("GITHUB_ACTIONS") == "true"


@pytest.mark.skipif(IN_GITHUB_ACTIONS, reason="Test doesn't work in GitHub Actions.")
def test_githubaction_get_info() -> None:  # pragma no cover
    """Tests if get_info() returns the expected string"""
    pattern = re.compile(
        r'github-action v[0-9]+\.[0-9]+\.[0-9]+\nCreated by: Joerg Heinrich <joerg@jfheinrich.eu>', re.MULTILINE)
    info: str = GitHubAction.get_info()
    assert pattern.match(info) is not None


def test_githubaction_get_argument_argv() -> None:
    """Test to get commandline argument"""
    args: list[str] = ["progname", "--testing"]
    argument: (str | None) = GitHubAction.get_argument(1, "", args)
    assert argument == "--testing"


def test_githubaction_get_argument_env() -> None:
    """Test to get commandline argument"""
    args: list[str] = ["progname"]
    os.environ["INPUT_TESTING"] = "value"
    argument: (str | None) = GitHubAction.get_argument(
        1, "INPUT_TESTING", args)
    del os.environ["INPUT_TESTING"]
    assert argument == "value"


def test_githubaction_get_argument_none() -> None:
    """Test to get commandline argument"""
    args: list[str] = ["progname"]
    argument: (str | None) = GitHubAction.get_argument(
        1, "INPUT_TESTING", args)
    assert argument is None
