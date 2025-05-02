"""Test app.py"""
from pytest import CaptureFixture
import app
import re
import os
import pytest
from github_action import get_info

IN_GITHUB_ACTIONS = os.getenv("GITHUB_ACTIONS") == "true"


@pytest.mark.skipif(IN_GITHUB_ACTIONS, reason="Test doesn't work in GitHub Actions.")
# pragma no cover
def test_app_main(capsys: CaptureFixture[str], mocker) -> None:
    """Test for app.main()"""
    pattern = re.compile(
        r'github-action v[0-9]+\.[0-9]+\.[0-9]+\nCreated by: Joerg Heinrich <joerg@jfheinrich.eu>\n', re.MULTILINE)
    app.main()
    captured = capsys.readouterr()
    assert pattern.match(captured.out) is not None


@pytest.mark.skipif(IN_GITHUB_ACTIONS, reason="Test doesn't work in GitHub Actions.")
# pragma no cover
def test_githubaction_get_info(capsys: CaptureFixture[str]) -> None:
    """Test for github_action.get_info"""
    pattern = re.compile(
        r'github-action v[0-9]+\.[0-9]+\.[0-9]+\nCreated by: Joerg Heinrich <joerg@jfheinrich.eu>\n', re.MULTILINE)
    get_info()
    captured = capsys.readouterr()
    assert pattern.match(captured.out) is not None
