<p align="center">
  <a href="" rel="noopener">
 <img width=200px height=200px src="https://imgur.com/r85zecB.png" alt="Template Repository: GitHub Actions"></a>
</p>

<h1 align="center">Template Repository: GitHub Actions</h1>

<div align="center">

[![Status](https://img.shields.io/badge/status-active-success.svg)]()
![Maintainer](https://img.shields.io/badge/maintainer-@jfheinrich-blue)
[![GitHub Issues](https://img.shields.io/github/issues/jfheinrich-eu/template-github-action.svg)](https://github.com/jfheinrich-eu/template-github-action/issues)
[![GitHub pull-requests](https://img.shields.io/github/issues-pr/jfheinrich-eu/template-github-action.svg)](https://GitHub.com/Naereen/StrapDown.js/pull/)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](/LICENSE)

</div>

---

<p align="center"> Template repository for GitHub Actions written in Python
    <br>
</p>

<h2>Table of Contents</h2>

- [About](#about)
- [Getting Started](#getting-started)
  - [Requirements](#requirements)
  - [GitHub Workflow](#github-workflow)
    - [integration.yml](#integrationyml)
    - [create-requirements.yml ](#create-requirementsyml)
    - [tag.yml](#tagyml)
    - [pr\_labler.yml](#pr_lableryml)
    - [pr.yml](#pryml)
    - [release.yml](#releaseyml)
- [Usage](#usage)
- [Authors](#authors)
- [Acknowledgements](#acknowledgements)



## About

This template could be the starting point for develop GitHub Actions in `python`.

This project will be maintenance by `poetry`.

## Getting Started

This template repository provides a skeleton to invent a docker containernized GitHub Action written in `python`. It provides a workflow skeleton:

- on `push`
  - all branches
    - integration.yml
    - create-requirements.yml
  - branches: `main, master`
    - tag.yml
- on `pull_request_target`
  - pr_labler.yml
- on `pull_request`
  - types: `labeled, unlabeled, opened, edited, reopened, synchronize, ready_for_review`
    - pr.yml
- on `push`
  - type: `tag`
    - release.yml

### Requirements

The dependencies are managed by `poetry`, so you have to start, install the base tools:

```bash
$ cd [project root]
$ npm ci
$ pip install poetry
$ poetry sync --with test
```

After this, you can customize the skeleton for your project

**pyproject.toml**

```bash
$ poetry init --name="repalce with your project name" \
              --author='{name: "replace with authors name", email: "replace with authors email"}' \
              --license="MIT" \
              --description="Short description of your package"
```

### GitHub Workflow

#### integration.yml

This workflow is for code quality and testing

```yaml
name: Integration Test
permissions:
  contents: read
  pull-requests: write

on: [push]

jobs:
  lint:
    name: Lint
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Set up Python 3.12.10
        uses: actions/setup-python@v5.5.0
        with:
          python-version: "3.12.10"

      - name: Install dependencies
        run: |
          pip install poetry
          poetry install --with test

      - name: Lint
        run: poetry run flake8 src/ tests/

      - name: Tests
        run: poetry run pytest --cov --cov-branch --cov-report xml:coverage/cov.xml --cov-report lcov:coverage/cov.info

      - name: Upload results to Codecov
        uses: codecov/codecov-action@v5
        with:
          token: ${{ secrets.CODECOV_TOKEN }}
          slug: jfheinrich-eu/pipreqs-action
          files: coverage/cov.xml
          verbose: true

      - name: Generate Code Coverage report
        id: code-coverage
        uses: barecheck/code-coverage-action@v1
        with:
          barecheck-github-app-token: ${{ secrets.BARECHECK_GITHUB_APP_TOKEN }}
          lcov-file: "coverage/cov.info"
          send-summary-comment: true
          show-annotations: ''
```

#### create-requirements.yml <a name="create-requirementsyml">

This workflow creates or updates the `requirements.txt` file.

```yaml
name: Create requirements.txt
permissions:
  contents: write
  pull-requests: write

on: [push]

jobs:
  create-requirements:
    name: Create requirements
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v4

      - name: Set up Python 3.12.10
        uses: actions/setup-python@v5.5.0
        with:
          python-version: "3.12.10"

      - name: Install dependencies
        run: |
          pip install poetry poetry-plugin-export
          poetry sync --with test

      - name: Automatic requirements.txt for Python Project
        run: |
          poetry export --without-hashes --format=requirements.txt --with test --output tmp_requirements.txt
          diff requirements.txt tmp_requirements.txt >/dev/null 2>&1
          if [ $? -ne 0 ]; then mv -f tmp_requirements.txt requirements.txt; fi

      - uses: dorny/paths-filter@v3
        id: changes
        with:
          filters: |
            src:
              - 'requirements.txt'

      - name: Commit changes
        if: steps.changes.outputs.src == 'true'
        uses: stefanzweifel/git-auto-commit-action@v5
        with:
          branch: ${{ github.ref_name }}
          commit_message: 'Updated requirements file on ${{ github.ref_name }} [skip ci]'
          file_pattern: requirements.txt
```

#### tag.yml

This workflow provides the tagging, release creation and creation of the release notes.

To create the release notes it use the commit message block between these markers:

```html
<!--- START AUTOGENERATED NOTES --->
<!--- END AUTOGENERATED NOTES --->
```

The generated version number is `v` prefixed.

```yaml
name: Release
permissions:
  contents: write
  pull-requests: write

on:
  push:
    branches:
      - main
      - master

jobs:
  bump-tag-version:
    name: Bump and Tag Version
    runs-on: ubuntu-latest
    defaults:
      run:
        shell: bash
    env:
      PSONO_CI_API_KEY_ID: ${{ secrets.PSONO_API_KEY_ID }}
      PSONO_CI_API_SECRET_KEY_HEX: ${{ secrets.PSONO_API_SECRET_KEY_HEX }}
      PSONO_CI_SERVER_URL: ${{ vars.PSONO_SERVER_URL }}
      PSONO_GITHUB_TOKEN_ID: ${{ secrets.PSONO_GITHUB_CLI_TOKEN}}

    steps:
      - name: Get GitHub Token
        id: github-token
        uses: jfheinrich-eu/psono-secret-whisperer@v1.0.0
        with:
          ci_api_key_id: ${{ secrets.PSONO_API_KEY_ID }}
          ci_api_secret_key_hex: ${{ secrets.PSONO_API_SECRET_KEY_HEX }}
          ci_server_url: ${{ vars.PSONO_SERVER_URL }}
          secret_id: ${{ secrets.PSONO_GITHUB_CLI_TOKEN }}
          secret_type: 'secret'
          secret_fields: "password"
          mask_secrets: password

      - uses: actions/checkout@v4

      - uses: jefflinse/pr-semver-bump@v1.7.2
        name: Bump and Tag Version
        with:
          mode: bump
          repo-token: ${{ steps.github-token.outputs.secret1 }}
          major-label: major release
          minor-label: minor release
          patch-label: patch release
          noop-labels: |
            documentation change
            skip-release
            dependencies
          require-release-notes: true
          release-notes-prefix: '<!--- START AUTOGENERATED NOTES --->'
          release-notes-suffix: '<!--- END AUTOGENERATED NOTES --->'
          with-v: true
          base-branch: false
```

#### pr_labler.yml

Provides an automatically labeling on new pull requests, based on the files in the commit

```yaml
name: Pull Request Labeler
permissions:
  contents: read
  pull-requests: write
on: pull_request_target

jobs:
  triage:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/labeler@v5
        with:
          repo-token: ${{ secrets.GITHUB_TOKEN }}
          configuration-path: .github/pr_labeler.yml
          sync-labels: false
```

#### pr.yml

Generates the pull request description

```yaml
name: Release Info
permissions:
  contents: read
  pull-requests: write

on:
  pull_request:
    types: [labeled, unlabeled, opened, edited, reopened, synchronize, ready_for_review]

jobs:
  generate-pr-description:
    if: ${{ github.actor != 'dependabot[bot]' }}
    name: Generate the description on the pull request
    runs-on: ubuntu-latest
    defaults:
      run:
        shell: bash

    steps:
      - uses: actions/checkout@v4

      - uses: octue/generate-pull-request-description@1.0.0.beta-2
        id: pr-description
        with:
          pull_request_url: ${{ github.event.pull_request.url }}
          api_token: ${{ secrets.GITHUB_TOKEN }}

      - name: Update pull request body
        uses: riskledger/update-pr-description@v2
        with:
          body: ${{ steps.pr-description.outputs.pull_request_description }}
          token: ${{ secrets.GITHUB_TOKEN }}

  check-pr:
    if: ${{ github.actor != 'dependabot[bot]' }}
    needs: generate-pr-description
    name: Validate Release Label and Notes
    runs-on: ubuntu-latest
    defaults:
      run:
        shell: bash

    steps:
      - uses: actions/checkout@v4

      - name: Fetch secrets
        id: fetch-secrets
        uses: jfheinrich-eu/psono-secret-whisperer@v1.0.0
        with:
          ci_api_key_id: ${{ secrets.PSONO_API_KEY_ID }}
          ci_api_secret_key_hex: ${{ secrets.PSONO_API_SECRET_KEY_HEX }}
          ci_server_url: 'https://your-psono-server.com'
          secret_id: ${{ secrets.PSONO_GITHUB_CLI_TOKEN }}
          secret_type: 'secret'
          secret_fields: 'password'
          mask_secrets: 'password'

      - uses: jefflinse/pr-semver-bump@v1.7.2
        name: Validate Pull Request Metadata
        with:
          mode: validate
          repo-token: ${{ steps.fetch-secrets.outputs.secret1 }}
          major-label: major release
          minor-label: minor release
          patch-label: patch release
          noop-labels: |
            documentation change
            dependencies
            skip-release
          require-release-notes: true
          release-notes-prefix: '<!--- START AUTOGENERATED NOTES --->'
          release-notes-suffix: '<!--- END AUTOGENERATED NOTES --->'
          with-v: false
          base-branch: false
```

#### release.yml

This workflow runs on a release tag, e.g. `v1.5.20` and generates the `CHANGELOG.md` file.

```yaml
name: Create new release
permissions:
  contents: write
  pull-requests: write

on:
  push:
    tags:
      - 'v[0-9]+.[0-9]+.[0-9]+'

jobs:
  release:
    runs-on: ubuntu-latest
    defaults:
      run:
        shell: bash

    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Update CHANGELOG
        id: changelog
        uses: requarks/changelog-action@v1
        with:
          token: ${{ github.token }}
          tag: ${{ github.ref_name }}

      - name: Create Release
        uses: actions/create-release@v1
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
        with:
          tag_name: ${{ github.ref_name }}
          release_name: 'Release ${{ github.ref_name }}'
          body: ${{ steps.changelog.outputs.changes }}

      - name: Commit CHANGELOG.md
        uses: stefanzweifel/git-auto-commit-action@v5
        with:
          branch: master
          commit_message: 'docs: update CHANGELOG.md for ${{ github.ref_name }} [skip ci]'
          file_pattern: CHANGELOG.md
```

## Usage

To use this template, you have to click on `Use this template` on the [GitHub repository page](https://github.com/jfheinrich-eu/template-github-action).

## Authors

- [@jfheinrich](https://github.com/jfheinrich) - Idea & Initial work

See also the list of [contributors](https://github.com/jfheinrich-eu/jfheinrich-eu/template-github-action/contributors) who participated in this project.

## Acknowledgements

- Hat tip to anyone whose code was used
  - [stefanzweifel/git-auto-commit-action](https://github.com/stefanzweifel/git-auto-commit-action)
  - [actions/create-release](https://github.com/actions/create-release)
  - [requarks/changelog-action](https://github.com/requarks/changelog-action)
  - [jefflinse/pr-semver-bump](https://github.com/jefflinse/pr-semver-bump)
  - [dorny/paths-filter](https://github.com/dorny/paths-filter)
  - [octue/generate-pull-request-description](https://github.com/octue/generate-pull-request-description)
  - [riskledger/update-pr-description](https://github.com/riskledger/update-pr-description)
  - [actions/labeler](riskledger/update-pr-description)
  - [actions/setup-python](https://github.com/actions/setup-python)
