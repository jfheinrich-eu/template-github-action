"""Unit Test for class libs.helper.Helper"""
import os

from git import Repo
from git.util import IterableList

from github_action.libs.helper import Helper


class repo_double_tag(Repo):
    """Test double to simulate selecting tag"""
    tags: IterableList[str] = []

    def __init__(self, path=None, odbt=..., search_parent_directories=False, expand_vars=True):
        self.tags = ["v1.0.0"]


class repo_double_branch(Repo):
    """Test double to simulate selecting active branch"""
    tags: IterableList[str] = []
    active_branch = "feature/testing"

    def __init__(self, path=None, odbt=..., search_parent_directories=False, expand_vars=True):
        pass


def test_get_version_tag() -> None:
    """Test if we get the expected tag"""
    cwd = os.path.realpath(os.path.curdir)
    print(cwd)
    os.chdir('./src/github_action')
    vers = Helper.get_version(repository=repo_double_tag)
    os.chdir(cwd)
    assert vers == "v1.0.0"


def test_get_version_branch() -> None:
    """Test if we get the expected tag"""
    cwd = os.path.realpath(os.path.curdir)
    os.chdir('./src/github_action')
    vers = Helper.get_version(repository=repo_double_branch)
    os.chdir(cwd)
    assert vers == "feature/testing"
