#!/usr/bin/env python
"""Main entrypoint for the action"""
from github_action import GitHubAction
import sys
sys.path.append('.')


def main() -> None:  # pragma no cover
    print(GitHubAction.get_info())


if __name__ == "__main__":  # pragma no cover
    main()
